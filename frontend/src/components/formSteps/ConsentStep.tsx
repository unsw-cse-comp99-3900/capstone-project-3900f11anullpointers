import { UseFormReturn } from "react-hook-form";
import { CheckboxWithText, CheckboxWithTextProps } from "@/components/CheckboxWithText";
import { CardDescription, CardTitle } from "@/components/ui/card";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

const FHr = () => <hr className="my-4" />;

export type ConsentStepProps = {
  form: UseFormReturn<any>;
  title: string;
  checkboxes: CheckboxWithTextProps;
  preDescription: string;
  postDescription: string;
};

export function ConsentStep({ form, title, checkboxes, postDescription, preDescription }: ConsentStepProps) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className={textLarge ? "text-2xl" : "text-base"}>
      <CardTitle className={`pb-3 ${textLarge ? "text-3xl" : "text-xl"} ${dyslexicFont ? lexend.className : ""}`}>
        {title}
      </CardTitle>
      <FHr />
      <CardDescription className={`pb-3 ${textLarge ? "text-xl" : "text-base"} ${highContrast ? "filter contrast-200" : ""} ${dyslexicFont ? lexend.className : ""}`}>
        {preDescription}
      </CardDescription>
      <CheckboxWithText
        form={form}
        checkbox1={checkboxes.checkbox1}
        checkbox2={checkboxes.checkbox2}
      />
      <br />
      <CardDescription className={`${textLarge ? "text-xl" : "text-base"} ${highContrast ? "filter contrast-200" : ""} ${dyslexicFont ? lexend.className : ""}`}>
        {postDescription}
      </CardDescription>
    </div>
  );
}
