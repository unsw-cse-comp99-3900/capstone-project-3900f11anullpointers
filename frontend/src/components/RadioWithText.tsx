"use client";

import { UseFormReturn } from "react-hook-form";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useThemeContext } from "@/context/theme-context";

type RadioWithTextProps = {
  form: UseFormReturn<any>;
  radioOptions: {
    name: string;
    options: {
      value: string;
      labelText: string;
      descriptionText: string;
    }[];
  };
};

export function RadioWithText({
  form,
  radioOptions,
}: RadioWithTextProps) {
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
        name={radioOptions.name}
        render={({ field, fieldState }) => (
          <FormItem className='rounded-md border p-4'>
            <FormControl>
              <RadioGroup
                onValueChange={field.onChange}
                value={field.value}
              >
                {radioOptions.options.map((option) => (
                  <div key={option.value} className='flex items-start space-x-3 space-y-0'>
                    <RadioGroupItem value={option.value} id={option.value} />
                    <div className='space-y-1 leading-none'>
                      <Label
                        htmlFor={option.value}
                        className={`${textLarge ? "text-xl" : "text-base"} ${highContrast ? "filter contrast-200" : ""}`}
                      >
                        {option.labelText}
                      </Label>
                      <FormDescription>
                        {option.descriptionText}
                      </FormDescription>
                    </div>
                  </div>
                ))}
              </RadioGroup>
            </FormControl>
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
