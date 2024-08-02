import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider as CustomThemeProvider } from "@/context/theme-context";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import Footer from "@/components/Footer";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "UNSW Optometry Clinic",
  description: "UNSW Optometry Clinic Consent Form",
};
const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        <NextThemesProvider attribute="class" defaultTheme="system">
          <CustomThemeProvider>
            <div className="flex-shrink-0">
              <Header />
            </div>
            <main className="flex-grow flex flex-col items-center justify-center">
              {children}
            </main>
            <div className="flex-shrink-0">
              <Footer />
            </div>
          </CustomThemeProvider>
        </NextThemesProvider>
      </body>
    </html>
  );
}
