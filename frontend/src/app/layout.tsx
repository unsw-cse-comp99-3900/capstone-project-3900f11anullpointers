import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider as CustomThemeProvider } from "@/context/theme-context";
import { ThemeProvider as NextThemesProvider } from "next-themes";

export const metadata: Metadata = {
  title: "UNSW Optometry Clinic",
  description: "Consent form for the UNSW Optometry Clinic",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <NextThemesProvider attribute="class" defaultTheme="system">
          <CustomThemeProvider>
            {children}
          </CustomThemeProvider>
        </NextThemesProvider>
      </body>
    </html>
  );
}
