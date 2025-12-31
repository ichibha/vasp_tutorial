import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
from ase.io import read

# vcrelaxのPOSCARを読み込み
atoms_vcrelax = read("POSCAR")

for scale in np.arange(0.95, 1.05 + 1e-8, 0.01):
    # 計算ディレクトリを作成
    calc_dir = Path(f"{scale:.2f}", "relax")
    os.makedirs(calc_dir, exist_ok=True)

    # 格子ベクトルをscale倍したatomsを作成、出力
    atoms = atoms_vcrelax.copy()
    atoms.set_cell(atoms_vcrelax.cell * scale, scale_atoms=True)
    atoms.write(calc_dir / "POSCAR")

    # 入力ファイルを作成
    shutil.copy("INCAR.relax", calc_dir / "INCAR")
    shutil.copy("POTCAR", calc_dir)
    subprocess.run("make-kpoints --gamma 6 6 4 > KPOINTS", shell=True, cwd=calc_dir)

    # vaspを実行
    print(f"- Running {calc_dir}")
    subprocess.run("mpirun vasp_std | tee vasp.out", shell=True, cwd=calc_dir)
