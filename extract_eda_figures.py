#!/usr/bin/env python3
"""Extract EDA figure images from the executed notebook and save to figures/."""
import json
import base64
import os

NOTEBOOK = "Engine_PM_Interim_Notebook.ipynb"
FIG_DIR = "figures"
# Order: (cell_index, list of figure filenames for that cell)
FIG_NAMES = [
    (20, ["fig1_target_distribution.png", "fig2_univariate_histograms.png"]),
    (23, ["fig3_boxplots.png", "fig4_violin_subset.png", "fig5_violin_all6.png", "fig6_strip_plots.png", "fig7_mean_bar_chart.png"]),
    (26, ["fig8_correlation_heatmap.png", "fig9_scatter_two.png", "fig10_scatter_2x2.png", "fig11_corr_bar.png", "fig12_pairplot.png"]),
]

def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    with open(NOTEBOOK) as f:
        nb = json.load(f)
    idx_in_cell = 0
    for cell_idx, filenames in FIG_NAMES:
        cell = nb["cells"][cell_idx]
        outputs = cell.get("outputs", [])
        img_count = 0
        for out in outputs:
            if out.get("output_type") != "display_data" or "data" not in out:
                continue
            if "image/png" not in out["data"]:
                continue
            if img_count >= len(filenames):
                break
            path = os.path.join(FIG_DIR, filenames[img_count])
            b64 = out["data"]["image/png"]
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
            print("Saved", path)
            img_count += 1
    print("Done.")

if __name__ == "__main__":
    main()
