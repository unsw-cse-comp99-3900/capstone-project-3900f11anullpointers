import { FormStepConfig } from "../forms/AdultFormStepConfig";
import { UseFormReturn } from "react-hook-form";

type StepWrapperProps = {
  form: UseFormReturn<any>;
  step: FormStepConfig;
};

export function StepWrapper({ form, step }: StepWrapperProps) {
  const StepComponent = step.component;
  const stepProps = step.props;
  return <StepComponent form={form} {...stepProps} />;
}
