// components/NavigationButton.tsx
import { Button } from "@/components/ui/button";
import { ArrowRight, ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";
import { Lexend } from "next/font/google";
import { useThemeContext } from "@/context/theme-context";

const lexend = Lexend({ subsets: ["latin"] });

type ButtonProps = {
  onClick: () => void;
  isLoading: boolean;
  textLarge: boolean;
  highContrast: boolean;
  dyslexicFont: boolean;
  direction: "next" | "back";
  label: string;
};

export const NavigationButton = ({
  onClick,
  isLoading,
  textLarge,
  highContrast,
  dyslexicFont,
  direction,
  label,
}: ButtonProps) => (
  <Button
    type="button"
    variant="ghost"
    onClick={onClick}
    disabled={isLoading}
    className={cn(
      textLarge ? "text-xl" : "text-sm",
      highContrast && "filter contrast-200",
      dyslexicFont && lexend.className
    )}
  >
    {direction === "back" && <ArrowLeft className="w-4 h-4 mr-2" />}
    {label}
    {direction === "next" && <ArrowRight className="w-4 h-4 ml-2" />}
  </Button>
);
