# Voice-Clone Evaluation (Tortoise TTS & OpenVoice)

Dieses Repository enthält den praktischen Teil der Bachelorarbeit zum Thema Voice Cloning und Sprachassistenten. 
Für die Generierung der Sprachaufnahmen werden die bestehenden Open Source Projekte Tortoise TTS und OpenVoice verwendet.
Objektive und praxisnahe Bewertung von Voice Cloning Ausgaben (Eigenaufnahmen → Klon → Metriken → HomePod Tests). 

**Implementierungsbasis:** https://github.com/neonbjb/tortoise-tts

**Vergleich:** https://github.com/myshell-ai/OpenVoice/tree/main/openvoice

---

## Inhalt
- `evaluation/` – Skripte zur Ähnlichkeitsbewertung
- `results/` – Ergebnisse der Evaluation im JSON Format
- `data/` – Referenz- und Klonaufnahmen (die eigenen Aufnahmen werden aus Datenschutzgründen nicht veröffentlicht)
- `convert_audio.py` – Konvertierung der Audiodateien
- `requirements.txt` – Benötigte Python Bibliotheken
- `benchmark_presets.py` – Tortoise TTS Preset Vergleich
  
---

## Voraussetzungen
- Windows mit Python 3.9
- NVIDIA Grafikkarte mit CUDA Unterstützung

## Installation

**1. Tortoise TTS herunterladen**
```bash
git clone https://github.com/neonbjb/tortoise-tts.git
cd tortoise-tts
```

**2. Dateien dieses Repositories hinzufügen** 

Die mitgelieferte 'requirements.txt' ersetzt dabei die Originaldatei

**3. Virtuelle Umgebung erstellen und Abhängigkeiten installieren**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Ergebnisse
Die Ergebnisse der objektiven Evaluation werden im Ordner `results/` als JSON Dateien gespeichert.

Jede Datei enthält die berechneten Werte für:
- MCD-DTW-SL
- SECS
- F0-RMSE
- F0-Korrelation
- Dauer-Differenz
---

## Beispiel Kommandozeile: 
**Audio konvertieren**
```bash
python convert_audio.py data/raw/aufnahme.m4a
```
**Sprachgenerierung**
```bash
python tortoise/do_tts.py --text "Hey Siri, what time is it?" --voice myvoice --preset standard
```
**Evaluation einer einzelnen Klonaufnahme**
```bash
python evaluation/eval_voiceclone.py --ref data/wav/original/original_time.wav --synth data/wav/synthetic/Ting_60s_time1.wav
```
**Evaluation aller Audio Dateien eines Ordners**
```bash
python evaluation/eval_voiceclone.py --ref data/wav/original/original_time.wav --synth_dir data/wav/synthetic --output results/time_evaluation.json
```

