"use client";
import { Inter } from "next/font/google";
import { motion } from "framer-motion";
import { consentSchema } from "@/validators/adult-auth";
import { useForm, FormProvider } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { CardHeaderContent } from "@/components/CardHeaderContent";
import { FormButtons } from "@/components/FormButtons";
import { Toaster } from "@/components/ui/toaster";
import TimeoutFeature from "@/components/TimeoutFeature";
import { StepWrapper } from "@/components/StepWrapper";
import { formSteps } from "../forms/AdultFormStepConfig";
import { SuccessStep } from "@/components/formSteps/SuccessStep";

type Input = z.infer<typeof consentSchema>;

export default function Home() {
  const [formStep, setFormStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const form = useForm<Input>({
    resolver: zodResolver(consentSchema),
    defaultValues: {
      email: "",
      name: "",
      formType: "adult",
      acceptResearchConsent: false,
      denyResearchConsent: false,
      acceptContactConsent: false,
      denyContactConsent: false,
      acceptStudentConsent: false,
      denyStudentConsent: false,
      drawSignature: "",
    },
  });

  async function onSubmit(data: Input) {
    console.log(data);
  }

  const handleRestart = () => {
    form.reset();
    setFormStep(0);
    setIsSubmitted(false);

    window.dispatchEvent(new Event("clearSignature"));
  };

  return (
    <main className='flex min-h-screen flex-col items-center justify-between'>
      <div className='flex flex-col items-center justify-center w-full max-w-xl mx-auto m-5 p-4 sm:p-6 md:p-8'>
        <Card className='w-full'>
          {isSubmitted ? (
            <CardContent>
              <SuccessStep />
            </CardContent>
          ) : (
            <>
              <CardHeaderContent
                step={formStep}
                totalSteps={formSteps.length - 1}
                title='Patient Consent & Information Sheet'
                description='The UNSW Optometry Clinic is part of the School of Optometry and Vision 
                Science, UNSW Australia. It is a teaching facility for both undergraduate and 
                postgraduate optometry students, providing excellence in eye care and is at the 
                forefront of the latest research.'
              />
              <CardContent>
                <FormProvider {...form}>
                  <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className='space-y-3 overflow-hidden'
                  >
                    <div className='relative w-full overflow-hidden'>
                      <motion.div
                        className='flex w-full'
                        initial={false}
                        animate={{
                          x: `-${formStep * 100}%`,
                        }}
                        transition={{
                          ease: "easeInOut",
                          duration: 0.5,
                        }}
                      >
                        {formSteps.map((_, index) => (
                          <div key={index} className='w-full flex-shrink-0 p-3'>
                            <StepWrapper form={form} step={index} />
                          </div>
                        ))}
                      </motion.div>
                    </div>
                  </form>
                </FormProvider>
              </CardContent>
              <CardFooter>
                <div className='w-full'>
                  <FormProvider {...form}>
                    <FormButtons
                      formStep={formStep}
                      setFormStep={setFormStep}
                      isLoading={isLoading}
                      setIsLoading={setIsLoading}
                      setIsSubmitted={setIsSubmitted}
                      handleRestart={handleRestart}
                    />
                  </FormProvider>
                </div>
              </CardFooter>
            </>
          )}
        </Card>
        <Toaster />
      </div>
      <TimeoutFeature />
    </main>
  );
}
