import { NextRequest, NextResponse } from "next/server";
import { convertTextToAsl } from "@/lib/asl/pipeline";

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as { text?: string };
    const text = body.text?.trim();

    if (!text) {
      return NextResponse.json({ error: "Text is required." }, { status: 400 });
    }

    return NextResponse.json(convertTextToAsl(text));
  } catch {
    return NextResponse.json({ error: "Unable to convert text." }, { status: 500 });
  }
}
