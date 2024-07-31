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
      preDescription: "",
      checkboxes: {
        checkbox1: {
          name: "acceptResearchConsent",
          labelText:
            "I CONSENT to the use of my de-identified* clinical information for the purpose of research",
          descriptionText: "",
        },
        checkbox2: {
          name: "denyResearchConsent",
          labelText:
            "I DO NOT CONSENT to the use of my de-identified* clinical information for the purpose of research",
          descriptionText: "",
        },
      },
      postDescription:
        "*De-identified means we will exclude your name and contact details from the research database",
    },
  },
  {
    component: ConsentStep,
    props: {
      title: "Contact for Future Research Studies",
      preDescription: "",
      checkboxes: {
        checkbox1: {
          name: "acceptContactConsent",
          labelText:
            "I CONSENT to be contacted with invitations to take part in teaching or clinical studies",
          descriptionText: "",
        },
        checkbox2: {
          name: "denyContactConsent",
          labelText:
            "I DO NOT CONSENT to be contacted with invitations to take part in teaching or clinical studies",
          descriptionText: "",
        },
      },
      postDescription:
        "",
    },
  },
  {
    component: ConsentStep,
    props: {
      title: "Student Clinic Consent",
      preDescription: "I acknowledge that I have been informed that the initial eye examination and subsequent care in the UNSW Optometry Clinic that I will receive, will be conducted by an optometry student under the supervision of a qualified, AHPRA registered optometrist.",
      checkboxes: {
        checkbox1: {
          name: "acceptStudentConsent",
          labelText: "I CONSENT to be examined by a student under supervision",
          descriptionText: "",
        },
        checkbox2: {
          name: "denyStudentConsent",
          labelText:
            "I DO NOT CONSENT to be examined by a student under supervision",
          descriptionText: "",
        },
      },
      postDescription:
        "",
    },
  },
  {
    component: ReviewStep,
    props: {
      showResearchConsent: true,
      showContactConsent: true,
      showStudentConsent: true,
    },
  },
  {
    component: SuccessStep,
    props: {},
  },
];
