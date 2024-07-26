import { UseFormReturn } from "react-hook-form";
import { CardTitle } from "@/components/ui/card";
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

const FHr = () => <hr className="my-4" />;

export type NameStepProps = {
  form: UseFormReturn<any>;
};

export function NameStep({ form }: NameStepProps) {
  const { textLarge, highContrast, dyslexicFont } = useThemeContext();

  return (
    <div className={textLarge ? "text-2xl" : "text-base"}>
      <CardTitle className={`pb-3 ${textLarge ? "text-3xl" : "text-xl"} ${dyslexicFont ? lexend.className : ""}`}>Personal Information and Contact</CardTitle>
      <FHr />
      <FormField
        control={form.control}
        name="name"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className={`pb-3 ${textLarge ? "text-xl" : ""} ${dyslexicFont ? lexend.className : ""}`}>Full name</FormLabel>
            <FormControl>
              <Input className={`pb-3 ${textLarge ? "text-xl" : ""} ${dyslexicFont ? lexend.className : ""}`} placeholder="Enter your name" {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className='text-red-500'>
                {fieldState.error.message}
              </FormMessage>
            )}
          </FormItem>
        )}
      />
      <br />
      <FormField
        control={form.control}
        name="email"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className={`pb-3 ${textLarge ? "text-xl" : ""} ${dyslexicFont ? lexend.className : ""}`}>Email</FormLabel>
            <FormControl>
              <Input className={`pb-3 ${textLarge ? "text-xl" : ""} ${dyslexicFont ? lexend.className : ""}`} placeholder="Enter your email" {...field} />
            </FormControl>
            {fieldState.error && (
              <FormMessage className='text-red-500'>
                {fieldState.error.message}
              </FormMessage>
            )}
          </FormItem>
        )}
      />
    </div>
  );
}