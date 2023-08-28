import argparse


def parse_args():
    print("  \n~~~BEANQC~~~")
    print("-Check guide/sample level quality and mask / discard-")
    print(
        r"""
    _ _       
  /  \ '\        ___   ___ 
  |   \  \      / _ \ / __|
   \   \  |    | (_) | (__ 
    `.__|/      \__\_\\___|
    """
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bdata_path", help="Path to the ReporterScreen object to run QC on", type=str
    )
    parser.add_argument(
        "-o",
        "--out-screen-path",
        help="Path where quality-filtered ReporterScreen object to be written to",
        type=str,
    )
    parser.add_argument(
        "-r",
        "--out-report-prefix",
        help="Output prefix of qc report (prefix.html, prefix.ipynb)",
        type=str,
    )
    parser.add_argument(
        "--replicate-label",
        help="Label of column in `bdata.samples` that describes replicate ID.",
        type=str,
        default="rep",
    )
    parser.add_argument(
        "--condition-label",
        help="Label of column in `bdata.samples` that describes experimental condition. (sorting bin, time, etc.)",
        type=str,
        default="bin",
    )
    parser.add_argument(
        "--target-pos-col",
        help="Target position column in `bdata.guides` specifying target edit position in reporter",
        type=str,
        default="target_pos",
    )
    parser.add_argument(
        "--rel-pos-is-reporter",
        help="Specifies whether `edit_start_pos` and `edit_end_pos` are relative to reporter position. If `False`, those are relative to spacer position.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--edit-start-pos",
        help="Edit start position to quantify editing rate on, 0-based inclusive.",
        default=2,
    )
    parser.add_argument(
        "--edit-end-pos",
        help="Edit end position to quantify editing rate on, 0-based exclusive.",
        default=7,
    )
    parser.add_argument(
        "--count-correlation-thres",
        help="Correlation threshold to mask out.",
        type=float,
        default=0.8,
    )
    parser.add_argument(
        "--edit-rate-thres",
        help="Median editing rate threshold per sample to mask out.",
        type=float,
        default=0.1,
    )
    parser.add_argument(
        "--posctrl-col",
        help="Column name in .h5ad.guides DataFrame that specifies guide category.",
        type=str,
        default="target_group",
    )
    parser.add_argument(
        "--posctrl-val",
        help="Value in .h5ad.guides[`posctrl_col`] that specifies guide will be used as the positive control in calculating log fold change.",
        type=str,
        default="PosCtrl",
    )
    parser.add_argument(
        "--lfc-thres",
        help="Positive guides' correlation threshold to filter out.",
        type=float,
        default=-0.1,
    )
    args = parser.parse_args()
    if args.out_screen_path is None:
        args.out_screen_path = f"{args.bdata_path.rsplit('.h5ad', 1)[0]}.filtered.h5ad"
    if args.out_report_prefix is None:
        args.out_report_prefix = f"{args.bdata_path.rsplit('.h5ad', 1)[0]}.qc_report"
    return args
