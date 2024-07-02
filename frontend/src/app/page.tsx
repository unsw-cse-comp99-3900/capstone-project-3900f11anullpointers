"use client";
import { Inter } from "next/font/google";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { consentSchema } from "@/validators/auth";
import { useToast } from "@/components/ui/use-toast";
import { Form } from "@/components/ui/form";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { cn } from "@/lib/utils";
import { ArrowRight } from "lucide-react";
import { useState } from "react";
import { CardHeaderContent } from "@/components/CardHeaderContent";
import { FormStep1 } from "@/components/FormStep1";
import { FormStep2 } from "@/components/FormStep2";
import { FormButtons } from "@/components/FormButtons";

const inter = Inter({ subsets: ["latin"] });
type Input = z.infer<typeof consentSchema>;

export default function Home() {
  const [formStep, setFormStep] = useState(0);
  const { toast } = useToast();
  const form = useForm<Input>({
    resolver: zodResolver(consentSchema),
    defaultValues: {
      email: "",
      name: "",
      acceptResearchConsent: false,
      denyResearchConsent: false,
      acceptStudentConesent: false,
      denyStudentConsent: false,
    },
  });

  function onSubmit(data: Input) {
    if (!data.signature) {
      return;
    }
    {
      /**
      INSERT BACKEND COMMUNICATION HERE
      INSERT BACKEND COMMUNICATION HERE
      INSERT BACKEND COMMUNICATION HERE
      */
    }
    alert(JSON.stringify(data, null, 4));
    console.log(data);
  }

  return (
    <div className='absolute -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 sm:w-11/12 md:w-auto'>
      <Card className=''>
        <CardHeaderContent />
        <CardContent className='relative min-h-[400px]'>
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className='relative space-y-3 overflow-hidden'
            >
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
                <div className='w-full flex-shrink-0'>
                  <FormStep1 form={form} />
                </div>
                <div className='w-full flex-shrink-0'>
                  <FormStep2 form={form} />
                </div>
              </motion.div>
              <FormButtons formStep={formStep} setFormStep={setFormStep} />
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
