"""
"""
from __future__ import annotations

import os
import time
import tempfile
import json
import numpy as np

from pathlib import Path
from typing import Any
#from monty.string import marquee, list_strings # is_string,
from monty.json import MontyEncoder
from monty.collections import dict2namedtuple
from ase.atoms import Atoms
from ase.calculators.abinit import Abinit, AbinitProfile
from ase.constraints import ExpCellFilter
from ase.stress import full_3x3_to_voigt_6_stress, voigt_6_to_full_3x3_stress
from abipy.core.abinit_units import eV_Ha, Ang_Bohr
from abipy.core.structure import Structure, StructDiff
from abipy.tools.iotools import workdir_with_prefix
from abipy.dynamics.hist import HistFile
from abipy.flowtk import PseudoTable
from abipy.ml.aseml import print_atoms, get_atoms, CalcBuilder, ase_optimizer_cls, abisanitize_atoms

from time import perf_counter

class Timer:

    def __enter__(self):
        self.time = perf_counter()
        return self

    def __str__(self):
        return self.readout

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.time
        self.readout = f'Time: {self.time:.3f} seconds'


class RelaxationProfiler:

    def __init__(self, atoms: Any, pseudos, xc, kppa, relax_mode: str, fmax: float, mpi_nprocs, steps=500,
                 verbose: int = 0, optimizer="BFGS", nn_name="m3gnet", mpi_runner="mpirun"):
        """
        Args:
            atoms: ASE atoms, pymatgen structure or file with structure.
            pseudos: List of pseudopotentials with cutoff hints.
            xc: String defining the XC functional e.g. LDA or GGA.
            kppa: K-point per atom used to sample the BZ.
            relax_mode: String definining the relaxation mode e.g. "ions" or "cell"
            fmax: Tolerance for structural relaxation in eV/Ang.
            mpi_nprocs: Number of MPI procs used to run Abinit
            steps: Max number of relaxation steps.
            verbose: Verbosity level.
            optimizer: String defining the ASE optimizer or Optimizer instance.
            nn_name: String specifying the ML potential e.g. "m3gnet" or "chgnet".
            mpi_runner:
        """
        atoms = get_atoms(atoms)
        self.initial_atoms = atoms.copy()
        self.xc = xc
        self.relax_mode = relax_mode
        assert self.relax_mode in ("ions", "cell")
        self.fmax = fmax
        self.steps = steps
        self.verbose = verbose
        self.ase_opt_cls = ase_optimizer_cls(optimizer)
        self.nn_name = nn_name
        self.scalar_pressure = 0.0

        structure = Structure.as_structure(atoms)

        # Get pseudos and ecut
        pseudos = PseudoTable.as_table(pseudos).get_pseudos_for_structure(structure)
        pp_paths = [p.filepath for p in pseudos]

        hints = [p.hint_for_accuracy("normal") for p in pseudos]
        ecut = max(h.ecut for h in hints) * 27.3  # In ASE this is in eV (don't know why!)
        #pawecutdg = max(h.pawecutdg for h in hints) if pseudos.allpaw else None

        # TODO: Automatic K-point sampling.
        import pymatgen.io.abinit.abiobjects as aobj
        kmesh = aobj.KSampling.automatic_density(structure, kppa, chksymbreak=0).to_abivars()
        #print("kmesh", kmesh)

        self.gs_kwargs = dict(
            ecut=ecut,
            # Smoothing PW cutoff energy (mandatory for cell optimization)
            ecutsm=0.5 if self.relax_mode == "cell" else 0,
            tolvrs=1e-8,
            #kpts=[4, 4, 4],
            expert_user=1,   # Ignore warnings (chksymbreak, chksymtnons, chkdilatmx)
            autoparal=1,
            paral_kgb=1,
            rmm_diis=1 if all(p.isnc for p in pseudos) else 0,
            nstep=100,
            prtwf=0,
            pseudos=pp_paths,
            **kmesh,
        )

        # Run fully ab-initio relaxation with abinit.
        # TODO: Fix issue with ixc set by ASE.
        self.relax_kwargs = dict(
            #ecutsm=0.5,     # Smoothing PW cutoff energy (mandatory for cell optimization)
            ionmov=2,
            #ionmov=22,
            #ionmov=28,     # activate i-pi/socket mode
            optcell=0 if self.relax_mode == "ions" else 2,
            tolmxf=self.fmax * eV_Ha * Ang_Bohr,
            ntime=200,
        )
        self.relax_kwargs.update(**self.gs_kwargs)

        argv = f"{mpi_runner} -n {mpi_nprocs} abinit".split()
        self.abinit_profile = AbinitProfile(argv)

    #def __str__(self):
    #    return self.to_string()
    #def to_string(self, verbose=0) -> str:

    def _mkfilter(self, atoms: Atoms):
        if self.relax_mode == "ions":
            return atoms
        elif self.relax_mode == "cell":
            return ExpCellFilter(atoms, scalar_pressure=self.scalar_pressure)

        raise ValueError(f"Invalid value of {self.relax_mode=}")

    def ml_relax_opt(self, directory):
        """
        Relax structure with ML potential only. Return ASE optimizer.
        """
        print(f"\nBegin {self.nn_name} relaxation in {str(directory)}")
        print("relax_mode:", self.relax_mode, "with fmax:", self.fmax)
        directory.mkdir()
        ml_calc = CalcBuilder(self.nn_name).get_calculator()
        atoms = self.initial_atoms.copy()
        atoms.calc = ml_calc

        opt_kws = dict(
            trajectory=str(directory / f"opt.traj"),
            #logfile=str(directory / f"log"),
        )
        opt = self.ase_opt_cls(self._mkfilter(atoms), **opt_kws)

        with Timer() as timer:
            opt.run(fmax=self.fmax, steps=self.steps)
            if not opt.converged():
                raise RuntimeError("ml_relax_opt didn't converge!")
        print('%s relaxation completed in %.2f sec after nsteps: %d\n' % (self.nn_name, timer.time, opt.nsteps))

        return opt

    def abi_relax_atoms(self, directory, atoms=None, header="Begin ABINIT relaxation"):
        """
        Relax structure with ABINIT. Return namedtuple with results.
        """
        print(f"\n{header} in {str(directory)}")
        print("relax_mode:", self.relax_mode, "with tolmxf:", self.relax_kwargs["tolmxf"])
        if atoms is None:
            atoms = self.initial_atoms.copy()

        abinit = Abinit(profile=self.abinit_profile, directory=directory, **self.relax_kwargs)
        atoms.calc = abinit
        with Timer() as timer:
            forces = atoms.get_forces()

        with HistFile(abinit.directory / "abinito_HIST.nc") as hist:
            nsteps = hist.num_steps
            atoms = get_atoms(hist.final_structure)
        print('ABINIT relaxation completed in %.2f sec after nsteps: %d\n' % (timer.time, nsteps))

        data = dict2namedtuple(
                atoms=atoms,
                fmax=np.sqrt((forces ** 2).sum(axis=1).max()),
                nsteps=nsteps,
               )
        return data

    def abi_relax_atoms_with_ase(self, directory, header="Begin ABINIT+ASE relaxation"):
        """
        Relax structure with ABINIT. Return namedtuple with results.
        """
        print(f"\n{header} in {str(directory)}")
        print("relax_mode:", self.relax_mode, "with tolmxf:", self.relax_kwargs["tolmxf"])

        atoms = self.initial_atoms.copy()
        abinit = Abinit(profile=self.abinit_profile, directory=directory, **self.gs_kwargs)
        atoms.calc = abinit

        opt = self.ase_opt_cls(self._mkfilter(atoms))
        with Timer() as timer:
            opt.run(fmax=self.fmax, steps=self.steps)
            if not opt.converged():
                raise RuntimeError("Abinit+ASE opt didn't converge!")

        print('%s relaxation completed in %.2f sec after nsteps: %d\n' % (self.nn_name, timer.time, opt.nsteps))

        return opt

    def abinit_run_gs_atoms(self, directory, atoms):
        """
        Perform a GS calculation with ABINIT. Return namedtuple with results.
        """
        with Timer() as timer:
            print(f"\nBegin ABINIT GS in {str(directory)}")
            abinit = Abinit(profile=self.abinit_profile, directory=directory, **self.gs_kwargs)
            #abinit.use_cache = False # This one seems to be needed to get updated forces but don't know why!!
            forces = abinit.get_forces(atoms=atoms)
            #abinit.use_cache = True
            stress = abinit.get_stress(atoms=atoms)
            #abinit.use_cache = False
            print('ABINIT GS completed in %.2f sec\n' % (timer.time))

        data = dict2namedtuple(abinit=abinit, forces=forces,
                               stress=voigt_6_to_full_3x3_stress(stress),
                               fmax=np.sqrt((forces ** 2).sum(axis=1).max()))
        return data

    def run(self, workdir=None, prefix=None):
        """
        Run the different steps of the bechmark.
        """
        workdir = workdir_with_prefix(workdir, prefix)

        # Run relaxation with ML potential.
        ml_opt = self.ml_relax_opt(workdir / "ml_relax")

        # Run fully ab-initio relaxation with abinit.
        abi_relax = self.abi_relax_atoms(workdir / "abinit_relax")

        # Run relaxation with ASE optimizer and Abinit forces.
        #abiase_opt = self.abi_relax_atoms_with_ase(workdir / f"abiase_relax")

        # Compare structures
        diff = StructDiff(["INITIAL", "ABINIT_RELAX", self.nn_name + "_RELAX"],
                          [self.initial_atoms, abi_relax.atoms, ml_opt.atoms])
        diff.tabulate()
        #raise RuntimeError()

        # Run hybrid relaxation (ML + abinit)
        ml_calc = CalcBuilder(self.nn_name).get_calculator()

        print(f"\nBegin ABINIT + {self.nn_name} hybrid relaxation")
        if self.xc.is_gga_family == "GGA":
            print(f"Starting from ML-optimized Atoms as {self.xc=}")
            atoms = ml_opt.atoms.copy()
            atoms = abisanitize_atoms(atoms)
        else:
            print(f"Starting from initial Atoms as {self.xc=}")
            atoms = self.initial_atoms.copy()

        count, abiml_nsteps, ml_nsteps = 0, 0, 0
        count_max = 10
        t_start = time.time()
        while count <= count_max:
            count += 1
            # Compute ab-initio forces and check for convergence.
            directory = workdir / f"abiml_gs_count_{count}"
            gs = self.abinit_run_gs_atoms(directory, atoms)
            abiml_nsteps += 1
            print("Iteration:", count, "abi_fmax:", gs.fmax, ", fmax:", self.fmax)
            if self.relax_mode == "cell":
                print("abinit_stress", full_3x3_to_voigt_6_stress(gs.stress))
            #print_atoms(atoms, cart_forces=gs.forces)

            # Compute ML forces and set delta forces in the ML calculator.
            ml_calc.set_delta_forces(None)
            ml_forces = ml_calc.get_forces(atoms=atoms)
            delta_forces = gs.forces - ml_forces #; delta_forces = None
            ml_calc.set_delta_forces(delta_forces)
            #print("delta_forces:\n", delta_forces)
            #write_forces(count, gs.forces, ml_forces)

            if self.relax_mode == "cell":
                ml_calc.set_delta_stress(None)
                ml_stress = ml_calc.get_stress(atoms=atoms)
                delta_stress = gs.stress - ml_stress
                ml_calc.set_delta_stress(delta_stress)
                print("delta_stress:\n", delta_stress)
                #write_stress(count, gs.stress, ml_stress)

            # Attach ML calculator with delta quantities to atoms.
            atoms.calc = ml_calc

            opt_kws = dict(
                trajectory=str(gs.abinit.directory / f"opt.traj"),
                #logfile=str(abinit.directory / f"log_{count}"),
            )
            opt = self.ase_opt_cls(self._mkfilter(atoms), **opt_kws)
            opt.run(fmax=self.fmax, steps=self.steps)
            atoms = opt.atoms.copy()
            atoms = abisanitize_atoms(atoms)
            opt_converged = opt.converged()
            ml_nsteps += opt.nsteps

            final_mlabi_relax = None
            if opt_converged and opt.nsteps <= 1:
                final_mlabi_relax = self.abi_relax_atoms(directory=workdir / "abiml_final_relax",
                                                         atoms=atoms,
                                                         header="Performing final structural relaxation with ABINIT",
                                                         )
                abiml_nsteps += final_mlabi_relax.nsteps
                break

        t_end = time.time() - t_start
        print(f'ABINIT + {self.nn_name} relaxation completed in {t_end:.2f} sec\n')
        #print_atoms(atoms, title="Atoms after ABINIT + ML relaxation:")

        #in final_mlabi_relax is None
        diff = StructDiff(["INITIAL", self.nn_name + "_RELAX", "ABINIT_RELAX", "ABI_ML"],
                          [self.initial_atoms, ml_opt.atoms, abi_relax.atoms, final_mlabi_relax.atoms])
        diff.tabulate()
        print(f"GS steps in ML mode {ml_nsteps=}")
        print(f"GS steps in ABINIT mode {abi_relax.nsteps=}")
        print(f"GS steps in ABI+ML mode {abiml_nsteps=}")

        # Write json file with output results.
        with open(workdir / "data.json", "wt") as fh:
            data = dict(
                xc=self.xc,
                gs_kwargs=self.gs_kwargs,
                relax_kwargs=self.relax_kwargs,
                ml_nsteps=ml_nsteps,
                abiml_nsteps=abiml_nsteps,
                abi_nsteps=abi_relax.nsteps,
                ml_relaxed_structure=Structure.as_structure(ml_opt.atoms),
                abi_relaxed_structure=Structure.as_structure(abi_relax.atoms),
                abiml_relaxed_structure=Structure.as_structure(final_mlabi_relax.atoms),
            )
            json.dump(data, fh, indent=4, cls=MontyEncoder)


if __name__ == "__main__":
    from abipy.flowtk.psrepos import get_repo_from_name
    xc = "GGA"
    # Get pseudos
    repo_name = {
        "PBE": "ONCVPSP-PBE-SR-PDv0.4",
        "PBEsol": "ONCVPSP-PBEsol-SR-PDv0.4",
        "LDA": "ONCVPSP-LDA-SR-PDv0.4",
    }[xc]
    print(f"Using {repo_name=}")
    pseudos = get_repo_from_name(repo_name).get_pseudos("standard")

    from ase.build import bulk
    atoms = bulk('Si')
    atoms.rattle(stdev=0.1, seed=42)
    kppa = 200
    prof = RelaxationProfiler(atoms, pseudos, xc, kppa, relax_mode="ions", fmax=0.001, mpi_nprocs=2, verbose=0)
    prof.run()
