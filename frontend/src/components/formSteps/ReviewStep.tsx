import { UseFormReturn } from "react-hook-form";
import { CardTitle } from "../ui/card";
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
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

const FHr = () => <hr className='my-4' />;

type FormStepProps = {
  form: UseFormReturn<any>;
  showResearchConsent?: boolean;
  showContactConsent?: boolean;
  showStudentConsent?: boolean;
};

export function ReviewStep({
  form,
  showResearchConsent = true,
  showContactConsent = true,
  showStudentConsent = true,
}: FormStepProps) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();
  const { getValues } = form;
  const values = getValues();

  return (
    <div
      className={`space-y-4 ${textLarge ? "text-2xl" : "text-base"} ${
        dyslexicFont ? lexend.className : ""
      }`}
    >
      <CardTitle
        className={`pb-3 ${textLarge ? "text-2xl" : "text-base"} ${
          dyslexicFont ? lexend.className : ""
        }`}
      >
        Review Your Information
      </CardTitle>
      <FHr />
      <div>
        <strong>Name:</strong> {values.name}
      </div>
      <div>
        <strong>Email:</strong> {values.email}
      </div>
      {showResearchConsent && (
        <div>
          <strong>Research Consent:</strong>{" "}
          {values.acceptResearchConsent ? "Accepted" : "Denied"}
        </div>
      )}
      {showContactConsent && (
        <div>
          <strong>Contact Consent:</strong>{" "}
          {values.acceptContactConsent ? "Accepted" : "Denied"}
        </div>
      )}
      {showStudentConsent && (
        <div>
          <strong>Student Consent:</strong>{" "}
          {values.acceptStudentConsent ? "Accepted" : "Denied"}
        </div>
      )}
      <FHr />
      <FormDescription
        className={`${textLarge ? "text-xl" : "text-base"} ${
          highContrast ? "filter contrast-200" : ""
        } ${dyslexicFont ? lexend.className : ""}`}
      >
        By signing below, you agree that the information you have provided is
        accurate
      </FormDescription>
      <FormField
        control={form.control}
        name='drawSignature'
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel
              className={`${textLarge ? "text-xl" : "text-base"} ${
                dyslexicFont ? lexend.className : ""
              }`}
            >
              Signature
            </FormLabel>
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
