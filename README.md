# Speech to ASL

Modular BE project pipeline for converting spoken or typed English into ASL gloss and retrieving matching dataset signs.

## Pipeline

1. Speech-to-text adapter: Moonshine first, Vosk fallback support.
2. Text normalization: lowercase, punctuation cleanup, whitespace cleanup.
3. Tokenization and POS tagging.
4. Intelligent stopword removal.
5. Lemmatization, number handling, synonym mapping, and phrase simplification.
6. ASL gloss conversion with deterministic ordering rules.
7. Dataset retrieval from `dataset/words`, `dataset/alphabets`, and `dataset/numbers`.
8. Optional video merge with MoviePy.

## Run

Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Start the UI:

```bash
streamlit run app.py
```

Run a quick CLI conversion:

```bash
python app.py --text "Where is the nearest hospital?"
```

Run tests:

```bash
python -m unittest discover tests
```

The core text-to-ASL pipeline has standard-library fallbacks, so it can still convert and retrieve assets before optional NLP/STT packages are installed.
