import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ProgressBar from "./ProgressBar";
import { useThemeContext } from "@/context/theme-context";

export function CardHeaderContent({
  step,
  totalSteps,
}: {
  step: number;
  totalSteps: number;
}) {

  const { textLarge } = useThemeContext();
  return (
    <>
      <CardHeader>
        <CardTitle className={`text-center pb-3 ${textLarge ? "text-4xl" : "text-3xl"}`}>Patient Consent & Information Sheet</CardTitle>
        <CardDescription className={`${textLarge ? "text-lg" : ""}`}>
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
