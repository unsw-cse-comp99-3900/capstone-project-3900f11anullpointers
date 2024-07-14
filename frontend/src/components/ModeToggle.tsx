"use client";
import * as React from "react";
import { Moon, Sun, ZoomIn, ZoomOut, Contrast, EyeOff, Eye, Circle } from "lucide-react";
import { useThemeContext } from "@/context/theme-context";
import { Button } from "@/components/ui/button";

export function ModeToggle() {
  const { theme, textLarge, highContrast, dyslexicFont, toggleTheme, toggleTextSize, toggleHighContrast, toggleDyslexicFont } = useThemeContext();

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
            <ZoomOut
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
          </>
        ) : (
          <>
            <ZoomIn
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
          </>
        )}
        <span className="sr-only">Toggle large text</span>
      </Button>
      <Button
        variant="outline"
        size={textLarge ? "lg" : "icon"}
        onClick={toggleHighContrast}
      > {
          highContrast ? (
            <Contrast
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-180 scale-100`}
            />
          ) : (
            <Circle
              className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
                } transition-all rotate-0 scale-100`}
            />
          )
        }
      </Button>
      <Button
        variant="outline"
        size={textLarge ? "lg" : "icon"}
        onClick={toggleDyslexicFont}
      >
        {dyslexicFont ?
          (<Eye
            className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
              } transition-all rotate-0 scale-100`}
          />) :
          (<EyeOff
            className={`${textLarge ? "h-6 w-6" : "h-[1.2rem] w-[1.2rem]"
              } transition-all rotate-0 scale-100`} />)
        }
        <span className="sr-only">Toggle dyslexic font</span>
      </Button>
    </div>
  );
}
