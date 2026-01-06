import matplotlib.pyplot as plt
from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.io.vasp.outputs import BandStructure, Vasprun

# vasprun.xmlからバンド分散データを読み込む
vasprun = Vasprun("vasprun.xml")
band_structure: BandStructure = vasprun.get_band_structure()

# BandStructureインスタンスでプロッターを初期化する
plotter = BSPlotter(band_structure)

# フェルミエネルギーの上下20eVの範囲でバンド分散をプロットする
plot = plotter.get_plot(ylim=[-20, 20])

# フェルミレベルをプロットする
plt.axhline(0, color="black", linestyle="dotted")

plot.get_legend().remove()  # 凡例を削除
plt.xlabel("")  # x軸ラベル
plt.ylabel(r"$E - E_{\mathrm{Fermi}}$ (eV)", fontsize=32)  # y軸ラベル
plt.xticks(fontsize=18)  # x軸目盛り
plt.yticks(fontsize=18)  # y軸目盛り
plt.tight_layout()  # 余白を自動調節
plt.savefig("bands.pdf")  # バンド分散のプロットを'bands.pdf'にファイル出力する
plt.show()  # バンド分散のプロットを画面出力する
