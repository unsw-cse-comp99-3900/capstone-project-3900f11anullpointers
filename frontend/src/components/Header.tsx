"use client"
import React from "react";
import { ModeToggle } from "./ModeToggle";
import { useThemeContext } from "@/context/theme-context";

const Header = () => {
  const { theme } = useThemeContext();

  return (
    <header className={`bg-background text-foreground border-b border-border w-full ${theme === "dark" ? "dark-mode-class" : "light-mode-class"}`}>
      <div className="container mx-auto flex items-center justify-between py-4 px-4">
        <div className="flex items-center space-x-4">
          <img src="/unsw_logo.png" alt="Logo" className="h-[80px] w-auto" />
          <h1 className="font-heading text-3xl md:text-4xl text-primary">
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
