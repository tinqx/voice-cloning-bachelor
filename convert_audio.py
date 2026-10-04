"""
convert_audio.py
Konvertiert Audiodateien in WAV.
"""

import argparse
from pathlib import Path

from pydub import AudioSegment


def convert_file(input_file, output_dir, sample_rate):

    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(sample_rate)
    audio = audio.set_sample_width(2)

    output_file = (
        output_dir
        / f"{input_file.stem}.wav"
    )

    audio.export(
        output_file,
        format="wav"
    )

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Audiodateien in WAV konvertieren"
    )

    parser.add_argument("inputs", nargs="+", help="Audiodateien oder Ordner")
    parser.add_argument("--outdir", default="data/wav/original", help="Zielordner")
    parser.add_argument("--sr", type=int, default=22050, help="Samplingrate in Hz")

    args = parser.parse_args()

    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)

    extensions = (".m4a", ".mp4", ".mp3", ".wav")
    files = []

    for input_path in args.inputs:

        path = Path(
            input_path
        )

        if path.is_dir():

            for file in path.rglob("*"):

                if file.suffix.lower() in extensions:
                    files.append(file)

        elif path.suffix.lower() in extensions:

            files.append(path)

    if not files:

        print(
            "Keine passende Audiodatei gefunden"
        )

        return

    # Dateien konvertieren
    for file in files:

        output_file = convert_file(
            file,
            output_dir,
            args.sr
        )

        print(
            f"OK: {file} -> {output_file}"
        )


if __name__ == "__main__":
    main()