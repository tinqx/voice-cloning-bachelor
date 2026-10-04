"""
secs_metric.py

Berechnung der Sprecherähnlichkeit

Verwendetes Modell:
SpeechBrain ECAPA-TDNN

Modell:
speechbrain/spkrec-ecapa-voxceleb

Die Speaker Embeddings werden mit SpeechBrain erzeugt, anschließend die Cosine Similarity berechnet.
"""
import numpy as np
import torch
from speechbrain.inference import EncoderClassifier

from audio_utils import load_audio


def load_speaker_model():

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        run_opts={"device": device}
    )

    return model, device


def calculate_secs(
    ref_wav,
    synth_wav,
    model,
    device,
    sample_rate=16000
):
    """
    Berechnet die Cosine Similarity zwischen den Speaker Embeddings von Referenz und Synthese
    """

    ref = load_audio(ref_wav, sample_rate)
    synth = load_audio(synth_wav, sample_rate)

    ref = torch.tensor(ref).float().unsqueeze(0).to(device)
    synth = torch.tensor(synth).float().unsqueeze(0).to(device)

    with torch.inference_mode():
        emb_ref = model.encode_batch(ref).squeeze().cpu().numpy()
        emb_synth = model.encode_batch(synth).squeeze().cpu().numpy()

    similarity = np.dot(emb_ref, emb_synth) / (
        np.linalg.norm(emb_ref) * np.linalg.norm(emb_synth) + 1e-9
    )

    return float(similarity)