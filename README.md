# TruthLens Advanced — Multimodal Forensic Workbench

A functional, local-first Django hackathon prototype for evidence intake, explainable forensic **indicators**, cross-modal evidence inventory, chain-of-custody fingerprints and PDF reports.

## Quick start (Windows PowerShell)

Use Python 3.12. **If Windows blocks `pip.exe` or `django-admin.exe`, use `python.exe -m ...` as below.**

```powershell
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt --index-url https://pypi.org/simple --timeout 60 --retries 10
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ . If network dependencies fail, install `requirements-minimal.txt` first; image/text/reporting will work, but video/audio require optional packages.

## What is implemented

- Premium responsive dark investigation dashboard, case history, multi-file uploads
- Image: EXIF presence, dimensions, JPEG recompression statistics
- Video: frame sampling, duration/FPS, abrupt transition timestamps (requires OpenCV)
- Audio: duration, RMS, clipping, zero-crossing rate (requires Librosa + NumPy)
- Text: word statistics and optional token-overlap with trusted reference
- Cross-modal evidence inventory with **explicitly disclosed** missing lip-sync/transcription verification
- SHA-256 hashes for uploaded evidence; persistent SQLite case archive
- PDF evidence report with analysis, limitations, and hashes

## Scientific integrity

**This app does not have a trained deepfake classifier.** Heuristics are not proof of manipulation. No invented deepfake percentages. Its default assessment is `Inconclusive — manual verification recommended`. Add validated pretrained models to `investigations/analyzers.py` before claiming deepfake detection. Audio/transcript synchronization is not implemented. Results can be affected by codecs, transcoding, metadata stripping, camera movement, and compression.

## Demo script

1. Create an investigation and upload a sample image, video and audio recording.
2. Paste a claim and optionally a trusted reference passage.
3. Show evidence SHA-256 fingerprints and per-modality metrics.
4. Show timestamps of sampled video transitions and explain that these are **not** deepfake detections.
5. Open the cross-modal review and explain which model-based checks remain pending.
6. Download the PDF and discuss evidence traceability.

## Recommended advanced extensions for the team

- Validated deepfake image/video model with documented dataset, threshold, calibration and benchmarks
- Voice anti-spoofing model (ASVspoof-style) with held-out testing
- Speech-to-text with consent, forced alignment and timestamped transcript comparisons
- Face tracking and audiovisual synchronization model, plus heatmap overlays
- Authenticated user roles, case access permissions, background task queue, audit events
- Signed reports, retention controls, virus scanning, secure media serving

## Security notes

Local demo only: default DEBUG=1, no login, uploads served directly during development. Do not expose publicly without authentication, media isolation, rate limiting, file validation, malware scanning, storage controls, and production configuration. No evidence is uploaded to external AI services by this code.

## Team split

1. Backend/security + integration
2. Image/video models and benchmarking
3. Audio/transcript models
4. Cross-modal correlation and evidence visualization
5. Frontend, reporting, tests and pitch

## Testing

```powershell
.\venv\Scripts\python.exe manage.py test investigations
```


## Advanced image evidence extension

The image analyzer now generates an **ELA-style JPEG recompression residual image** displayed in each case's evidence card. This is a visual aid, **not a deepfake heatmap** or reliable localization of edits. JPEG encoding, detailed textures and ordinary exports can create bright regions.

### Optional pretrained image classifier

No pretrained model is bundled, and no network model download happens by default. To enable an experimental Hugging Face image classifier, install the optional dependencies and configure a model you have evaluated for your specific task:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-ai.txt --index-url https://pypi.org/simple --timeout 60 --retries 10
$env:TRUTHLENS_IMAGE_MODEL = 'YOUR_TRUSTED_MODEL_ID_OR_LOCAL_PATH'
.\venv\Scripts\python.exe manage.py runserver
```

Model labels and scores are displayed **as-is**, separately from the overall inconclusive assessment. A generic image classifier is not automatically a deepfake detector. Validate the selected model on held-out real and manipulated examples, record the dataset and report false positives before making any accuracy claims. Downloading model weights may require substantial bandwidth and storage.

### Privacy and safety

The ZIP intentionally excludes your original local SQLite database and uploaded evidence. Use a fresh database (`manage.py migrate`). `DEBUG=1` serves uploaded media for local demonstration; do not deploy this configuration publicly. Restrict uploads, authentication and evidence access before production use.

### Recommended hackathon demo

Show (1) upload, (2) SHA-256 evidence provenance, (3) numerical forensic indicators, (4) ELA residual image and its limitations, (5) optional pretrained model results if independently tested, and (6) PDF report. Never claim the ELA visualization proves an image is AI-generated.


## Version 3: Evidence visualization and efficient optional AI inference

- Video analyzer now saves up to six timestamped sample-frame previews (OpenCV required). These frames are **not** AI deepfake detections.
- Audio analyzer now saves an amplitude waveform preview for the analyzed 90-second segment (Librosa and NumPy required).
- Optional Hugging Face classifier is cached in memory after the first inference. Choose a trusted task-specific model and independently benchmark its false-positive rate. No pretrained weights are bundled.
- New automated tests cover video frame previews and waveform generation when dependencies are available.
- These derived images are saved under `media/derived/`. For a local hackathon demo only; do not expose evidence or derivatives without access controls.

### How to enable experimental model predictions

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-ai.txt --index-url https://pypi.org/simple --timeout 60 --retries 10
$env:TRUTHLENS_IMAGE_MODEL = 'YOUR_TRUSTED_DEEPFAKE_IMAGE_CLASSIFIER'
.\venv\Scripts\python.exe manage.py runserver
```

Verify model compatibility, model card and intended labels before setting the variable. A model trained for ordinary object classification does **not** detect deepfakes. Scores are not calibrated probabilities of forgery.

## V4: Optional model inference + evaluation

Image inference is **real pretrained-model inference only when you explicitly configure a trusted, trained model**. This ZIP does not bundle or download model weights automatically. The model must be a Hugging Face-compatible image-classification model with meaningful `real` and `fake` labels; a general-purpose object classifier is NOT a deepfake detector. Check model card, licensing, training dataset and evaluation before using it.

Install optional AI requirements:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-ai.txt --index-url https://pypi.org/simple --timeout 60 --retries 10
```

In the same PowerShell session, configure your trusted model ID or local directory and run the server:

```powershell
$env:TRUTHLENS_IMAGE_MODEL = "PATH_OR_HF_ID_OF_VERIFIED_BINARY_CLASSIFIER"
.\venv\Scripts\python.exe manage.py runserver
```

The configured model is used on images and up to eight sampled video frames; results appear in the case detail page and exported PDF. It is **not** a video temporal model or voice/lip-sync detector. Models can be large and CPU inference may take time. Initial model downloads require working internet access. Do not enable an untrusted model; this integration disables `trust_remote_code`.

### Benchmark model quality (before claiming detection accuracy)

Prepare `labels.csv` with columns `path,truth` where `truth` is `real` or `fake`, and paths are relative to the CSV file. Keep this set held out from training. Then run:

```powershell
.\venv\Scripts\python.exe evaluate_model.py labels.csv --fake-label fake
```

Adjust `--fake-label` to the model's exact label. This outputs confusion matrix, accuracy, fake-class precision and recall, specificity, and per-file errors. Metrics depend on the dataset; don't claim generalization from a tiny or biased sample.

### Safety / deployment notes

The development server is for local demos only. Uploaded files and reports may contain sensitive media; use synthetic/consented samples, don't expose the app publicly without authentication and access controls, and don't claim that heuristic indicators authenticate content. The project is a hackathon prototype, not a certified forensic tool.
