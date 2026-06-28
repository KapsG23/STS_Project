"use client";

import { FormEvent, useMemo, useState } from "react";

type SignAsset = {
  token: string;
  assetType: "video" | "image";
  url: string;
  source: string;
};

type ConvertResponse = {
  sourceText: string;
  normalizedText: string;
  tokens: string[];
  glossTokens: string[];
  gloss: string;
  assets: SignAsset[];
};

type SpeechRecognitionConstructor = new () => SpeechRecognition;

type SpeechRecognition = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
};

type SpeechRecognitionEvent = {
  results: {
    [index: number]: {
      [index: number]: {
        transcript: string;
      };
    };
    length: number;
  };
};

const examples = [
  "Where is the nearest hospital?",
  "I want water.",
  "Hey, how are you?",
  "How can I help you?",
  "Thank you doctor.",
];

declare global {
  interface Window {
    SpeechRecognition?: SpeechRecognitionConstructor;
    webkitSpeechRecognition?: SpeechRecognitionConstructor;
  }
}

export default function Home() {
  const [text, setText] = useState(examples[0]);
  const [result, setResult] = useState<ConvertResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState("");

  const hasAssets = Boolean(result?.assets.length);
  const videoCount = useMemo(
    () => result?.assets.filter((asset) => asset.assetType === "video").length ?? 0,
    [result],
  );

  async function convert(nextText = text) {
    const cleanText = nextText.trim();
    if (!cleanText) {
      setError("Please enter or speak a sentence first.");
      return;
    }

    setIsLoading(true);
    setError("");
    try {
      const response = await fetch("/api/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: cleanText }),
      });

      if (!response.ok) {
        throw new Error("Conversion failed. Please try again.");
      }

      const payload = (await response.json()) as ConvertResponse;
      setResult(payload);
    } catch (conversionError) {
      setError(conversionError instanceof Error ? conversionError.message : "Conversion failed.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void convert();
  }

  function startSpeechInput() {
    const Recognition = window.SpeechRecognition ?? window.webkitSpeechRecognition;
    if (!Recognition) {
      setError("Speech input is not supported in this browser. Chrome or Edge works best.");
      return;
    }

    const recognition = new Recognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      const transcript = event.results[event.results.length - 1][0].transcript;
      setText(transcript);
      void convert(transcript);
    };
    recognition.onerror = () => {
      setIsListening(false);
      setError("I could not hear that clearly. Please try again or type the sentence.");
    };
    recognition.onend = () => setIsListening(false);

    setError("");
    setIsListening(true);
    recognition.start();
  }

  return (
    <main className="shell">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">BE Final Year Project</p>
          <h1>Speech to ASL Converter</h1>
          <p>
            Speak or type English, get ASL gloss in signing order, and see the matched signs from
            your alphabet, number, and word dataset.
          </p>
        </div>
        <div className="hero-panel">
          <span>Live pipeline</span>
          <strong>Speech/Text to ASL Gloss to Sign Media</strong>
        </div>
      </section>

      <section className="workspace">
        <form className="input-panel" onSubmit={handleSubmit}>
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Input</p>
              <h2>Recognized speech or typed text</h2>
            </div>
            <button type="button" className="ghost-button" onClick={startSpeechInput}>
              {isListening ? "Listening..." : "Use mic"}
            </button>
          </div>

          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Speak or type a sentence..."
            rows={5}
          />

          <div className="example-row">
            {examples.map((example) => (
              <button
                key={example}
                type="button"
                onClick={() => {
                  setText(example);
                  void convert(example);
                }}
              >
                {example}
              </button>
            ))}
          </div>

          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? "Converting..." : "Convert to ASL"}
          </button>

          {error ? <p className="error">{error}</p> : null}
        </form>

        <section className="output-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Output</p>
              <h2>ASL conversion</h2>
            </div>
            <span className="asset-count">{hasAssets ? `${result?.assets.length} signs` : "Ready"}</span>
          </div>

          <div className="gloss-card">
            <span>Final ASL Gloss</span>
            <strong>{result?.gloss || "Your ASL gloss will appear here"}</strong>
          </div>

          <div className="meta-grid">
            <div>
              <span>Tokens</span>
              <strong>{result?.glossTokens.join("  ") || "-"}</strong>
            </div>
            <div>
              <span>Videos matched</span>
              <strong>{videoCount}</strong>
            </div>
          </div>
        </section>
      </section>

      <section className="sign-section">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Dataset retrieval</p>
            <h2>Matched signs</h2>
          </div>
          <p>{hasAssets ? "Videos play from the dataset; unknown words fall back to fingerspelling." : ""}</p>
        </div>

        {hasAssets ? (
          <div className="asset-grid">
            {result?.assets.map((asset, index) => (
              <article className="asset-card" key={`${asset.token}-${index}`}>
                <div className="asset-title">
                  <strong>{asset.token.toUpperCase()}</strong>
                  <span>{asset.source}</span>
                </div>
                {asset.assetType === "video" ? (
                  <video src={asset.url} controls muted playsInline />
                ) : (
                  <img src={asset.url} alt={`${asset.token} sign`} />
                )}
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <strong>No conversion yet</strong>
            <span>Try “I want water” or use the microphone to begin.</span>
          </div>
        )}
      </section>
    </main>
  );
}
