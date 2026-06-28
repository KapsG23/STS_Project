import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Speech to ASL",
  description: "Convert English speech or text into ASL gloss and matching sign media.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
