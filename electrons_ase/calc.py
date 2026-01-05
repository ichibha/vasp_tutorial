import os
import shutil
from pathlib import Path

from ase.calculators.vasp import Vasp
from ase.io import read
from pymatgen.io.vasp import Vasprun

atoms = read(Path("~/vasp_tutorial/str/sio2_mp6930.vasp").expanduser())
scf_dir = Path("scf")
resume_dir = Path("resume")
dos_dir = Path("dos")
bands_dir = Path("bands")
dielectric_dir = Path("dielectric")


def main():
    # scf
    run_vasp(scf_dir)

    # resume
    os.makedirs(resume_dir, exist_ok=True)
    shutil.copy(scf_dir / "WAVECAR", resume_dir)
    run_vasp(resume_dir)

    # dos
    os.makedirs(dos_dir, exist_ok=True)
    shutil.copy(scf_dir / "CHGCAR", dos_dir)
    run_vasp(dos_dir)

    # bands
    os.makedirs(bands_dir, exist_ok=True)
    shutil.copy("KPOINTS.bands", bands_dir / "KPOINTS")
    shutil.copy(scf_dir / "CHGCAR", bands_dir)
    run_vasp(bands_dir)

    # dielectric
    os.makedirs(dielectric_dir, exist_ok=True)
    shutil.copy(scf_dir / "WAVECAR", dielectric_dir)
    run_vasp(dielectric_dir)


def run_vasp(directory: Path):
    if is_converged(directory):
        return

    if directory in (dos_dir):
        kspacing = 0.15
    else:
        kspacing = 0.30

    if directory in (dos_dir):
        smear = dict(ismear=-5, sigma=None)
    else:
        smear = dict(ismear=0, sigma=0.03)

    if directory in (dos_dir, bands_dir):
        isym = 0
        icharg = 11
    else:
        isym = None
        icharg = None

    if directory in (dos_dir):
        dos = dict(lorbit=11, emin=-20, emax=20, nedos=2000)
    else:
        dos = dict()

    if directory in (dielectric_dir):
        dielectric = dict(lepsilon=True)
    else:
        dielectric = dict()

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
        kspacing=kspacing,
        # smearing
        **smear,
        # scf
        prec="Accurate",
        ediff=1e-6,
        nelm=120,
        isym=isym,
        icharg=icharg,
        # dos
        **dos,
        # dielectric
        **dielectric
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
