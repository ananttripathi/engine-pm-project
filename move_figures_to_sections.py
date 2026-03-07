#!/usr/bin/env python3
"""Move the EDA figure block from the end of the doc to the correct subsection positions."""
from docx import Document

DOCX_PATH = "AnantTripathi_EnginePredictiveMaintenance_InterimReport.docx"

def main():
    doc = Document(DOCX_PATH)
    body = doc.element.body
    children = list(body)

    # Find figure elements: captions (Figure N:) and following image paragraph
    figure_pairs = []  # list of (caption_elem, image_elem)
    i = 0
    while i < len(children):
        c = children[i]
        if c.tag.endswith("p"):
            t = "".join(x for x in c.itertext()).strip()
            if t.startswith("Figure ") and ":" in t:
                cap_elem = c
                img_elem = None
                if i + 1 < len(children) and children[i + 1].tag.endswith("p"):
                    nxt = children[i + 1]
                    if any("drawing" in d.tag for d in nxt.iter()):
                        img_elem = nxt
                        i += 1
                figure_pairs.append((cap_elem, img_elem))
        i += 1

    if len(figure_pairs) != 12:
        print("Expected 12 figure pairs, found", len(figure_pairs))
        return

    # Order: Fig1, Fig2 (univariate), Fig3-Fig7 (bivariate), Fig8-Fig12 (multivariate)
    # Current order in doc (from earlier output): Fig2, Fig1, Fig7, Fig6, Fig5, Fig4, Fig3, Fig12, Fig11, Fig10, Fig9, Fig8
    order_map = {
        "Figure 1:": 0, "Figure 2:": 1, "Figure 3:": 2, "Figure 4:": 3, "Figure 5:": 4,
        "Figure 6:": 5, "Figure 7:": 6, "Figure 8:": 7, "Figure 9:": 8, "Figure 10:": 9,
        "Figure 11:": 10, "Figure 12:": 11
    }
    ordered = [None] * 12
    for cap, img in figure_pairs:
        t = "".join(x for x in cap.itertext()).strip()
        for k, idx in order_map.items():
            if t.startswith(k):
                ordered[idx] = (cap, img)
                break

    univariate = ordered[0:2]   # Fig1, Fig2
    bivariate = ordered[2:7]    # Fig3-Fig7
    multivariate = ordered[7:12] # Fig8-Fig12

    # Remove all 24 elements from body (in reverse order)
    to_remove = []
    for cap, img in figure_pairs:
        to_remove.append(cap)
        if img is not None:
            to_remove.append(img)
    for elem in to_remove:
        body.remove(elem)

    # Find insert positions (after "Refer to notebook" for each subsection)
    body_new = list(body)
    idx_after_univariate = None
    idx_after_bivariate = None
    idx_after_multivariate = None
    for i, c in enumerate(body_new):
        if c.tag.endswith("p"):
            t = "".join(x for x in c.itertext())
            if "Refer to notebook" in t and "target bar" in t:
                idx_after_univariate = i + 1
            if "Refer to notebook" in t and "box plots" in t:
                idx_after_bivariate = i + 1
            if "Refer to notebook" in t and "correlation heatmap" in t:
                idx_after_multivariate = i + 1

    def insert_pair(body, index, cap, img):
        if img is not None:
            body.insert(index + 1, img)
        body.insert(index, cap)
        return 2 if img else 1

    # Insert univariate (Fig1, Fig2) at idx_after_univariate
    pos = idx_after_univariate
    for cap, img in univariate:
        insert_pair(body, pos, cap, img)
        pos += 2
    # After inserting 4 elements, bivariate and multivariate ref positions shift
    if idx_after_bivariate is not None and idx_after_bivariate >= idx_after_univariate:
        idx_after_bivariate += 4
    if idx_after_multivariate is not None and idx_after_multivariate >= idx_after_univariate:
        idx_after_multivariate += 4

    # Insert bivariate (Fig3-Fig7)
    pos = idx_after_bivariate
    for cap, img in bivariate:
        insert_pair(body, pos, cap, img)
        pos += 2
    if idx_after_multivariate is not None and idx_after_multivariate >= idx_after_bivariate:
        idx_after_multivariate += 10

    # Insert multivariate (Fig8-Fig12)
    pos = idx_after_multivariate
    for cap, img in multivariate:
        insert_pair(body, pos, cap, img)
        pos += 2

    doc.save(DOCX_PATH)
    print("Figures moved to correct sections. Saved:", DOCX_PATH)

if __name__ == "__main__":
    main()
