import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export function CardHeaderContent() {
  return (
    <>
      <CardHeader>
        <CardTitle className='text-3xl'>Teaching & Research</CardTitle>
        <CardDescription>
          The UNSW Optometry Clinic is part of the School of Optometry and
          Vision Science, UNSW Australia. It is a teaching facility for both
          undergraduate and postgraduate optometry students, providing
          excellence in eye care and is at the forefront of the latest
          research.
          <br />
          <br />
          *De-identified means we will exclude your name and contact details
          from the research database
        </CardDescription>
      </CardHeader>
      <CardHeader>
        <CardTitle className='text-lg'>
          USE OF CLINICAL INFORMATION IN RESEARCH STUDIES
        </CardTitle>
      </CardHeader>
    </>
  );
}
