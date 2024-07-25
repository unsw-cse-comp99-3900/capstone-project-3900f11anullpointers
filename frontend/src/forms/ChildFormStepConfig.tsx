import { UseFormReturn } from "react-hook-form";
import { ConsentStep } from "@/components/formSteps/ConsentStep";
import { NameStep } from "@/components/formSteps/NameStep";
import { SuccessStep } from "@/components/formSteps/SuccessStep";
import { ReviewStep } from "@/components/formSteps/ReviewStep";

export type FormStepProps = {
  form: UseFormReturn<any>;
  [key: string]: any;
};

export type FormStepConfig = {
  component: any;
  props: { [key: string]: any };
};

export const formSteps: FormStepConfig[] = [
  {
    component: NameStep,
    props: {},
  },
  {
    component: ConsentStep,
    props: {
      title: "Use of Clinical Information in Research Studies",
      preDescription: `Please indicate below whether you give consent for your child's
        de-identified* information being used for teaching and research
        purposes. This has no bearing on your child's clinical care.`,
      checkboxes: {
        checkbox1: {
          name: "acceptResearchConsent",
          labelText:
            "I CONSENT to the use of my child's de-identified* clinical information for the purpose of research",
          descriptionText: "",
        },
        checkbox2: {
          name: "denyResearchConsent",
          labelText:
            "I DO NOT CONSENT to the use of my child's de-identified* clinical information for the purpose of research",
          descriptionText: "",
        },
      },
      description:
        "*De-identified means we will exclude your child's name and contact details from the research database",
    },
  },
  {
    component: ConsentStep,
    props: {
      title: "Use of Clinical Information in Research Studies",
      preDescription: `I acknowledge that I have been informed that my child's initial eye
        examination and subsequent care in the UNSW Optometry Clinic will be
        conducted by an optometry student under the supervision of a qualified,
        APHRA registered optometrist.`,
      checkboxes: {
        checkbox1: {
          name: "acceptStudentConsent",
          labelText:
            "I CONSENT to my child being examined by a student under supervision",
          descriptionText: "",
        },
        checkbox2: {
          name: "denyStudentConsent",
          labelText:
            "I DO NOT CONSENT to my child being examined by a student under supervision",
          descriptionText: "",
        },
      },
      description:
        "*De-identified means we will exclude your child's name and contact details from the research database",
    },
  },
  {
    component: ReviewStep,
    props: {
      showResearchConsent: true,
      showContactConsent: false,
      showStudentConsent: true,
    },
  },
  {
    component: SuccessStep,
    props: {},
  },
];
