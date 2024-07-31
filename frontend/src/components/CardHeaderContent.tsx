import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ProgressBar from "./ProgressBar";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

export function CardHeaderContent({
  step,
  totalSteps,
  title,
  description,
}: {
  step: number;
  totalSteps: number;
  title: string;
  description: string;
}) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();
  return (
    <CardHeader>
      <CardTitle
        className={`${textLarge ? "text-5xl" : "text-3xl"} ${
          dyslexicFont ? lexend.className : ""
        } text-center pb-3`}
      >
        {title}
      </CardTitle>
      <CardDescription
        className={`${textLarge ? "text-xl" : "text-sm"} ${
          highContrast ? "filter contrast-200" : ""
        } ${dyslexicFont ? lexend.className : ""}`}
      >
        {description}
      </CardDescription>
      <br />
      <ProgressBar step={step} totalSteps={totalSteps} />
    </CardHeader>
  );
}
