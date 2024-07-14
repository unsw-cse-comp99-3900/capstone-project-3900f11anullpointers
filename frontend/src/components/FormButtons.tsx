import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ArrowRight, ArrowLeft } from "lucide-react";
import { useFormContext } from "react-hook-form";
import { toast } from "@/components/ui/use-toast";
import { useThemeContext } from "@/context/theme-context";

type FormButtonsProps = {
  formStep: number;
  setFormStep: (step: number) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  setIsSubmitted: (submitted: boolean) => void;
  handleRestart: () => void;
};

export function FormButtons({ formStep, setFormStep, isLoading, setIsLoading, setIsSubmitted, handleRestart }: FormButtonsProps) {
  const { trigger, getValues } = useFormContext();
  const { textLarge } = useThemeContext();

  const handleNext = async () => {
    let fieldsToValidate: string | readonly string[] | undefined = [];
    if (formStep === 0) {
      fieldsToValidate = ["name", "email"];
    } else if (formStep === 1) {
      fieldsToValidate = ["acceptResearchConsent", "denyResearchConsent"]
    } else if (formStep === 2) {
      fieldsToValidate = ["acceptContactConsent", "denyContactConsent"]
    } else if (formStep == 3) {
      fieldsToValidate = ["acceptStudentConsent", "denyStudentConsent"]
    } else if (formStep === 4) {
      fieldsToValidate = ['signature'];
    }

    const isValid = await trigger(fieldsToValidate);
    isValid && setFormStep(formStep + 1);
    console.log("UP!!", formStep)
  };

  const handleFinalSubmit = async () => {
    const formData = getValues();
    
    console.log(formData);
    try {
      let fieldsToValidate: string = "signature"
  
      const isValid = await trigger(fieldsToValidate);
      if (!isValid){
        return
      }
      setIsLoading(true);

      const reqFormData = {
        name: formData.name,
        email: formData.email,
        signature: formData.signature,
        formType: formData.formType,
        consent: {
          researchConsent: formData.acceptResearchConsent,
          contactConsent: formData.acceptContactConsent,
          studentConsent: formData.acceptStudentConsent,
        }
      }
      // For debugging
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setIsLoading(false);
      setFormStep(formStep + 1);

        const response = await fetch('http://localhost:3030/post', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify(reqFormData),
       });

       if (!response.ok) {
         const errorData = await response.json();
         throw new Error(errorData.message || 'Network response was not ok');
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

  return (
    <div className='flex justify-between'>
      {formStep > 0 && formStep < 5 && (
        <Button
          type='button'
          variant={"ghost"}
          className={textLarge ? "text-xl" : ""}
          onClick={() => setFormStep(formStep - 1)}
          disabled={isLoading}
        >
          <ArrowLeft className='w-4 h-4 mr-2' />
          Go Back
        </Button>
      )}
      {formStep < 4 && (
        <Button
          type='button'
          variant={"ghost"}
          className={cn("ml-auto", {
            hidden: formStep === 4,
          }) + (textLarge ? " text-xl" : "")}
          onClick={handleNext}
          disabled={isLoading}
        >
          {formStep === 3 ? 'Review' : 'Next Page'}
          <ArrowRight className='w-4 h-4 ml-2' />
        </Button>
      )}
      {formStep === 4 && (
        <Button
          type='button'
          onClick={handleFinalSubmit}
          disabled={isLoading}
          className={textLarge ? "text-xl" : ""}
        >
          {isLoading ? 'Submitting...' : 'Submit'}
        </Button>
      )}
      {formStep === 5 && (
        <Button
          className={"w-full " + (textLarge ? "text-xl" : "")}
          type='button'
          onClick={handleRestart}
        >
          Restart
        </Button>
      )}
    </div>
  );
}

