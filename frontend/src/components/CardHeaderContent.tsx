import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ProgressBar from "./ProgressBar";
import { useThemeContext } from "@/context/theme-context";


export function CardHeaderContent({ step, totalSteps }: { step: number, totalSteps: number }) {
  const { textLarge } = useThemeContext();
  return (
    <>
      <CardHeader>
        <CardTitle className={textLarge ? 'text-5xl' : 'text-3xl'}>Consent Form</CardTitle>
        <CardDescription className={textLarge ? 'text-xl' : 'text-sm'}>
          Please fill out the following form to provide your consent for the use of your clinical information in research studies.
        </CardDescription>
        <br />
        <ProgressBar step={step} totalSteps={totalSteps}/>
      </CardHeader>
    </>
  );
}
