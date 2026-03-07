#!/usr/bin/env python3
"""Fix docx report: reorder body so Section 4 and 5 are not mixed into Section 3."""
from docx import Document

DOCX_PATH = "AnantTripathi_EnginePredictiveMaintenance_InterimReport.docx"

def get_text(elem):
    if elem.tag.endswith("p"):
        return "".join(x for x in elem.itertext()).strip()
    return ""

def section_of(elem, idx, children):
    t = get_text(elem)
    if elem.tag.endswith("tbl"):
        # Associate table with preceding section
        for i in range(idx - 1, -1, -1):
            if children[i].tag.endswith("p"):
                pt = get_text(children[i])
                if "5.5 Confusion" in pt:
                    return "sec5"
                if "5.4 Classification" in pt:
                    return "sec5"
                if "5.3 Model Performance" in pt:
                    return "sec5"
                if "5.2 Best" in pt:
                    return "sec5"
                if "4.2 Results" in pt:
                    return "sec4"
                break
        return "sec5"
    if "Interim Project" in t or "Engine Predictive" in t or "Learner Name" in t or (t == "" and idx < 31):
        return "title"
    if t.startswith("1. Executive") or (idx == 9 and "interim report" in t):
        return "sec1"
    if "2. Data Registration" in t or "2.1" in t or "2.2" in t or "2.3" in t or "master folder" in t.lower() or "engine_maintenance_project" in t or "Centralized data" in t:
        return "sec2"
    if "3. Exploratory" in t or "3.1" in t or "3.2" in t or "3.3" in t or "3.4" in t or "3.5" in t or "3.6" in t:
        return "sec3"
    if "Data Collection" in t or "Data Overview" in t or "Univariate" in t or "Bivariate" in t or "Multivariate" in t:
        return "sec3"
    if "Target distribution" in t or "Feature distributions" in t or "Observation:" in t and "skewness" in t:
        return "sec3"
    if "Refer to notebook" in t or t.startswith("Figure "):
        return "sec3"
    if "Box plots:" in t or "Violin plots:" in t or "Strip plots:" in t or "Grouped bar" in t or "Mean table:" in t or "Business insight:" in t:
        return "sec3"
    if "Correlation matrix:" in t or "Scatter plots" in t or "Feature–target" in t or "Pair plot:" in t:
        return "sec3"
    if "Observation:" in t and "higher correlation" in t:
        return "sec3"
    if "1. Data quality" in t or "2. Target balance" in t or "3. Univariate" in t or "4. Bivariate" in t or "5. Multivariate" in t or "6. Recommendations" in t:
        return "sec3"
    if "4. Data Preparation" in t or "4.1" in t or "4.2" in t or "4.3" in t or "Load data from Hugging" in t or "Clean:" in t or "Split:" in t or "Save locally" in t or "Train and test" in t or "Proper data preparation" in t:
        return "sec4"
    if "5. Model Building" in t or "5.1" in t or "5.2" in t or "5.3" in t or "5.4" in t or "5.5" in t or "5.6" in t:
        return "sec5"
    if "Algorithm:" in t or "Preprocessing:" in t or "Hyperparameter" in t or "Experiment Tracking" in t or "Model Registry" in t:
        return "sec5"
    if "Recall for Maintenance" in t or "Precision for Maintenance" in t or "ROC-AUC" in t and "0.70" in t:
        return "sec5"
    if "6. Conclusion" in t:
        return "sec6"
    if "The interim pipeline" in t and "Data Registration" in t:
        return "sec6"
    if "The model achieves" in t and "F1-score" in t:
        return "sec6"
    if "Appendix" in t or "Raw code" in t or "Page 1 of 1" in t:
        return "appendix"
    # bookmarks and empty paras: keep with neighbors by index ranges
    return "other"

def main():
    doc = Document(DOCX_PATH)
    body = doc.element.body
    children = list(body)
    n = len(children)
    section_order = ["title", "sec1", "sec2", "sec3", "sec4", "sec5", "sec6", "appendix", "other"]
    # Assign section to each; for "other" use the section of the next non-other
    sec = []
    for i in range(n):
        s = section_of(children[i], i, children)
        sec.append(s)
    # Resolve "other": assign to same as next non-other, or previous
    for i in range(n):
        if sec[i] == "other":
            for j in range(i + 1, n):
                if sec[j] != "other":
                    sec[i] = sec[j]
                    break
            else:
                for j in range(i - 1, -1, -1):
                    if sec[j] != "other":
                        sec[i] = sec[j]
                        break
    # Within sec5 we need correct order: 5. Model Building, 5.1, methodology content, 5.2+table, 5.3+table, 5.4+table, 5.5+table, 5.6+content
    # Build ordered index list: sort by (section_rank, then by a custom order within sec5)
    def sort_key(i):
        s = sec[i]
        rank = section_order.index(s) if s in section_order else 99
        t = get_text(children[i])
        # Within sec5, order by: 5. (125), 5.1 (124), then methodology (122,117,120,121,119,118,106), 5.2 (83), tbl, 5.3 (79), tbl, 5.4 (56), tbl, 5.5 (44), tbl, 5.6 (95), 93,96,97
        if s == "sec5":
            if "5. Model Building" in t:
                return (rank, 0)
            if "5.1 Methodology" in t:
                return (rank, 1)
            if "Preprocessing:" in t:
                return (rank, 2)
            if "Algorithm:" in t:
                return (rank, 3)
            if "Hyperparameter Tuning" in t:
                return (rank, 4)
            if "Experiment Tracking" in t:
                return (rank, 5)
            if "Model Registry" in t:
                return (rank, 6)
            if "Hyperparameter Search" in t:
                return (rank, 7)
            if "5.2 Best" in t:
                return (rank, 8)
            if "5.3 Model" in t:
                return (rank, 10)
            if "5.4 Classification" in t:
                return (rank, 12)
            if "5.5 Confusion" in t:
                return (rank, 14)
            if "5.6 Business" in t:
                return (rank, 16)
            if "Precision for" in t or "ROC-AUC" in t or "Recall for" in t:
                return (rank, 17)
            if children[i].tag.endswith("tbl"):
                return (rank, 9.5)  # table after 5.2
            return (rank, 15)
        return (rank, i)
    ordered_indices = sorted(range(n), key=sort_key)
    # Tables need to be placed correctly - check: after 5.2 comes one table, after 5.3 one, after 5.4 one, after 5.5 one
    # Current sort_key puts all sec5 tables at 9.5. We need to distinguish. Use preceding paragraph.
    # Re-do sec5 order by explicit sequence of indices (from current body)
    sec5_indices = [i for i in range(n) if sec[i] == "sec5"]
    # Desired sec5 order (by content): 125, 124, 122, 117, 120, 121, 119, 118, 106, 83, 86, 79, 82, 56, 58, 44, 46, 95, 93, 94, 96, 97
    sec5_order = []
    for i in sec5_indices:
        t = get_text(children[i])
        if "5. Model Building" in t:
            sec5_order.append((i, 0))
        elif "5.1 Methodology" in t:
            sec5_order.append((i, 1))
        elif "Preprocessing:" in t:
            sec5_order.append((i, 2))
        elif "Algorithm:" in t:
            sec5_order.append((i, 3))
        elif "Hyperparameter Tuning" in t:
            sec5_order.append((i, 4))
        elif "Experiment Tracking" in t:
            sec5_order.append((i, 5))
        elif "Model Registry" in t:
            sec5_order.append((i, 6))
        elif "Hyperparameter Search" in t:
            sec5_order.append((i, 7))
        elif "5.2 Best" in t:
            sec5_order.append((i, 8))
        elif "5.3 Model" in t:
            sec5_order.append((i, 10))
        elif "5.4 Classification" in t:
            sec5_order.append((i, 12))
        elif "5.5 Confusion" in t:
            sec5_order.append((i, 14))
        elif "5.6 Business" in t:
            sec5_order.append((i, 16))
        elif "Precision" in t or "ROC-AUC" in t or "Recall" in t:
            sec5_order.append((i, 17))
        elif children[i].tag.endswith("tbl"):
            # Which table: look at position in original - 46 is after 5.5, 58 after 5.4, 82 after 5.3, 86 after 5.2
            sec5_order.append((i, 9 if i in (84, 85, 86) else 11 if i in (80, 81, 82) else 13 if i in (57, 58) else 15 if i in (45, 46) else 9))
        else:
            sec5_order.append((i, 18))
    sec5_order.sort(key=lambda x: x[1])
    sec5_indices_ordered = [x[0] for x in sec5_order]
    # Build full ordered list
    other_indices = [i for i in range(n) if sec[i] == "other" and i not in [x[0] for x in sec5_order]]
    # We need: title block (0-30), sec3 (31-42, 43, 47-55, 59-76, 88-89, 98-116, 126-128, 136-141), sec4 (143-160), sec5 (ordered), sec6 (78, 90, 133), appendix (129, 130, 132), then remaining other, sectPr
    sec3_indices = [i for i in range(n) if sec[i] == "sec3"]
    sec4_indices = [i for i in range(n) if sec[i] == "sec4"]
    sec6_indices = [i for i in range(n) if sec[i] == "sec6"]
    appendix_indices = [i for i in range(n) if sec[i] == "appendix"]
    title_indices = [i for i in range(n) if sec[i] == "title"]
    sec1_indices = [i for i in range(n) if sec[i] == "sec1"]
    sec2_indices = [i for i in range(n) if sec[i] == "sec2"]
    # Preserve relative order within sec3, sec4, sec6, appendix, title, sec1, sec2
    def by_original_order(lst):
        return sorted(lst)
    new_order = (by_original_order(title_indices) + by_original_order(sec1_indices) + by_original_order(sec2_indices) +
                 by_original_order(sec3_indices) + by_original_order(sec4_indices) + sec5_indices_ordered +
                 by_original_order(sec6_indices) + by_original_order(appendix_indices) + by_original_order(other_indices))
    # Add any remaining (e.g. sectPr) - elements not yet in new_order
    for i in range(n):
        if i not in new_order:
            new_order.append(i)
    # Remove all from body, then add in new_order
    for child in list(body):
        body.remove(child)
    for i in new_order:
        body.append(children[i])
    doc.save(DOCX_PATH)
    print("Reordered", n, "elements. Saved:", DOCX_PATH)

if __name__ == "__main__":
    main()
