import { UseFormReturn } from "react-hook-form";
import { CheckboxWithText } from "@/components/CheckboxWithText";
import { CardDescription, CardTitle } from "./ui/card";
import { FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useThemeContext } from "@/context/theme-context";

const FHr = () => <hr className='my-4' />;

type FormStep1Props = {
  form: UseFormReturn<any>;
};

export function FormStep1({ form }: FormStep1Props) {
  const { textLarge } = useThemeContext();

  return (
    <div className={textLarge ? "text-2xl" : "text-base"}>
      <CardTitle className={`pb-3 ${textLarge ? "text-2xl" : "text-base"}`}>
        Personal Information and Contact
      </CardTitle>
      <FHr />
      <FormField
        control={form.control}
        name='name'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className={textLarge ? "text-xl" : "text-base"}>Full name</FormLabel>
            <FormControl>
              <Input className={textLarge ? "text-xl" : "text-base"} placeholder='Enter your name' {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className={"text-red-500 " + (textLarge ? "text-xl" : "text-base")}>
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
            <FormLabel className={textLarge ? "text-xl" : "text-base"}>Email</FormLabel>
            <FormControl>
              <Input className={textLarge ? "text-xl" : "text-base"} placeholder='Enter your email' {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className={"text-red-500 " + (textLarge ? "text-xl" : "text-base")}>
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
  const { textLarge } = useThemeContext();

  return (
    <div className={textLarge ? "text-2xl" : "text-base"}>
      <CardTitle className={`pb-3 ${textLarge ? "text-2xl" : "text-base"}`}>
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
      <CardDescription className={textLarge ? "text-xl" : "text-base"}>
        *De-identified information is data that has been stripped of all personal identifiers, such as name, address, and contact information.
      </CardDescription>
    </div>
  );
}

type FormStep3Props = {
  form: UseFormReturn<any>;
};

export function FormStep3({ form }: FormStep3Props) {
  const { textLarge } = useThemeContext();
  const { getValues } = form;
  const values = getValues();

  return (
    <div className={`space-y-4 ${textLarge ? "text-2xl" : "text-base"}`}>
      <CardTitle className={`pb-3 ${textLarge ? "text-2xl" : "text-base"}`}>
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
        <strong>Student Consent:</strong> {values.acceptStudentConsent ? "Accepted" : "Denied"}
      </div>
      <FHr />
      <FormDescription className={textLarge ? "text-xl" : "text-base"}>
        By signing below, you agree that the information you have provided is accurate
      </FormDescription>
      <FormField
        control={form.control}
        name='signature'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className={textLarge ? "text-xl" : "text-base"}>Signature</FormLabel>
            <FormControl>
              <Input className={textLarge ? "text-xl" : "text-base"} placeholder='Type your name to sign' {...field} />
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
  const { textLarge } = useThemeContext();

  return (
    <div className={`text-center ${textLarge ? "text-2xl" : "text-base"}`}>
      <div>
        <CardTitle className={`mb-5 ${textLarge ? "text-2xl" : "text-base"}`}>Form Submitted Successfully</CardTitle>
        <CardDescription className={textLarge ? "text-xl" : "text-base"}>
          Your information has been submitted successfully. Thank you!
        </CardDescription>
      </div>
    </div>
  );
}
