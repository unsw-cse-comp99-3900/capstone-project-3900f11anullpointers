"use client";

import { UseFormReturn } from "react-hook-form";
import { Checkbox } from "@/components/ui/checkbox";
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useThemeContext } from "@/context/theme-context";

type CheckboxWithTextProps = {
  form: UseFormReturn<any>;
  checkbox1: {
    name: string;
    labelText: string;
    descriptionText: string;
  };
  checkbox2: {
    name: string;
    labelText: string;
    descriptionText: string;
  };
};

export function CheckboxWithText({
  form,
  checkbox1,
  checkbox2,
}: CheckboxWithTextProps) {
  const { textLarge, highContrast } = useThemeContext();
  
  const { errors } = form.formState;

  const consentErrors = [
    errors.acceptResearchConsent,
    errors.denyResearchConsent,
    errors.acceptContactConsent,
    errors.denyContactConsent,
    errors.acceptStudentConsent,
    errors.denyStudentConsent,
  ].filter(Boolean);

  return (
    <div className='space-y-6'>
      <FormField
        control={form.control}
        name={checkbox1.name}
        render={({ field, fieldState }) => (
          <FormItem className='flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4'>
            <FormControl>
              <Checkbox
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </FormControl>
            <div className='space-y-1 leading-none'>
              <FormLabel className={`${textLarge ? "text-xl" : "text-base"} ${highContrast ? "filter contrast-200" : ""}`}>{checkbox1.labelText}</FormLabel>
              <FormDescription>
                {checkbox1.descriptionText}
              </FormDescription>
            </div>
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name={checkbox2.name}
        render={({ field, fieldState }) => (
          <FormItem className='flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4'>
            <FormControl>
              <Checkbox
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </FormControl>
            <div className='space-y-1 leading-none'>
              <FormLabel className={textLarge ? "text-xl" : "text-base"}>{checkbox2.labelText}</FormLabel>
              <FormDescription>
                {checkbox2.descriptionText}
              </FormDescription>
            </div>
          </FormItem>
        )}
      />
      {consentErrors.length > 0 && (
        <FormMessage className='text-red-500'>
          Please select ONE option.
        </FormMessage>
      )}
    </div>
  );
}
