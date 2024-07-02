import { UseFormReturn } from "react-hook-form";
import { CheckboxWithText } from "@/components/CheckboxWithText";

type FormStep1Props = {
  form: UseFormReturn<any>;
};

export function FormStep1({ form }: FormStep1Props) {
  return (
    <CheckboxWithText
      form={form}
      checkbox1={{
        labelText:
          "I CONSENT to the use of my de‐identified* clinical information for the purpose of research",
        descriptionText: "",
      }}
      checkbox2={{
        labelText:
          "I DO NOT CONSENT to the use of my de‐identified* clinical information for the purpose of research",
        descriptionText: "",
      }}
      submitButtonText='Submit'
      mobileSettingsLink='/examples/forms'
    />
  );
}
