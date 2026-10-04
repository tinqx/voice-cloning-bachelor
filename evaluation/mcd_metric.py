"""
mcd_metric.py

Berechnung von MCD-DTW-SL

Verwendete Implementierung:
pymcd

Quelle:
Q. Chen, M. Tan, Y. Qi, J. Zhou, Y. Li, und Q. Wu, „V2C: Visual Voice Cloning“, in 2022
IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)

Repository:
https://github.com/chenqi008/pymcd
https://github.com/chenqi008/V2C
"""

import tempfile
from pathlib import Path

import soundfile as sf
from pymcd.mcd import Calculate_MCD

from audio_utils import load_audio

def calculate_mcd(ref_wav, synth_wav, sample_rate=22050):
   
    ref = load_audio(ref_wav, sample_rate)
    synth = load_audio(synth_wav, sample_rate)

    mcd = Calculate_MCD(MCD_mode="dtw_sl")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        ref_file = temp_dir / "ref.wav"
        synth_file = temp_dir / "synth.wav"

        sf.write(ref_file, ref, sample_rate)
        sf.write(synth_file, synth, sample_rate)

        value = mcd.calculate_mcd(
            str(ref_file),
            str(synth_file)
        )

    return float(value)