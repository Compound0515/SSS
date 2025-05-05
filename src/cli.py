import argparse
from src import split
from src.analysis import pca, umap, tsne


def main():
    parser = argparse.ArgumentParser(
        prog="soap_screen",
        description="Compute SOAP-based projections and select representative frames",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Split subcommand
    sp = sub.add_parser("split", help="Split XYZ trajectory into chunks")
    sp.add_argument("input_file", help="Path to .xyz trajectory")
    sp.add_argument(
        "-n",
        "--frames-per-file",
        type=int,
        default=10000,
        help="Number of frames per split",
    )

    # Analysis subcommands
    for cmd_name, module in [("pca", pca), ("umap", umap), ("tsne", tsne)]:
        ap = sub.add_parser(cmd_name, help=f"Run {cmd_name.upper()} analysis")
        ap.add_argument(
            "-a",
            "--cell-params",
            nargs=6,
            type=float,
            required=True,
            metavar=("a", "b", "c", "alpha", "beta", "gamma"),
            help="Lattice params: a b c α β γ",
        )
        ap.add_argument(
            "-p",
            "--pbc",
            nargs=3,
            type=int,
            choices=[0, 1],
            required=True,
            metavar=("Px", "Py", "Pz"),
            help="Periodic boundary flags (0/1)",
        )
        ap.add_argument(
            "-g",
            "--grid-division",
            type=int,
            default=20,
            help="Grid divisions per axis",
        )
        ap.add_argument("-s", "--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    if args.command == "split":
        split.run(args.input_file, args.frames_per_file)
    else:
        module = {"pca": pca, "umap": umap, "tsne": tsne}[args.command]
        module.run(args)
