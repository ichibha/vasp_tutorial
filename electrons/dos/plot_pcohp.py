#!/usr/bin/env python3
from itertools import product

import matplotlib.pyplot as plt
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter


def drawCohp(completeCohp: CompleteCohp, index: int):
    # 指標を文字列に変換する
    index: str = str(index)

    # Si-3sとO-2sのCOHPを取得する
    cohp_3s_2s = completeCohp.get_orbital_resolved_cohp(index, "3s-2s")

    # Si-3sとO-2pのCOHPを取得する
    cohp_3s_2p = completeCohp.get_summed_cohp_by_label_and_orbital_list(
        [index] * 3, [f"3s-2p{c}" for c in ["x", "y", "z"]]
    )
    # Si-3pとO-2sのCOHPを取得する
    cohp_3p_2s = completeCohp.get_summed_cohp_by_label_and_orbital_list(
        [index] * 3, [f"3p{c}-2s" for c in ["x", "y", "z"]]
    )
    # Si-3pとO-2pのCOHPを取得する
    cohp_3p_2p = completeCohp.get_summed_cohp_by_label_and_orbital_list(
        [index] * 9, [f"3p{c1}-2p{c2}" for c1, c2 in product(["x", "y", "z"], repeat=2)]
    )

    # CohpPlotterを初期化する
    plotter = CohpPlotter()

    # プロッタにCOHPを追加する
    plotter.add_cohp(label=f"Si-3s and O-2s", cohp=cohp_3s_2s)
    plotter.add_cohp(label=f"Si-3s and O-2p", cohp=cohp_3s_2p)
    plotter.add_cohp(label=f"Si-3p and O-2s", cohp=cohp_3p_2s)
    plotter.add_cohp(label=f"Si-3p and O-2p", cohp=cohp_3p_2p)

    # COHPをプロットする
    plotter.get_plot()

    # データの種類に応じてxラベルと図名を変更する
    if completeCohp.are_coops:
        xlabel = "$-$COOP"
        figure_name = "pcoop.pdf"
    elif completeCohp.are_cobis:
        xlabel = "$-$COBI"
        figure_name = "pcobi.pdf"
    else:
        xlabel = "$-$COHP"
        figure_name = "pcohp.pdf"

    plt.xlabel(xlabel, fontsize=32)
    plt.ylabel(r"$E - E_{\mathrm{Fermi}}$ (eV)", fontsize=32)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.tight_layout()
    plt.savefig(figure_name)
    plt.show()
    plt.close()


# COHPを読み込む
completeCohp = CompleteCohp.from_file(
    fmt="LOBSTER",
    filename="COHPCAR.lobster",
    structure_file="POSCAR",
)

# COOPを読み込む
completeCoop = CompleteCohp.from_file(
    fmt="LOBSTER",
    filename="COOPCAR.lobster",
    structure_file="POSCAR",
    are_coops=True,
)

# COBIを読み込む
completeCobi = CompleteCohp.from_file(
    fmt="LOBSTER",
    filename="COBICAR.lobster",
    structure_file="POSCAR",
    are_cobis=True,
)

drawCohp(completeCohp, 1)  # 1番目の結合のCOHPを描画
drawCohp(completeCoop, 1)  # 1番目の結合のCOOPを描画
drawCohp(completeCobi, 1)  # 1番目の結合のCOBIを描画
