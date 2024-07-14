import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider as CustomThemeProvider } from "@/context/theme-context";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "UNSW Optometry",
  description: "Information Discolsure and Consent",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='en' suppressHydrationWarning>
      <head />
      <body className={inter.className}>
        <NextThemesProvider attribute='class' defaultTheme='system'>
          <CustomThemeProvider>
            <Header />
            {children}
            <Footer />
          </CustomThemeProvider>
        </NextThemesProvider>
      </body>
    </html>
  );
}
