# TruthLens V5 — AI activation and repeatable case inference

## What's new
Existing cases now show an **AI Model / Inference Control** section. After installing a trusted model, you can rerun image/video AI inference on previously uploaded evidence without reuploading. Image analysis preserves forensic metadata and heatmaps; video analysis recomputes frame samples. No model is bundled.

## Windows PowerShell (Python 3.12)

```powershell
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt --index-url https://pypi.org/simple --timeout 60 --retries 10
.\venv\Scripts\python.exe -m pip install -r requirements-ai.txt --index-url https://pypi.org/simple --timeout 60 --retries 10
.\venv\Scripts\python.exe manage.py migrate
$env:TRUTHLENS_IMAGE_MODEL = 'PATH_OR_HF_ID_OF_YOUR_VERIFIED_IMAGE_CLASSIFIER'
.\venv\Scripts\python.exe manage.py runserver
```

The model setting above is a placeholder: replace it with a real, trusted Hugging Face **image-classification** checkpoint trained for real/synthetic image classification, or a local model directory. Verify model licensing, intended task, class labels and benchmarks. Initial download requires network and may take time. For offline demo, predownload and set the local model directory. Never set `trust_remote_code=True` for an untrusted checkpoint.

Visit an existing case, then select **Run AI on existing evidence**. Inspect model errors and scores under the evidence panel. Scores are uncalibrated classifier outputs, not proof of authenticity. Model must be independently evaluated on held-out images and unseen generators.

## Test
```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test investigations
```

## Important limitations
No trained weights or independently validated accuracy are bundled. Video classification samples frames and is not a temporal/lip-sync detector. Audio voice cloning is not implemented. For a winning demo, use a held-out labeled evaluation set, show errors and limitations, and demonstrate at least one real image-classification checkpoint.
