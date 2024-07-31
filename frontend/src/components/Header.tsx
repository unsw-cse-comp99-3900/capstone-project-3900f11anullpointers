"use client"
import React, { useEffect, useState } from "react";
import { ModeToggle } from "./ModeToggle";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";
import { Button } from "@/components/ui/button";

const lexend = Lexend({ subsets: ["latin"] });

const Header = () => {
  const { theme, textLarge, dyslexicFont } = useThemeContext();

  const [isChildForm, setIsChildForm] = useState(false);

  useEffect(() => {
    setIsChildForm(window.location.pathname.endsWith("/child-form"));
  }, []);

  return (
    <header className={`bg-primary-foreground text-foreground border-b border-border w-full ${theme === "dark" ? "dark-mode-class" : "light-mode-class"}`}>
      <div className="container mx-auto flex items-center justify-between py-2 md:py-4 px-4 flex-col sm:flex-row">
        <div className="flex items-center space-x-2 md:space-x-4">
          <img src="/unsw_logo.png" alt="Logo" className="h-10 w-auto md:h-[80px]" />
          <h1 className={`${textLarge ? 'text-2xl md:text-4xl lg:text-5xl' : 'text-xl md:text-3xl lg:text-4xl'} ${dyslexicFont ? lexend.className : ""} font-heading text-primary`}>
            UNSW Optometry Clinic
          </h1>
        </div>
        <div className="flex">
          <a href={isChildForm ? '/' : '/child-form'} className="w-full flex justify-end pb-1 pr-2">
            <Button variant='secondary' className={`w-[100%] ${textLarge ? "text-lg" : ""} ${dyslexicFont ? lexend.className : ""}`}>
              {isChildForm ? "Click for Adult Form" : "Click for Child Form"}
            </Button>
          </a>
          <ModeToggle />
        </div>
      </div>
    </header>
  );
};

export default Header;
