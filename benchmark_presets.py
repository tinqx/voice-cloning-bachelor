"""
benchmark_presets.py

Vergleicht die Generierungszeit der Tortoise TTS Presets
"""

import argparse
import json
import time
from pathlib import Path

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio


def load_voice(folder):
    files = sorted(Path(folder).glob("*.wav"))

    if not files:
        raise ValueError("Keine WAV Dateien gefunden.")

    return [load_audio(str(file), 22050) for file in files]


def benchmark(tts, preset, text, voice_samples, repetitions):

    start = time.perf_counter()

    for _ in range(repetitions):
        tts.tts_with_preset(
            text,
            voice_samples=voice_samples,
            preset=preset
        )

    average_time = (time.perf_counter() - start) / repetitions

    return average_time


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--output", default="benchmark_results.json")
    args = parser.parse_args()

    tts = TextToSpeech()
    voice_samples = load_voice(args.voice)

    presets = [
        "ultra_fast",
        "fast",
        "standard",
        "high_quality"
    ]

    results = {}

    for preset in presets:

        print(f"\nBenchmark: {preset}")

        average_time = benchmark(
            tts,
            preset,
            args.text,
            voice_samples,
            args.repetitions
        )

        results[preset] = {
            "avg_time_sec": round(average_time, 2),
            "repetitions": args.repetitions
        }

        print(f"Zeit: {average_time:.2f} s")

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print(f"\nErgebnisse gespeichert: {args.output}")


if __name__ == "__main__":
    main()