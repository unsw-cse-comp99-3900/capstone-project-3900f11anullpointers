"use client";
import { Inter } from "next/font/google";
import { motion } from "framer-motion";
import { consentSchema } from "@/validators/adult-auth";
import { useForm, FormProvider } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import {
  Card,
  CardContent,
  CardFooter
} from "@/components/ui/card";
import { CardHeaderContent } from "@/components/CardHeaderContent";
import { FormStep0, FormStep1, FormStep2, FormStep3, FormReviewStep, FormSuccess } from "@/components/Forms";
import { FormButtons } from "@/components/FormButtons";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Toaster } from "@/components/ui/toaster";

import { Lexend } from "next/font/google";
import { useThemeContext } from "@/context/theme-context";

type Input = z.infer<typeof consentSchema>;

const lexend = Lexend({ subsets: ["latin"] });

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
      signature: ""
    },
  });


  const { dyslexicFont, highContrast, textLarge } = useThemeContext();

  async function onSubmit(data: Input) {
    console.log(data);
  }

  const handleRestart = () => {
    form.reset();
    setFormStep(0);
    setIsSubmitted(false);
  };

  const formSteps: { [key: string]: React.ComponentType<{ form: any }> } = {
    "0": FormStep0,
    "1": FormStep1,
    "2": FormStep2,
    "3": FormStep3,
    "4": FormReviewStep,
    "5": FormSuccess,
  };

  return (
    <main className={`flex min-h-screen flex-col items-center justify-between ${dyslexicFont ? lexend.className : ""} ${highContrast ? "filter contrast-200" : ""} ${textLarge ? "text-3xl" : ""}`}>
      <div className="flex flex-col items-center justify-center w-full max-w-xl mx-auto m-5 p-4 sm:p-6 md:p-8">
        <Card className="w-full">
          {isSubmitted ? (
            <CardContent>
              <FormSuccess />
            </CardContent>
          ) : (
            <>
              <CardHeaderContent step={formStep} totalSteps={Object.keys(formSteps).length - 1} />
              <CardContent>
                <FormProvider {...form}>
                  <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-3 overflow-hidden"
                  >
                    <div className="flex flex-col space-between">
                      <motion.div
                        className="flex w-full"
                        initial={false}
                        animate={{
                          x: `-${formStep * 100}%`,
                        }}
                        transition={{
                          ease: "easeInOut",
                          duration: 0.5,
                        }}
                      >
                        {Object.keys(formSteps).map((key) => {
                          const StepComponent = formSteps[key];
                          return (
                            <div key={key} className="w-full flex-shrink-0 p-3">
                              <StepComponent form={form} />
                            </div>
                          );
                        })}
                      </motion.div>
                    </div>
                  </form>
                </FormProvider>
              </CardContent>
              <CardFooter>
                <div className="w-full">
                  <FormProvider {...form}>
                    <FormButtons formStep={formStep} setFormStep={setFormStep} isLoading={isLoading} setIsLoading={setIsLoading} setIsSubmitted={setIsSubmitted} handleRestart={handleRestart} />
                  </FormProvider>
                </div>
              </CardFooter>
            </>
          )}
        </Card>
        <Toaster />
      </div>
    </main>
  );
}
