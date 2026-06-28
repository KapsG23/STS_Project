# Speech to ASL

Modern Next.js app for converting spoken or typed English into ASL gloss and retrieving matching signs from the local dataset.

## What It Does

1. Accepts typed text or browser microphone speech input.
2. Normalizes and tokenizes the sentence.
3. Removes helper words while preserving useful ASL meaning.
4. Applies lemmatization, synonym mapping, number handling, and phrase simplification.
5. Converts English into ASL gloss order.
6. Retrieves matching videos from `dataset/words`.
7. Falls back to alphabet or number images from `dataset/alphabets` and `dataset/numbers`.

## Run The Next.js App

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

Use the microphone flow:

1. Open the app in Chrome or Edge.
2. Click `Start mic`.
3. Allow microphone permission if the browser asks.
4. Speak your full sentence.
5. Click `Stop and convert` to turn the transcript into ASL gloss and signs.

Create a production build:

```bash
npm run build
npm start
```

## Python CLI Backend Check

The Python pipeline is still available for quick terminal verification and tests.

Install Python dependencies if needed:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Run a CLI conversion:

```bash
python app.py --text "Where is the nearest hospital?"
```

Run tests:

```bash
python -m unittest discover tests
```

## Deployment

The app is structured for Vercel with Next.js API routes:

- `app/api/convert/route.ts` converts text into ASL gloss.
- `app/api/asset/route.ts` safely streams dataset videos/images.
- `next.config.ts` includes the dataset in Vercel function tracing.
