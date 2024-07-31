import { CardDescription, CardTitle } from "../ui/card";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

export function SuccessStep() {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className={`text-center ${textLarge ? "text-2xl" : "text-base"}`}>
      <div>
        <CardTitle
          className={`mb-5 ${textLarge ? "text-2xl" : "text-base"} ${
            dyslexicFont ? lexend.className : ""
          }`}
        >
          Form Submitted Successfully
        </CardTitle>
        <CardDescription
          className={`${textLarge ? "text-xl" : "text-base"} ${
            highContrast ? "filter contrast-200" : ""
          } ${dyslexicFont ? lexend.className : ""}`}
        >
          Your information has been submitted successfully. Thank you!
        </CardDescription>
      </div>
    </div>
  );
}
