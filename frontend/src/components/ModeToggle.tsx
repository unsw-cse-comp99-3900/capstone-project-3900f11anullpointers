"use client";
import * as React from "react";
import { Moon, Sun, ZoomIn, ZoomOut } from "lucide-react";
import { useThemeContext } from "@/context/theme-context";
import { Button } from "@/components/ui/button";

export function ModeToggle() {
  const { theme, textLarge, toggleTheme, toggleTextSize } = useThemeContext();

  return (
    <div className="flex space-x-2">
      <Button
        variant="outline"
        size={textLarge ? "lg" : "icon"}
        onClick={toggleTheme}
      >
        {theme === "dark" ? (
          <>
            <Sun
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-90 scale-0`}
            />
            <Moon
              className={`absolute ${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
          </>
        ) : (
          <>
            <Sun
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
            <Moon
              className={`absolute ${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-90 scale-0`}
            />
          </>
        )}
        <span className="sr-only">Toggle theme</span>
      </Button>
      <Button
        variant="outline"
        size={textLarge ? "lg" : "icon"}
        onClick={toggleTextSize}
      >
        {textLarge ? (
          <>
            <ZoomIn
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-90 scale-0`}
            />
            <ZoomOut
              className={`absolute ${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
          </>
        ) : (
          <>
            <ZoomIn
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
            <ZoomOut
              className={`absolute ${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-90 scale-0`}
            />
          </>
        )}
      </Button>
    </div>
  );
}
