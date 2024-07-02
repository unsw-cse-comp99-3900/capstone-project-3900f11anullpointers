import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ArrowRight } from "lucide-react";

type FormButtonsProps = {
  formStep: number;
  setFormStep: (step: number) => void;
};

export function FormButtons({ formStep, setFormStep }: FormButtonsProps) {
  return (
    <div className='absolute bottom-0 left-0 right-0 flex gap-2 p-4'>
      <Button
        type='submit'
        className={cn({
          hidden: formStep === 0,
        })}
      >
        Submit
      </Button>
      <Button
        type='button'
        variant={"ghost"}
        className={cn({
          hidden: formStep === 1,
        })}
        onClick={() => {
          // validation
          // form.trigger(["email", "name", "year", "studentId"]);
          // const emailState = form.getFieldState("email");
          // const nameState = form.getFieldState("name");
          // const yearState = form.getFieldState("year");
          // const idState = form.getFieldState("studentId");

          // if (!emailState.isDirty || emailState.invalid) return;
          // if (!nameState.isDirty || nameState.invalid) return;
          // if (!yearState.isDirty || yearState.invalid) return;
          // if (!idState.isDirty || idState.invalid) return;
          setFormStep(1);
        }}
      >
        Next Page
        <ArrowRight className='w-4 h-4 ml-2' />
      </Button>
      <Button
        type='button'
        variant={"ghost"}
        onClick={() => setFormStep(0)}
        className={cn({
          hidden: formStep === 0,
        })}
      >
        Go Back
      </Button>
    </div>
  );
}
