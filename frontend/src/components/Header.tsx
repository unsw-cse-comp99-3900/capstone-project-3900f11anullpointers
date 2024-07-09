"use client";
import React from "react";
import { ModeToggle } from "./ModeToggle";
import { useThemeContext } from "@/context/theme-context";

const Header = () => {
  const { theme, textLarge } = useThemeContext();

  return (
    <header className={`bg-primary-foreground text-foreground border-b border-border w-full ${theme === "dark" ? "dark-mode-class" : "light-mode-class"} ${textLarge ? "text-2xl" : "text-base"}`}>
      <div className="container mx-auto flex items-center justify-between py-2 md:py-4 px-4">
        <div className="flex items-center space-x-2 md:space-x-4">
          <img src="/unsw_logo.png" alt="Logo" className="h-10 w-auto md:h-[80px]" />
          <h1 className={`font-heading ${textLarge ? "text-3xl md:text-4xl lg:text-5xl" : "text-xl md:text-3xl lg:text-4xl"} text-primary`}>
            UNSW Optometry Clinic Stuff
          </h1>
        </div>
        <div>
          <ModeToggle />
        </div>
      </div>
    </header>
  );
};

export default Header;
