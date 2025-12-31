from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.io.vasp import Vasprun

# matplotlib settings
plt.rcParams["font.size"] = 18
plt.rcParams["figure.titlesize"] = 18
plt.rcParams["axes.labelsize"] = 18
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14
plt.rcParams["legend.fontsize"] = 14
plt.rcParams["figure.autolayout"] = True
plt.rcParams["axes.formatter.useoffset"] = False


# 体積とエネルギーを取得
volumes, energies = [], []
for scale in np.arange(0.95, 1.05 + 1e-8, 0.01):
    vasprun = Vasprun(Path(f"{scale:.2f}", "relax", "vasprun.xml"))
    volumes.append(vasprun.final_structure.volume)
    energies.append(vasprun.final_energy)

# 体積とエネルギーの数値データを出力
lines = ["# Volume(A^3) Energy(eV)\n"]
lines += [f"{volume:.6f} {energy:.6f}\n" for volume, energy in zip(volumes, energies)]
with open("e-v.dat", "w") as fout:
    fout.writelines(lines)

# 体積とエネルギーのプロットを出力
plt.plot(volumes, energies)
plt.xlabel("Volume ($\mathrm{\AA^3}$)")
plt.ylabel("Total energy (eV)")
plt.savefig("e-v.pdf")
plt.close()
