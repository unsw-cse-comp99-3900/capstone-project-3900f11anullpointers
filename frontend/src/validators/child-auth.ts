import { z } from "zod";

export const consentSchema = z
  .object({
    acceptResearchConsent: z.boolean(),
    denyResearchConsent: z.boolean(),
    acceptStudentConsent: z.boolean(),
    denyStudentConsent: z.boolean(),
    email: z.string().email(),
    formType: z.enum(["child", "adult"]),
    name: z
      .string()
      .min(1, { message: "Please enter a name" })
      .max(255, { message: "Name is too long" }),
    drawSignature: z
      .string()
      .min(1, { message: "Please draw your signature to sign" }), // Ensure the signature is included and validated
  })
  .superRefine((data, ctx) => {
    if (
      (data.acceptResearchConsent && data.denyResearchConsent) ||
      (!data.acceptResearchConsent && !data.denyResearchConsent)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "You cannot both accept and deny research consent.",
        path: ["acceptResearchConsent"],
      });
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "You cannot both accept and deny research consent.",
        path: ["denyResearchConsent"],
      });
    }
    if (
      (data.acceptStudentConsent && data.denyStudentConsent) ||
      (!data.acceptStudentConsent && !data.denyStudentConsent)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "You cannot both accept and deny student consent.",
        path: ["acceptStudentConsent"],
      });
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "You cannot both accept and deny student consent.",
        path: ["denyStudentConsent"],
      });
    }
  });
