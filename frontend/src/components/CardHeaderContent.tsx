import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ProgressBar from "./ProgressBar";
import { useThemeContext } from "@/context/theme-context";

export function CardHeaderContent({ step, totalSteps }: { step: number, totalSteps: number }) {
  return (
    <>
      <CardHeader>
        <CardTitle className='text-3xl'>Consent Form</CardTitle>
        <CardDescription>
          Please fill out the following form to provide your consent for the use of your clinical information in research studies.
        </CardDescription>
        <br />
        <ProgressBar step={step} totalSteps={totalSteps}/>
      </CardHeader>
    </>
  );
}
