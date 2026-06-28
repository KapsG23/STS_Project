import fs from "node:fs/promises";
import path from "node:path";
import { NextRequest, NextResponse } from "next/server";

const contentTypes: Record<string, string> = {
  ".mp4": "video/mp4",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

export async function GET(request: NextRequest) {
  const relativePath = request.nextUrl.searchParams.get("path");
  if (!relativePath) {
    return NextResponse.json({ error: "Asset path is required." }, { status: 400 });
  }

  const projectRoot = process.cwd();
  const datasetRoot = path.resolve(projectRoot, "dataset");
  const assetPath = path.resolve(projectRoot, relativePath);

  if (!assetPath.startsWith(`${datasetRoot}${path.sep}`)) {
    return NextResponse.json({ error: "Asset path is not allowed." }, { status: 403 });
  }

  try {
    const file = await fs.readFile(assetPath);
    const extension = path.extname(assetPath).toLowerCase();
    return new NextResponse(file, {
      headers: {
        "Content-Type": contentTypes[extension] ?? "application/octet-stream",
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  } catch {
    return NextResponse.json({ error: "Asset not found." }, { status: 404 });
  }
}
