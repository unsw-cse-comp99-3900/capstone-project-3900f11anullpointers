import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ArrowRight, ArrowLeft } from "lucide-react";
import { useFormContext } from "react-hook-form";
import { useState } from "react";
import { toast } from "@/components/ui/use-toast";

type FormButtonsProps = {
  formStep: number;
  setFormStep: (step: number) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  setIsSubmitted: (submitted: boolean) => void;
  handleRestart: () => void; // Add this line
};

export function FormButtons({ formStep, setFormStep, isLoading, setIsLoading, setIsSubmitted, handleRestart }: FormButtonsProps) {
  const { trigger, getValues } = useFormContext();

  const handleNext = async () => {
    let fieldsToValidate: string | readonly string[] | undefined = [];
    if (formStep === 0) {
      fieldsToValidate = ['name', 'email'];
    } else if (formStep === 2) {
      fieldsToValidate = ['signature'];
    }

    const isValid = await trigger(fieldsToValidate);
    isValid && setFormStep(formStep + 1);
  };

  const handleFinalSubmit = async () => {
    setIsLoading(true);
    const formData = getValues();

    try {
      // For debugging
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setIsLoading(false);
      setFormStep(formStep + 1);

      // TODO: Fix this up to be appropriate with the backend
/*       const response = await fetch('http://localhost:3030/post', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify(formData),
       });

       if (!response.ok) {
         const errorData = await response.json();
         throw new Error(errorData.message || 'Network response was not ok');
       }

       setIsLoading(false);
       setFormStep(formStep + 1); */
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
      {formStep > 0 && formStep < 3 && (
        <Button
          type='button'
          variant={"ghost"}
          onClick={() => setFormStep(formStep - 1)}
          disabled={isLoading}
        >
          <ArrowLeft className='w-4 h-4 mr-2' />
          Go Back
        </Button>
      )}
      {formStep < 2 && (
        <Button
          type='button'
          variant={"ghost"}
          className={cn("ml-auto", {
            hidden: formStep === 2,
          })}
          onClick={handleNext}
          disabled={isLoading}
        >
          {formStep === 1 ? 'Review' : 'Next Page'}
          <ArrowRight className='w-4 h-4 ml-2' />
        </Button>
      )}
      {formStep === 2 && (
        <Button
          type='button'
          onClick={handleFinalSubmit}
          disabled={isLoading}
        >
          {isLoading ? 'Submitting...' : 'Submit'}
        </Button>
      )}
      {formStep === 3 && (
        <Button
          className="w-full"
          type='button'
          onClick={handleRestart}
        >
          Restart
        </Button>
      )}
    </div>
  );
}

