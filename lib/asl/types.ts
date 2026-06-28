export type TaggedToken = {
  text: string;
  pos: string;
};

export type SignAsset = {
  token: string;
  assetType: "video" | "image";
  relativePath: string;
  url: string;
  source: string;
};

export type ConversionResult = {
  sourceText: string;
  normalizedText: string;
  tokens: string[];
  taggedTokens: TaggedToken[];
  filteredTokens: TaggedToken[];
  finalTokens: string[];
  glossTokens: string[];
  gloss: string;
  assets: SignAsset[];
};
