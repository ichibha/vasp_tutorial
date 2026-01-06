import subprocess
from os import PathLike
from pathlib import Path

import numpy as np


def main():
    for scale in np.arange(0.95, 1.05 + 1e-8, 0.01):
        root_dir = Path(f"scale_{scale:.2f}")
        analyze_harmonic(
            mesh="16 16 16",
            band="0 0 0   0 0 1/2   1/3 1/3 1/2   1/3 1/3 0   1/2 0 1/2   1/2 0 0",
            band_labels=r"$\Gamma$ A H K L M",
            directory=root_dir,
        )


def analyze_harmonic(
    mesh: str,
    band: str,
    band_labels: str,
    sigma: float = 0.1,
    directory: PathLike | None = None,
):
    dos_options = f"--mesh {mesh} --sigma {sigma}"
    band_options = f"--band {band} --band-labels {band_labels}"

    run("-f FC2-*/vasprun.xml", directory=directory)
    run(f"-ps {band_options} {dos_options}", directory=directory)
    run(f"-tps {dos_options}", directory=directory)


def run(_args: str, directory: PathLike | None = None):
    subprocess.run(f"phonopy-load {_args}", shell=True, cwd=directory)


if __name__ == "__main__":
    main()
