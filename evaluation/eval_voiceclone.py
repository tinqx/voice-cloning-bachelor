"""
eval_voiceclone.py

Führt die Metriken aus und speichert die Ergebnisse als JSON
"""

import argparse
import json
from pathlib import Path

from mcd_metric import calculate_mcd
from secs_metric import load_speaker_model, calculate_secs
from f0_metric import calculate_f0_metrics


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True, help="Referenzaufnahme")
    parser.add_argument("--synth", nargs="+", help="Klonaufnahme")
    parser.add_argument("--synth_dir", help="Ordner mit Klonaufnahmen")
    parser.add_argument("--output", default="results.json", help="Ergebnisdatei")
    args = parser.parse_args()

    clone_files = args.synth or []

    if args.synth_dir:
        clone_files += [
            str(file)
            for file in sorted(Path(args.synth_dir).glob("*.wav"))
        ]

    if not clone_files:
        print("Keine Klonaufnahmen gefunden.")
        return

    model, device = load_speaker_model()
    results = {}

    for i, clone in enumerate(clone_files, start=1):

        print(f"\nAuswertung {i}: {clone}")

        mcd = calculate_mcd(args.ref, clone)
        secs = calculate_secs(args.ref, clone, model, device)
        f0 = calculate_f0_metrics(args.ref, clone)

        results[f"candidate_{i}"] = {
            "file": clone,
            "mcd_dtw_sl": round(mcd, 3),
            "secs_cosine": round(secs, 3),
            "f0_rmse_hz": round(f0["f0_rmse_hz"], 3),
            "f0_corr": round(f0["f0_corr"], 3),
            "duration_diff_sec": round(f0["duration_diff_sec"], 3)
        }

        print(f"MCD-DTW-SL: {mcd:.3f}")
        print(f"SECS: {secs:.3f}")
        print(f"F0-RMSE: {f0['f0_rmse_hz']:.3f}")
        print(f"F0-Korrelation: {f0['f0_corr']:.3f}")
        print(f"Dauer-Differenz: {f0['duration_diff_sec']:.3f} s")

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print(f"\nErgebnisse gespeichert: {args.output}")


if __name__ == "__main__":
    main()