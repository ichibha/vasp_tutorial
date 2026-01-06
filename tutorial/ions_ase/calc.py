import os
import shutil
from pathlib import Path

from ase.calculators.vasp import Vasp
from ase.io import read
from pymatgen.io.vasp import Vasprun

atoms = read(Path("~/vasp_tutorial/str/sio2_mp6930.vasp").expanduser())
scf_dir = Path("~/vasp_tutorial/electrons_ase/scf").expanduser()
relax_dir = Path("relax")
vcrelax_dir = Path("vcrelax")


def main():
    # relax
    os.makedirs(relax_dir, exist_ok=True)
    shutil.copy(scf_dir / "WAVECAR", relax_dir)
    run_vasp(relax_dir)

    # vcrelax
    os.makedirs(vcrelax_dir, exist_ok=True)
    shutil.copy(relax_dir / "CONTCAR", vcrelax_dir / "POSCAR")
    shutil.copy(relax_dir / "WAVECAR", vcrelax_dir)
    run_vasp(vcrelax_dir)


def run_vasp(directory: Path):
    if is_converged(directory):
        return

    if directory == relax_dir:
        isif = 2
    elif directory == vcrelax_dir:
        isif = 3
    else:
        raise ValueError(f"Invalid directory value: {directory}")

    atoms.calc = Vasp(
        # ase
        directory=directory,
        # functional
        gga="PE",
        # pseudopotentials
        pp="PBE",
        setups=dict(Si="", O=""),
        # cutoff energy
        encut=520,
        # k-mesh
        kspacing=0.3,
        # smearing
        ismear=0,
        sigma=0.03,
        # scf
        prec="Accurate",
        ediff=1e-6,
        nelm=120,
        # ions
        isif=isif,
        ibrion=1,
        ediffg=-1e-2,
        nsw=200,
    )
    atoms.get_potential_energy()


def is_converged(directory: Path):
    vasprun_path = directory / "vasprun.xml"
    if not vasprun_path.exists():
        return False
    try:
        return Vasprun(vasprun_path).converged
    except:
        return False


if __name__ == "__main__":
    main()
