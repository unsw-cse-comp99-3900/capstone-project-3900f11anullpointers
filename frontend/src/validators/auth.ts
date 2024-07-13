import { z } from "zod";

export const consentSchema = z
  .object({
    acceptResearchConsent: z.boolean(),
    denyResearchConsent: z.boolean(),
    acceptStudentConsent: z.boolean(),
    denyStudentConsent: z.boolean(),
    email: z.string().email(),
    name: z
      .string()
      .min(1, { message: "Please enter a name" })
      .max(255, { message: "Name is too long" }),
    textSignature: z
      .string()
      .min(1, { message: "Please type your name to sign" }), // Ensure the signature is included and validated
    drawSignature: z
      .string()
      .min(1, { message: "Please draw your signature to sign" }), // Ensure the signature is included and validated
  })
  .refine(
    (schema) => {
      const researchConsentValid = !(
        schema.acceptResearchConsent && schema.denyResearchConsent
      );
      const studentConsentValid = !(
        schema.acceptStudentConsent && schema.denyStudentConsent
      );
      return researchConsentValid && studentConsentValid;
    },
    {
      message: "You cannot both accept and deny consent.",
      path: ["consent"], // This will point the error to the 'consent' field, adjust as necessary
    }
  );
