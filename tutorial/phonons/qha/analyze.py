#!/usr/bin/env python3
import subprocess
from os import PathLike


def main():
    analyze_harmonic(
        mesh="16 16 16",
        band_options="0 0 0   0 0 1/2   1/3 1/3 1/2   1/3 1/3 0   1/2 0 1/2   1/2 0 0",
        band_labels=r"$\Gamma$ A H K L M",
    )


def analyze_harmonic(
    mesh: str,
    band_options: str,
    band_labels: str,
    sigma: float = 0.1,
    directory: PathLike | None = None,
):
    dos_options = f"--mesh {mesh} --sigma {sigma}"
    band_options = f"--band {band_options} --band_labels {band_labels}"

    run(f"-ps {dos_options}", directory=directory)
    run(f"-ps {band_options}", directory=directory)
    run(f"-ps {band_options} {dos_options}", directory=directory)
    run(f"-tps {dos_options}", directory=directory)
    run(f"-p {dos_options} --fits-debye-model", directory=directory)


def run(_args: str, directory: PathLike | None = None):
    subprocess.run(f"phonopy-load {_args}", shell=True, cwd=directory)


if __name__ == "__main__":
    main()
