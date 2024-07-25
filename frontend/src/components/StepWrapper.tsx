import { formSteps } from "./formConfigs/AdultFormStepConfig";
import { UseFormReturn } from "react-hook-form";

type StepWrapperProps = {
  form: UseFormReturn<any>;
  step: number;
};

export function StepWrapper({ form, step }: StepWrapperProps) {
  const StepComponent = formSteps[step].component;
  const stepProps = formSteps[step].props;
  return <StepComponent form={form} {...stepProps} />;
}
