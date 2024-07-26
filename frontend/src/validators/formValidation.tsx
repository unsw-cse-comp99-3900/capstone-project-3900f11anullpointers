// lib/formValidation.ts
import { useFormContext } from "react-hook-form";

export const useFormValidation = () => {
  const { trigger, getValues } = useFormContext();

  const validateStep = async (formStep: number, formType: string) => {
    let fieldsToValidate: string[] = [];

    if (formType === "typeA") {
      if (formStep === 0) {
        fieldsToValidate = ["name", "email"];
      } else if (formStep === 1) {
        fieldsToValidate = ["acceptResearchConsent", "denyResearchConsent"];
      } else if (formStep === 2) {
        fieldsToValidate = ["acceptContactConsent", "denyContactConsent"];
      } else if (formStep === 3) {
        fieldsToValidate = ["acceptStudentConsent", "denyStudentConsent"];
      } else if (formStep === 4) {
        fieldsToValidate = ["drawSignature"];
      }
    } else if (formType === "typeB") {
      if (formStep === 0) {
        fieldsToValidate = ["name", "email"];
      } else if (formStep === 1) {
        fieldsToValidate = ["acceptResearchConsent", "denyResearchConsent"];
      } else if (formStep === 2) {
        fieldsToValidate = ["acceptStudentConsent", "denyStudentConsent"];
      } else if (formStep === 3) {
        fieldsToValidate = ["drawSignature"];
      }
    }

    return await trigger(fieldsToValidate);
  };

  const getFormData = () => getValues();

  return { validateStep, getFormData };
};
