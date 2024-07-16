import { UseFormReturn } from "react-hook-form";
import { CheckboxWithText } from "@/components/CheckboxWithText";
import { CardDescription, CardTitle } from "@/components/ui/card";
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { SignatureInput } from "@/components/ui/signature-input";

const FHr = () => <hr className='my-4' />;

type FormStepProps = {
  form: UseFormReturn<any>;
};

export function FormStep0({ form }: FormStepProps) {
  return (
    <div>
      <CardTitle className='pb-3'>Personal Information and Contact</CardTitle>
      <FHr />
      <FormField
        control={form.control}
        name='name'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Parent/ Guardian's Full name</FormLabel>
            <FormControl>
              <Input placeholder='Enter your full name' {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className='text-red-500'>
                {fieldState.error.message}
              </FormMessage>
            )}
          </FormItem>
        )}
      />
      <br />
      <FormField
        control={form.control}
        name='email'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input placeholder='Enter your email' {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className='text-red-500'>
                {fieldState.error.message}
              </FormMessage>
            )}
          </FormItem>
        )}
      />
    </div>
  );
}

export function FormStep1({ form }: FormStepProps) {
  return (
    <div>
      <CardTitle className='pb-3'>
        Use of Clinical Information in Research Studies
      </CardTitle>
      <FHr />
      <CardDescription className="pb-3">
        Please indicate below whether you give consent for your child's{" "}
        <u>de-identified</u>* information being used for teaching and research
        purposes. This has no bearing on your child's clinical care.
      </CardDescription>
      <CheckboxWithText
        form={form}
        checkbox1={{
          name: "acceptResearchConsent",
          labelText:
            "I CONSENT to the use of my child's de-identified* clinical information for the purpose of research",
          descriptionText: "",
        }}
        checkbox2={{
          name: "denyResearchConsent",
          labelText:
            "I DO NOT CONSENT to the use of my child's de-identified* clinical information for the purpose of research",
          descriptionText: "",
        }}
      />
      <br />
      <CardDescription>
        *De-identified means we will exclude your name and contact details from
        the research database
      </CardDescription>
    </div>
  );
}

export function FormStep3({ form }: FormStepProps) {
  return (
    <div>
      <CardTitle className='pb-3'>Student Clinic Consent</CardTitle>
      <CardDescription className='font-bold text-gray-700'>
        I acknowledge that I have been informed that my child's initial eye
        examination and subsequent care in the UNSW Optometry Clinic will be
        conducted by an optometry student under the supervision of a qualified,
        APHRA registered optometrist.
      </CardDescription>
      <FHr />
      <CheckboxWithText
        form={form}
        checkbox1={{
          name: "acceptStudentConsent",
          labelText:
            "I CONSENT to my child being examined by a student under supervision",
          descriptionText: "",
        }}
        checkbox2={{
          name: "denyStudentConsent",
          labelText:
            "I DO NOT CONSENT to my child being examined by a student under supervision",
          descriptionText: "",
        }}
      />
    </div>
  );
}

export function FormReviewStep({ form }: FormStepProps) {
  const { getValues } = form;
  const values = getValues();

  return (
    <div className='space-y-4'>
      <CardTitle className='pb-3'>Review Your Information</CardTitle>
      <FHr />
      <div>
        <strong>Name:</strong> {values.name}
      </div>
      <div>
        <strong>Email:</strong> {values.email}
      </div>
      <div>
        <strong>Research Consent:</strong>{" "}
        {values.acceptResearchConsent ? "Accepted" : "Denied"}
      </div>
      <div>
        <strong>Student Consent:</strong>{" "}
        {values.acceptStudentConsent ? "Accepted" : "Denied"}
      </div>
      <FHr />
      <FormDescription>
        By signing below, you agree that the information you have provided is
        accurate
      </FormDescription>
      <FormField
        control={form.control}
        name='drawSignature'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Parent's Signature</FormLabel>
            <FormControl>
              <SignatureInput field={field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className='text-red-500'>
                {fieldState.error.message}
              </FormMessage>
            )}
          </FormItem>
        )}
      />
    </div>
  );
}

export function FormSuccess() {
  return (
    <div className='text-center'>
      <div>
        <CardTitle className='mb-5'>Form Submitted Successfully</CardTitle>
        <CardDescription>
          Your information has been submitted successfully. Thank you!
        </CardDescription>
      </div>
    </div>
  );
}
