import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ArrowRight, ArrowLeft } from "lucide-react";
import { useFormContext } from "react-hook-form";
import { toast } from "@/components/ui/use-toast";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

const BACKEND_HOST = process.env.NEXT_PUBLIC_HOST;
const BACKEND_PORT = process.env.NEXT_PUBLIC_BACKEND_PORT;

type FormButtonsProps = {
  formStep: number;
  setFormStep: (step: number) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  setIsSubmitted: (submitted: boolean) => void;
  handleRestart: () => void;
};

export function FormButtons({
  formStep,
  setFormStep,
  isLoading,
  setIsLoading,
  setIsSubmitted,
  handleRestart,
}: FormButtonsProps) {
  const { trigger, getValues } = useFormContext();

  const handleNext = async () => {
    let fieldsToValidate: string | readonly string[] | undefined = [];
    if (formStep === 0) {
      fieldsToValidate = ["name", "email"];
    } else if (formStep === 1) {
      fieldsToValidate = ["acceptResearchConsent", "denyResearchConsent"];
    } else if (formStep === 2) {
      fieldsToValidate = ["acceptContactConsent", "denyContactConsent"];
    } else if (formStep == 3) {
      fieldsToValidate = ["acceptStudentConsent", "denyStudentConsent"];
    } else if (formStep === 4) {
      fieldsToValidate = ["drawSignature"];
    }

    const isValid = await trigger(fieldsToValidate);
    isValid && setFormStep(formStep + 1);
  };

  const handleFinalSubmit = async () => {
    const isValid = await trigger(["drawSignature"]);
    if (!isValid) return;

    setIsLoading(true);
    const formData = getValues();

    if (!formData.drawSignature) {
      setIsLoading(false);
      return;
    }

    try {
      let fieldsToValidate: string = "drawSignature"

      const isValid = await trigger(fieldsToValidate);
      if (!isValid) {
        return
      }
      setIsLoading(true);

      const reqFormData = {
        name: formData.name,
        email: formData.email,
        drawSignature: formData.drawSignature,
        formType: formData.formType,
        consent: {
          researchConsent: formData.acceptResearchConsent,
          contactConsent: formData.acceptContactConsent,
          studentConsent: formData.acceptStudentConsent,
        },
      };
      // For debugging
      /*       await new Promise((resolve) => setTimeout(resolve, 1000));
            setIsLoading(false);
            setFormStep(formStep + 1); */

      const backendURL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;
      const response = await fetch(`${backendURL}/post`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reqFormData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Network response was not ok");
      }

      setIsLoading(false);
      setFormStep(formStep + 1);
    } catch (error: any) {
      setIsLoading(false);
      toast({
        variant: "destructive",
        title: "Something went wrong",
        description: error.message,
      });
    }
  };

  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className="flex justify-between">
      {formStep > 0 && formStep < 5 && (
        <Button
          type="button"
          variant={"ghost"}
          onClick={() => setFormStep(formStep - 1)}
          disabled={isLoading}
          className={`${textLarge ? "text-xl" : "text-sm"} ${
            highContrast ? "filter contrast-200" : ""
          } ${dyslexicFont ? lexend.className : ""}`}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Go Back
        </Button>
      )}
      {formStep < 4 && (
        <Button
          type="button"
          variant={"ghost"}
          className={cn(
            { "text-xl": textLarge, "text-sm": !textLarge },
            { "filter contrast-200": highContrast },
            { [lexend.className]: dyslexicFont },
            "ml-auto",
            { hidden: formStep === 4 }
          )}
          onClick={handleNext}
          disabled={isLoading}
        >
          {formStep === 3 ? "Review" : "Next Page"}
          <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
      )}
      {formStep === 4 && (
        <Button
          type="button"
          onClick={handleFinalSubmit}
          disabled={isLoading}
          className={`${textLarge ? "text-xl" : "text-sm"} ${
            highContrast ? "filter contrast-200" : ""
          } ${dyslexicFont ? lexend.className : ""}`}
        >
          {isLoading ? "Submitting..." : "Submit"}
        </Button>
      )}
      {formStep === 5 && (
        <Button
          className={`w-full ${textLarge ? "text-xl" : "text-sm"} ${
            highContrast ? "filter contrast-200" : ""
          } ${dyslexicFont ? lexend.className : ""}`}
          type="button"
          onClick={handleRestart}
        >
          Restart
        </Button>
      )}
    </div>
  );
}
