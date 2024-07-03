import { UseFormReturn } from "react-hook-form";
import { CheckboxWithText } from "@/components/CheckboxWithText";
import { CardTitle } from "./ui/card";

type FormStep1Props = {
  form: UseFormReturn<any>;
};

export function FormStep3({ form }: FormStep1Props) {
  return (
    <div>
      <CardTitle className='text-lg pb-3'>
        Use of Clinical Information for Research
      </CardTitle>
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
    </div>

  );
}
