import os
import shutil
import subprocess
from pathlib import Path

import numpy as np

for scale in np.arange(0.95, 1.05 + 1e-8, 0.01):
    # 変位構造を生成
    root_dir = Path(f"scale_{scale:.2f}")
    shutil.copy(root_dir / "relax" / "CONTCAR", root_dir / "POSCAR")
    subprocess.run("phonopy -d --dim 3 3 2 --nac", shell=True, cwd=root_dir)

    # 変位構造の力場を計算
    for poscar_path in root_dir.glob("POSCAR-*"):
        calc_dir = poscar_path.with_name(poscar_path.name.replace("POSCAR", "FC2"))
        os.makedirs(calc_dir, exist_ok=True)
        shutil.copy(poscar_path, calc_dir / "POSCAR")
        shutil.copy("INCAR.fixed", calc_dir / "INCAR")
        shutil.copy("POTCAR", calc_dir)
        subprocess.run("make-kpoints --gamma 2 2 2 > KPOINTS", shell=True, cwd=calc_dir)
        subprocess.run("mpirun vasp_std | tee vasp.out", shell=True, cwd=calc_dir)
