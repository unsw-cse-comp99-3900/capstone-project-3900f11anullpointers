import * as React from "react";
import { Button } from "./button";
import { cn } from "@/lib/utils";
import SignaturePad from "react-signature-canvas";
import { useThemeContext } from "@/context/theme-context";
import { Lexend } from "next/font/google";

const lexend = Lexend({ subsets: ["latin"] });

interface SignatureInputProps {
  className?: string;
  field: any;
}

const SignatureInput = React.forwardRef<SignaturePad, SignatureInputProps>(
  ({ className, field }, ref) => {
    const sigCanvas = React.useRef<SignaturePad>(null);

    const clear = React.useCallback(() => {
      sigCanvas.current?.clear();
      field.onChange("");
    }, [field]);

    const save = () => {
      const trimmedDataURL =
        sigCanvas.current?.getCanvas().toDataURL("image/png") || null;
      field.onChange(trimmedDataURL);
    };

    React.useEffect(() => {
      const handleClearSignature = () => {
        clear();
      };

      window.addEventListener("clearSignature", handleClearSignature);

      return () => {
        window.removeEventListener("clearSignature", handleClearSignature);
      };
    }, [clear]);

    const { textLarge, highContrast, dyslexicFont } = useThemeContext();

    return (
      <div className="items-center no-select">
        <SignaturePad
          ref={sigCanvas}
          onEnd={save}
          canvasProps={{
            className: cn(
              "border border-input bg-white rounded-md touch-none w-full h-28",
              className
            ),
          }}
          clearOnResize={false}
        />
        <div className="flex mt-4 space-x-2">
          <Button
            onClick={clear}
            variant="outline"
            className={`${textLarge ? "text-xl" : "text-sm"} ${
              dyslexicFont ? lexend.className : ""
            }`}
          >
            Clear
          </Button>
        </div>
      </div>
    );
  }
);

SignatureInput.displayName = "SignatureInput";

export { SignatureInput };
