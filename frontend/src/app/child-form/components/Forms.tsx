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
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

const FHr = () => <hr className="my-4" />;

type FormStepProps = {
  form: UseFormReturn<any>;
};

export function FormStep0({ form }: FormStepProps) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className={textLarge ? "text-2xl" : "text-base"}>
      <CardTitle
        className={`pb-3 ${textLarge ? "text-3xl" : "text-xl"} ${
          dyslexicFont ? lexend.className : ""
        }`}
      >
        Personal Information and Contact
      </CardTitle>
      <FHr />
      <FormField
        control={form.control}
        name="name"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel
              className={`pb-3 ${textLarge ? "text-xl" : ""} ${
                dyslexicFont ? lexend.className : ""
              }`}
            >
              Parent/ Guardian&apos;s Full name
            </FormLabel>
            <FormControl>
              <Input
                className={`pb-3 ${textLarge ? "text-xl" : ""} ${
                  dyslexicFont ? lexend.className : ""
                }`}
                placeholder="Enter your full name"
                {...field}
              />
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
        name="email"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel
              className={`pb-3 ${textLarge ? "text-xl" : ""} ${
                dyslexicFont ? lexend.className : ""
              }`}
            >
              Email
            </FormLabel>
            <FormControl>
              <Input
                className={`pb-3 ${textLarge ? "text-xl" : ""} ${
                  dyslexicFont ? lexend.className : ""
                }`}
                placeholder="Enter your email"
                {...field}
              />
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

export function FormStep1({ form }: FormStepProps) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className={textLarge ? "text-2xl" : "text-base"}>
      <CardTitle
        className={`pb-3 ${textLarge ? "text-3xl" : "text-xl"} ${
          dyslexicFont ? lexend.className : ""
        }`}
      >
        Use of Clinical Information in Research Studies
      </CardTitle>
      <FHr />
      <CardDescription
        className={`pb-3 ${textLarge ? "text-xl" : "text-base"} ${
          highContrast ? "filter contrast-200" : ""
        } ${dyslexicFont ? lexend.className : ""}`}
      >
        Please indicate below whether you give consent for your child&apos;s{" "}
        <u>de-identified</u>* information being used for teaching and research
        purposes. This has no bearing on your child&apos;s clinical care.
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
      <CardDescription
        className={`${textLarge ? "text-xl" : "text-base"} ${
          highContrast ? "filter contrast-200" : ""
        } ${dyslexicFont ? lexend.className : ""}`}
      >
        *De-identified means we will exclude your name and contact details from
        the research database
      </CardDescription>
    </div>
  );
}

export function FormStep3({ form }: FormStepProps) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div>
      <CardTitle
        className={`pb-3 ${textLarge ? "text-3xl" : "text-xl"} ${
          dyslexicFont ? lexend.className : ""
        }`}
      >
        Student Clinic Consent
      </CardTitle>
      <CardDescription
        className={`${textLarge ? "text-xl" : "text-base"} ${
          highContrast ? "filter contrast-200" : ""
        } ${dyslexicFont ? lexend.className : ""} font-bold text-gray-700`}
      >
        I acknowledge that I have been informed that my child&apos;s initial eye
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
      <div>
        <strong>Research Consent:</strong>{" "}
        {values.acceptResearchConsent ? "Accepted" : "Denied"}
      </div>
      <div>
        <strong>Student Consent:</strong>{" "}
        {values.acceptStudentConsent ? "Accepted" : "Denied"}
      </div>
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
        name="drawSignature"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel
              className={`${textLarge ? "text-xl" : "text-base"} ${
                dyslexicFont ? lexend.className : ""
              }`}
            >
              Parent&apos;s Signature
            </FormLabel>
            <FormControl>
              <SignatureInput field={field} />
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
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className={`text-center ${textLarge ? "text-2xl" : "text-base"}`}>
      <div>
        <CardTitle
          className={`mb-5 ${textLarge ? "text-2xl" : "text-base"} ${
            dyslexicFont ? lexend.className : ""
          }`}
        >
          Form Submitted Successfully
        </CardTitle>
        <CardDescription
          className={`${textLarge ? "text-xl" : "text-base"} ${
            highContrast ? "filter contrast-200" : ""
          } ${dyslexicFont ? lexend.className : ""}`}
        >
          Your information has been submitted successfully. Thank you!
        </CardDescription>
      </div>
    </div>
  );
}
