"use client";

import { UseFormReturn } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";

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
  submitButtonText,
  mobileSettingsLink,
}: CheckboxWithTextProps) {
  return (
    <form onSubmit={form.handleSubmit((data) => console.log(data))} className='space-y-6'>
      <FormField
        control={form.control}
        name='mobile'
        render={({ field }) => (
          <FormItem className='flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4'>
            <FormControl>
              <Checkbox
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </FormControl>
            <div className='space-y-1 leading-none'>
              <FormLabel>{checkbox1.labelText}</FormLabel>
              <FormDescription>
                {checkbox1.descriptionText}
              </FormDescription>
            </div>
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name='notifications'
        render={({ field }) => (
          <FormItem className='flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4'>
            <FormControl>
              <Checkbox
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </FormControl>
            <div className='space-y-1 leading-none'>
              <FormLabel>{checkbox2.labelText}</FormLabel>
              <FormDescription>
                {checkbox2.descriptionText}{" "}
              </FormDescription>
            </div>
          </FormItem>
        )}
      />
      {/* <Button type='submit'>{submitButtonText}</Button> */}
    </form>
  );
}
