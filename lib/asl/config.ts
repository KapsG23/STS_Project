export const questionWords = new Set(["who", "what", "when", "where", "why", "how", "which"]);

export const negations = new Set(["no", "not", "never", "cannot", "can't", "dont", "don't"]);

export const timeWords = new Set([
  "today",
  "tomorrow",
  "yesterday",
  "morning",
  "afternoon",
  "evening",
  "night",
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
  "sunday",
  "week",
  "month",
  "year",
  "now",
  "later",
  "soon",
]);

export const defaultSynonyms: Record<string, string> = {
  hey: "hello",
  hi: "hello",
  bye: "goodbye",
  thanks: "thank you",
  thankyou: "thank you",
  physician: "doctor",
  clinic: "hospital",
  ill: "sick",
  unwell: "sick",
  nearest: "near",
  nearby: "near",
  automobile: "car",
  purchase: "buy",
  cellphone: "phone",
  mobile: "phone",
  loudly: "loud",
  rapid: "fast",
  quick: "fast",
};

export const phraseSimplifications: Record<string, string> = {
  "nearest hospital": "hospital",
  "near hospital": "hospital",
  "nearby hospital": "hospital",
  "closest hospital": "hospital",
  "sign language": "sign language",
  "thank you": "thank you",
  "how are you": "you how",
  "what is your name": "name what",
  "where is": "where",
  "where are": "where",
};

export const preserveWords = new Set([
  ...questionWords,
  ...negations,
  ...timeWords,
  "i",
  "you",
  "me",
  "my",
  "your",
]);
