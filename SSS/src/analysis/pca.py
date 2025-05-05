import matplotlib.pyplot as plt
from dscribe.descriptors import SOAP
from sklearn.decomposition import PCA
from src.utils import load_structures, make_output_dir, grid_select
from ase.io import write


def run(args):
    for split in sorted(__import__("glob").glob("split_*.xyz")):
        structures = load_structures(split)
        soap = SOAP(
            species={a.symbol for fr in structures for a in fr},
            periodic=True,
            r_cut=7.0,
            n_max=8,
            l_max=8,
            average="inner",
            sparse=False,
        )
        feats = soap.create(structures, n_jobs=-1)
        proj = PCA(n_components=2).fit_transform(feats)
        sel = grid_select(proj, args.grid_division, args.seed)

        out = make_output_dir("selected_data_pca", split[:-4])
        write(f"{out}/pca_selection.xyz", [structures[i] for i in sel])
        plt.figure(figsize=(10, 6))
        plt.scatter(proj[:, 0], proj[:, 1], alpha=0.3)
        plt.scatter(proj[sel, 0], proj[sel, 1], alpha=0.7)
        plt.savefig(f"{out}/pca_plot.png", dpi=300)
        print(f"[PCA] {split} → {len(sel)} frames → {out}")
