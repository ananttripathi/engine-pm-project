# Interim Submission – Engine Predictive Maintenance

## Files Ready for Submission

| File | Description |
|------|-------------|
| `AnantTripathi_EnginePredictiveMaintenance_Notebook.html` | Executed Python notebook in HTML format (required for verification) |
| `AnantTripathi_EnginePredictiveMaintenance_InterimReport.md` | Interim Report in Markdown |
| `AnantTripathi_EnginePredictiveMaintenance_InterimReport.html` | Interim Report in HTML (for PDF conversion) |
| `engine_data.csv` | Raw dataset (for reference) |

## How to Create the PDF Report

**Option 1 – Print to PDF (Recommended)**  
1. Open `AnantTripathi_EnginePredictiveMaintenance_InterimReport.html` in a browser (Chrome, Safari, etc.)  
2. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows)  
3. Choose **Save as PDF**  
4. Save as `AnantTripathi_EnginePredictiveMaintenance_InterimReport.pdf`

**Option 2 – Using Word/Google Docs**  
1. Open the `.md` or `.html` file  
2. Copy content into Word or Google Docs  
3. Format as needed and export to PDF  

**Option 3 – Using pandoc (if LaTeX installed)**  
```bash
pandoc AnantTripathi_EnginePredictiveMaintenance_InterimReport.md -o AnantTripathi_EnginePredictiveMaintenance_InterimReport.pdf
```

## Re-running the Notebook

To re-execute and re-export the notebook:

```bash
cd /Users/ananttripathi/Desktop/Interim_Submission
/opt/anaconda3/bin/jupyter nbconvert --to notebook --execute --inplace AnantTripathi_EnginePredictiveMaintenance_Notebook.ipynb
/opt/anaconda3/bin/jupyter nbconvert --to html --output AnantTripathi_EnginePredictiveMaintenance_Notebook.html AnantTripathi_EnginePredictiveMaintenance_Notebook.ipynb
```

## Checklist Before Submission

- [ ] PDF report created and named correctly  
- [ ] HTML notebook has all outputs visible  
- [ ] Both files submitted together  
- [ ] File naming: `AnantTripathi_EnginePredictiveMaintenance_InterimReport.pdf` and `AnantTripathi_EnginePredictiveMaintenance_Notebook.html`
