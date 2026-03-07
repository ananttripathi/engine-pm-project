# Update your Hugging Face Space with the latest app

The Space is still showing old defaults (700, 3.0, 6.0...) because the deploy job in GitHub Actions may have failed (e.g. no HF_TOKEN in Secrets). To push the current app (new defaults + Suggested focus fix) to the Space:

## Option A: Run deploy script locally (fastest)

1. Get your Hugging Face token: https://huggingface.co/settings/tokens (read + write).

2. In a terminal, from the project root:

```bash
cd /Users/ananttripathi/Desktop/Interim_Submission
export HF_TOKEN="your_token_here"
python engine_pm_project/deployment/deploy_to_hf_spaces.py
```

3. Wait 1–2 minutes for the Space to rebuild, then open the Space and hard-refresh (Cmd+Shift+R). Defaults should show **1437**, **1.9**, **3.8**, **3.8**, **77.5**, **79.8**.

## Option B: Fix GitHub Actions so future pushes auto-update the Space

1. In GitHub: **Settings → Secrets and variables → Actions**.
2. Add (or fix) **HF_TOKEN** with your Hugging Face token (same as above).
3. Re-run the workflow: **Actions → ML Pipeline - Engine Predictive Maintenance → Run workflow**.
4. Open the **deploy-hosting** job log and confirm you see `Uploaded app.py` and `Done. Open: https://huggingface.co/spaces/...`.

After that, every push to `main` will update the Space.
