import { z } from "zod";

export const consentSchema = z.object({
  acceptResearchConsent: z.boolean(),
  denyResearchConsent: z.boolean(),
  acceptStudentConesent: z.boolean(),
  denyStudentConsent: z.boolean(),
  email: z.string().email(),
  name: z
    .string()
    .min(1, { message: "Please enter a name" })
    .max(255),
  date: z
    .coerce
    .date(),
  signature: z
    .string()
    .min(1, { message: "Please type your name to sign" })
})
  .refine(schema => {
    return !(
      schema.acceptResearchConsent && schema.denyResearchConsent ||
      schema.acceptStudentConesent && schema.denyStudentConsent
    )
  });

