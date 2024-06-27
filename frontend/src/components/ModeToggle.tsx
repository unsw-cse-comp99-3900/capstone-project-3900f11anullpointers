"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useThemeContext } from "@/context/theme-context";
import { Button } from "@/components/ui/button";

export function ModeToggle() {
  const { theme, toggleTheme } = useThemeContext();

  return (
    <Button variant="outline" size="icon" onClick={
        () => {
            toggleTheme();
            console.log("Theme toggled", theme);
        }

        }>
      {theme === "dark" ? (
        <>
          <Sun className="h-[1.2rem] w-[1.2rem] transition-all rotate-90 scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] transition-all rotate-0 scale-100" />
        </>
      ) : (
        <>
          <Sun className="h-[1.2rem] w-[1.2rem] transition-all rotate-0 scale-100" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] transition-all rotate-90 scale-0" />
        </>
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
