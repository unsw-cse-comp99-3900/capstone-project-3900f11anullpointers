"use client";

import { UseFormReturn } from "react-hook-form";
import { Checkbox } from "@/components/ui/checkbox";
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { useThemeContext } from "@/context/theme-context";

type CheckboxWithTextProps = {
  form: UseFormReturn<any>;
  checkbox1: {
    labelText: string;
    descriptionText: string;
  };
  checkbox2: {
    labelText: string;
    descriptionText: string;
  };
  submitButtonText: string;
  mobileSettingsLink: string;
};

export function CheckboxWithText({
  form,
  checkbox1,
  checkbox2,
}: CheckboxWithTextProps) {
  const { textLarge, highContrast } = useThemeContext();
  
  return (
    <div className='space-y-6'>
      <FormField
        control={form.control}
        name='acceptResearchConsent'
        render={({ field }) => (
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
        name='denyResearchConsent'
        render={({ field }) => (
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
    </div>
  );
}
