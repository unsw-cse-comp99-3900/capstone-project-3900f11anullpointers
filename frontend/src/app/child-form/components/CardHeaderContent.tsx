import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ProgressBar from "@/components/ProgressBar";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

export function CardHeaderContent({
  step,
  totalSteps,
}: {
  step: number;
  totalSteps: number;
}) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();
  return (
    <>
      <CardHeader>
        <CardTitle
          className={`${textLarge ? "text-5xl" : "text-3xl"} ${
            dyslexicFont ? lexend.className : ""
          } text-center pb-3`}
        >
          Patient&apos;s Consent & Information Sheet (Children)
        </CardTitle>
        <CardDescription
          className={`${textLarge ? "text-xl" : "text-sm"} ${
            highContrast ? "filter contrast-200" : ""
          } ${dyslexicFont ? lexend.className : ""}`}
        >
          The UNSW Optometry Clinic is part of the School of Optometry and
          Vision Science, UNSW Australia. It is a teaching facility for both
          undergraduate and postgraduate optometry students, providing
          excellence in eye care and is at the forefront of the latest research.{" "}
        </CardDescription>
        <br />
        <ProgressBar step={step} totalSteps={totalSteps} />
      </CardHeader>
    </>
  );
}
