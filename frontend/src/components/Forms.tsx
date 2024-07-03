import { UseFormReturn } from "react-hook-form";
import { CheckboxWithText } from "@/components/CheckboxWithText";
import { CardDescription, CardTitle } from "./ui/card";
import { FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const FHr = () => <hr className='my-4' />;

type FormStep1Props = {
  form: UseFormReturn<any>;
};

export function FormStep1({ form }: FormStep1Props) {
  return (
    <div>
      <CardTitle className='pb-3'>
        Personal Information and Contact
      </CardTitle>
      <FHr />
      <FormField
        control={form.control}
        name='name'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Full name</FormLabel>
            <FormControl>
              <Input placeholder='Enter your name' {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className="text-red-500">
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
              <FormMessage className="text-red-500">
                {fieldState.error.message}
              </FormMessage>
            )}
          </FormItem>
        )}
      />
    </div>
  );
}

type FormStep2Props = {
  form: UseFormReturn<any>;
};

export function FormStep2({ form }: FormStep2Props) {
  return (
    <div>
      <CardTitle className='pb-3'>
        Use of Clinical Information for Research
      </CardTitle>
      <FHr />
      <CheckboxWithText
        form={form}
        checkbox1={{
          labelText:
            "I CONSENT to the use of my de-identified* clinical information for the purpose of research",
          descriptionText: "",
        }}
        checkbox2={{
          labelText:
            "I DO NOT CONSENT to the use of my de-identified* clinical information for the purpose of research",
          descriptionText: "",
        }}
        submitButtonText='Submit'
        mobileSettingsLink='/examples/forms'
      />
      <br />
      <CardDescription>
        *De-identified information is data that has been stripped of all personal identifiers, such as name, address, and contact information.
      </CardDescription>
    </div>
  );
}

type FormStep3Props = {
  form: UseFormReturn<any>;
};

export function FormStep3({ form }: FormStep3Props) {
  const { getValues } = form;
  const values = getValues();

  return (
    <div className='space-y-4'>
      <CardTitle className='pb-3'>
        Review Your Information
      </CardTitle>
      <FHr />
      <div>
        <strong>Name:</strong> {values.name}
      </div>
      <div>
        <strong>Email:</strong> {values.email}
      </div>
      <div>
        <strong>Research Consent:</strong> {values.acceptResearchConsent ? "Accepted" : "Denied"}
      </div>
      <div>
        <strong>Student Consent:</strong> {values.acceptStudentConesent ? "Accepted" : "Denied"}
      </div>
      <FHr />
      <FormDescription>
        By signing below, you agree that the information you have provided is accurate
      </FormDescription>
      <FormField
        control={form.control}
        name='signature'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Signature</FormLabel>
            <FormControl>
              <Input placeholder='Type your name to sign' {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className="text-red-500">
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
    <div className="text-center">
      <div>
        <CardTitle className="mb-5">Form Submitted Successfully</CardTitle>
        <CardDescription>
          Your information has been submitted successfully. Thank you!
        </CardDescription>
      </div>
    </div>
  );
}
