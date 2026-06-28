import fs from "node:fs";
import path from "node:path";
import {
  defaultSynonyms,
  negations,
  phraseSimplifications,
  preserveWords,
  questionWords,
  timeWords,
} from "./config";
import type { ConversionResult, SignAsset, TaggedToken } from "./types";

const projectRoot = process.cwd();
const metadataDir = path.join(projectRoot, "dataset", "metadata");
const wordsDir = path.join(projectRoot, "dataset", "words");

type SignDictionaryEntry = {
  type: string;
  path: string;
};

function loadJson<T>(filePath: string, fallback: T): T {
  try {
    if (!fs.existsSync(filePath) || fs.statSync(filePath).size === 0) {
      return fallback;
    }
    return JSON.parse(fs.readFileSync(filePath, "utf8")) as T;
  } catch {
    return fallback;
  }
}

function signKey(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

function dictionaryKey(value: string) {
  return signKey(value).replaceAll(" ", "_");
}

function normalizeText(text: string) {
  return text
    .toLowerCase()
    .trim()
    .replaceAll("can't", "cannot")
    .replace(/n't/g, " not")
    .replace(/[^a-z0-9\s']/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function simplifyTextPhrases(text: string) {
  let simplified = ` ${signKey(text)} `;
  Object.entries(phraseSimplifications)
    .sort((a, b) => b[0].length - a[0].length)
    .forEach(([phrase, replacement]) => {
      simplified = simplified.replaceAll(` ${phrase} `, ` ${replacement} `);
    });
  return simplified.trim().replace(/\s+/g, " ");
}

function tokenize(text: string) {
  return text.match(/[a-z]+(?:'[a-z]+)?|\d+/g) ?? [];
}

const pronouns = new Set(["i", "me", "my", "you", "your", "he", "she", "we", "they", "their"]);
const verbs = new Set([
  "go",
  "come",
  "want",
  "need",
  "help",
  "understand",
  "know",
  "remember",
  "forget",
  "think",
  "hear",
  "listen",
  "talk",
  "speak",
  "tell",
  "ask",
  "answer",
  "say",
  "read",
  "write",
  "study",
  "learn",
  "teach",
  "work",
  "play",
  "watch",
  "walk",
  "run",
  "sit",
  "stand",
  "wait",
  "meet",
  "visit",
  "travel",
  "drive",
  "buy",
  "give",
  "take",
  "bring",
  "show",
  "call",
  "use",
  "make",
  "change",
  "choose",
  "join",
  "leave",
  "stay",
  "find",
  "lose",
  "finish",
  "stop",
  "start",
  "move",
  "open",
  "close",
  "drink",
  "eat",
  "cook",
  "pay",
  "sleep",
]);

function tagToken(token: string): TaggedToken {
  if (/^\d+$/.test(token)) return { text: token, pos: "NUM" };
  if (questionWords.has(token)) return { text: token, pos: "WH" };
  if (timeWords.has(token)) return { text: token, pos: "TIME" };
  if (negations.has(token)) return { text: token, pos: "NEG" };
  if (pronouns.has(token)) return { text: token, pos: "PRON" };
  if (verbs.has(token) || token.endsWith("ing") || token.endsWith("ed")) {
    return { text: token, pos: "VERB" };
  }
  return { text: token, pos: "NOUN" };
}

function removeStopwords(tokens: TaggedToken[]) {
  const stopwords = new Set(
    loadJson<string[]>(path.join(metadataDir, "stopwords.json"), []).map((word) => word.toLowerCase()),
  );
  return tokens.filter((token) => !stopwords.has(token.text) || preserveWords.has(token.text));
}

const irregular: Record<string, string> = {
  went: "go",
  gone: "go",
  came: "come",
  bought: "buy",
  gave: "give",
  taken: "take",
  took: "take",
  children: "child",
  men: "man",
  women: "woman",
  better: "good",
  worse: "bad",
};

function lemmatize(tokens: TaggedToken[]) {
  return tokens.map((token) => {
    if (irregular[token.text]) return { ...token, text: irregular[token.text] };
    if (token.pos === "VERB" && token.text.endsWith("ing") && token.text.length > 5) {
      return { ...token, text: token.text.slice(0, -3) };
    }
    if (token.pos === "VERB" && token.text.endsWith("ed") && token.text.length > 4) {
      return { ...token, text: token.text.slice(0, -2) };
    }
    if (token.pos === "NOUN" && token.text.endsWith("s") && token.text.length > 3) {
      return { ...token, text: token.text.slice(0, -1) };
    }
    return token;
  });
}

const numberWords: Record<string, string> = {
  zero: "0",
  one: "1",
  two: "2",
  three: "3",
  four: "4",
  five: "5",
  six: "6",
  seven: "7",
  eight: "8",
  nine: "9",
};

function handleNumbers(tokens: TaggedToken[]) {
  return tokens.map((token) =>
    numberWords[token.text] ? { text: numberWords[token.text], pos: "NUM" } : token,
  );
}

function mapSynonyms(tokens: TaggedToken[]) {
  const userSynonyms = loadJson<Record<string, string>>(path.join(metadataDir, "synonyms.json"), {});
  const synonyms = { ...defaultSynonyms, ...userSynonyms };
  return tokens.map((token) => ({ ...token, text: synonyms[token.text] ?? token.text }));
}

function simplifyTokenPhrases(tokens: TaggedToken[]) {
  const tokenTexts = tokens.map((token) => token.text);
  const rules = Object.entries(phraseSimplifications)
    .sort((a, b) => b[0].length - a[0].length)
    .map(([phrase, replacement]) => [phrase.split(" "), replacement] as const);

  const output: TaggedToken[] = [];
  let index = 0;
  while (index < tokenTexts.length) {
    let matched = false;
    for (const [phraseTokens, replacement] of rules) {
      const end = index + phraseTokens.length;
      if (tokenTexts.slice(index, end).join(" ") === phraseTokens.join(" ")) {
        output.push({ text: replacement, pos: tokens[index].pos });
        index = end;
        matched = true;
        break;
      }
    }
    if (!matched) {
      output.push(tokens[index]);
      index += 1;
    }
  }
  return output;
}

function applyAslOrder(tokens: string[]) {
  const body = tokens.filter((token) => !questionWords.has(token));
  const questions = tokens.filter((token) => questionWords.has(token));
  return [...new Set([...body, ...questions])];
}

function findExistingPath(relativePath: string) {
  const candidate = path.join(projectRoot, relativePath);
  if (fs.existsSync(candidate)) return relativePath.replaceAll("\\", "/");

  const parsed = path.parse(candidate);
  const alternatives = [
    path.join(parsed.dir, `${parsed.name.replaceAll("_", " ")}${parsed.ext}`),
    path.join(parsed.dir, `${parsed.name.replaceAll(" ", "_")}${parsed.ext}`),
    path.join(parsed.dir, `${parsed.name.toLowerCase()}${parsed.ext}`),
    path.join(parsed.dir, `${parsed.name.toUpperCase()}${parsed.ext}`),
  ];

  const found = alternatives.find((alternative) => fs.existsSync(alternative));
  if (!found) return null;
  return path.relative(projectRoot, found).replaceAll("\\", "/");
}

function assetUrl(relativePath: string) {
  return `/api/asset?path=${encodeURIComponent(relativePath)}`;
}

function wordAsset(token: string): SignAsset | null {
  const signs = loadJson<Record<string, SignDictionaryEntry>>(path.join(metadataDir, "sign_dictionary.json"), {});
  const keys = [dictionaryKey(token), signKey(token), signKey(token).replaceAll("_", " ")];

  for (const key of keys) {
    const entry = signs[key];
    if (entry?.path) {
      const found = findExistingPath(entry.path);
      if (found) {
        return {
          token,
          assetType: "video",
          relativePath: found,
          url: assetUrl(found),
          source: "metadata",
        };
      }
    }
  }

  const candidates = [
    path.relative(projectRoot, path.join(wordsDir, `${token}.mp4`)),
    path.relative(projectRoot, path.join(wordsDir, `${token.replaceAll("_", " ")}.mp4`)),
    path.relative(projectRoot, path.join(wordsDir, `${token.replaceAll(" ", "_")}.mp4`)),
  ];

  for (const candidate of candidates) {
    const found = findExistingPath(candidate);
    if (found) {
      return {
        token,
        assetType: "video",
        relativePath: found,
        url: assetUrl(found),
        source: "filesystem",
      };
    }
  }

  return null;
}

function numberAsset(digit: string): SignAsset | null {
  const numbers = loadJson<Record<string, string>>(path.join(metadataDir, "number_dictionary.json"), {});
  const found = numbers[digit] ? findExistingPath(numbers[digit]) : null;
  return found
    ? { token: digit, assetType: "image", relativePath: found, url: assetUrl(found), source: "number" }
    : null;
}

function letterAsset(letter: string): SignAsset | null {
  const alphabet = loadJson<Record<string, string>>(path.join(metadataDir, "alphabet_dictionary.json"), {});
  const found = alphabet[letter.toLowerCase()] ? findExistingPath(alphabet[letter.toLowerCase()]) : null;
  return found
    ? { token: letter.toLowerCase(), assetType: "image", relativePath: found, url: assetUrl(found), source: "alphabet" }
    : null;
}

function retrieveToken(token: string): SignAsset[] {
  const cleanToken = signKey(token);
  const word = wordAsset(cleanToken);
  if (word) return [word];

  if (/^\d+$/.test(cleanToken)) {
    return cleanToken.split("").flatMap((digit) => {
      const asset = numberAsset(digit);
      return asset ? [asset] : [];
    });
  }

  if (cleanToken.length === 1) {
    const asset = letterAsset(cleanToken);
    return asset ? [asset] : [];
  }

  return cleanToken
    .split("")
    .filter((letter) => /[a-z]/.test(letter))
    .flatMap((letter) => {
      const asset = letterAsset(letter);
      return asset ? [asset] : [];
    });
}

export function convertTextToAsl(sourceText: string): ConversionResult {
  const normalizedText = normalizeText(sourceText);
  const simplifiedText = simplifyTextPhrases(normalizedText);
  const tokens = tokenize(simplifiedText);
  const taggedTokens = tokens.map(tagToken);
  const filteredTokens = removeStopwords(taggedTokens);
  const finalTaggedTokens = simplifyTokenPhrases(mapSynonyms(handleNumbers(lemmatize(filteredTokens))));
  const finalTokens = finalTaggedTokens.map((token) => token.text);
  const glossTokens = applyAslOrder(finalTokens);
  const gloss = glossTokens.map((token) => token.toUpperCase()).join(" ");
  const assets = glossTokens.flatMap(retrieveToken);

  return {
    sourceText,
    normalizedText,
    tokens,
    taggedTokens,
    filteredTokens,
    finalTokens,
    glossTokens,
    gloss,
    assets,
  };
}
