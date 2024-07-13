import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ProgressBar from "./ProgressBar";

export function CardHeaderContent({
  step,
  totalSteps,
}: {
  step: number;
  totalSteps: number;
}) {
  return (
    <>
      <CardHeader>
        <CardTitle className='text-3xl text-center pb-3'>Patient Consent & Information Sheet</CardTitle>
        <CardDescription>
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
