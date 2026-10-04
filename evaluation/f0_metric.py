"""
f0_metric.py

Vergleich der Grundfrequenzverläufe

Verwendete Bibliothek:
librosa
numpy

Verwendete Verfahren:
- pYIN für F0, zur Schätzung der Grundfrequenz
- MFCC, Audiosignale beschreiben
- Dynamic Time Warping, zeitliche Ausrichtung
"""

import librosa
import numpy as np

from audio_utils import load_audio


def calculate_f0_metrics(
    ref_wav,
    synth_wav,
    sample_rate=22050,
    f0_min=50,
    f0_max=400
):
    """
    Berechnet F0-RMSE, F0-Korrelation und den Unterschied der Audiodauer
    """

    ref = load_audio(ref_wav, sample_rate)
    synth = load_audio(synth_wav, sample_rate)

    f0_ref, _, _ = librosa.pyin(
        ref,
        fmin=f0_min,
        fmax=f0_max,
        sr=sample_rate
    )

    f0_synth, _, _ = librosa.pyin(
        synth,
        fmin=f0_min,
        fmax=f0_max,
        sr=sample_rate
    )

    # MFCCs berechnen
    mfcc_ref = librosa.feature.mfcc(y=ref, sr=sample_rate)
    mfcc_synth = librosa.feature.mfcc(y=synth, sr=sample_rate)

    # Zeitliche Ausrichtung mit DTW
    _, path = librosa.sequence.dtw(
        X=mfcc_ref,
        Y=mfcc_synth,
        metric="euclidean"
    )

    aligned_ref = []
    aligned_synth = []

    for ref_index, synth_index in path[::-1]:
        ref_value = f0_ref[ref_index]
        synth_value = f0_synth[synth_index]

        # Nur stimmhafte Frames vergleichen
        if not np.isnan(ref_value) and not np.isnan(synth_value):
            aligned_ref.append(ref_value)
            aligned_synth.append(synth_value)

    aligned_ref = np.array(aligned_ref)
    aligned_synth = np.array(aligned_synth)

    # Unterschied der Audiodauer
    duration_diff = abs(len(ref) - len(synth)) / sample_rate

    # falls zu wenig gültige f0 Werte vorhanden sind
    if len(aligned_ref) < 3:
        return {
            "f0_rmse_hz": None,
            "f0_corr": None,
            "duration_diff_sec": float(duration_diff)
        }

    # F0-RMSE
    f0_rmse = np.sqrt(
        np.mean((aligned_ref - aligned_synth) ** 2)
    )

    # F0-Korrelation
    if np.std(aligned_ref) == 0 or np.std(aligned_synth) == 0:
        f0_corr = None
    else:
        f0_corr = float(
            np.corrcoef(aligned_ref, aligned_synth)[0, 1]
        )

    return {
        "f0_rmse_hz": float(f0_rmse),
        "f0_corr": f0_corr,
        "duration_diff_sec": float(duration_diff)
    }