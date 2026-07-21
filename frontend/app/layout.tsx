import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VoiceSync AI - AI Video Dubbing',
  description: 'Translate and dub your movies and series with AI-powered voices in 50+ languages',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-900 text-slate-100">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
}
