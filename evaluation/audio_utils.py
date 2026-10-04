"""
audio_utils.py

Hilfsfunktionen zum Laden und Vorverarbeiten von Audiodateien
Auf die gewünschte Samplingrate bringen und entfernt Stille am Anfang und Ende

Verwendete Bibliothek: 
librosa
"""

import librosa


def load_audio(path, sample_rate, trim_top_db=30):

    audio, _ = librosa.load(
        path,
        sr=sample_rate,
        mono=True
    )

    audio, _ = librosa.effects.trim(
        audio,
        top_db=trim_top_db
    )

    return audio