import type { Metadata } from "next";
import { Orbitron, Rajdhani } from "next/font/google";
import "./globals.css";

const orbitron = Orbitron({
  variable: "--font-orbitron",
  subsets: ["latin"],
});

const rajdhani = Rajdhani({
  variable: "--font-rajdhani",
  weight: ["300", "400", "500", "600", "700"],
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Voice Agent RAG | AI-Powered Voice Assistant",
  description: "Real-time voice-powered RAG (Retrieval-Augmented Generation) agent with LiveKit, Cartesia, and Deepgram integration.",
  keywords: ["voice AI", "RAG", "LiveKit", "voice assistant", "AI agent", "real-time", "Cartesia", "Deepgram"],
  authors: [{ name: "Voice Agent RAG Team" }],
  creator: "Voice Agent RAG",
  publisher: "Voice Agent RAG",

  // Favicon and Icons
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
      { url: '/icon.svg', type: 'image/svg+xml', sizes: '32x32' },
    ],
    apple: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
  },

  // PWA Configuration
  manifest: '/manifest.json',

  // Open Graph
  openGraph: {
    title: "Voice Agent RAG | AI-Powered Voice Assistant",
    description: "Real-time voice-powered RAG agent with AI capabilities",
    type: "website",
    locale: "en_US",
    siteName: "Voice Agent RAG",
  },

  // Twitter Card
  twitter: {
    card: "summary_large_image",
    title: "Voice Agent RAG",
    description: "Real-time AI-Powered Voice Assistant",
  },
};

// Viewport configuration (Next.js 14+ requires separate export)
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#00D4FF' },
    { media: '(prefers-color-scheme: dark)', color: '#1a1b26' },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${orbitron.variable} ${rajdhani.variable} antialiased`}
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
