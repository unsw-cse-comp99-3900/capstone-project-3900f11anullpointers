import * as React from "react";
import { Button } from "./button";
import { cn } from "@/lib/utils";
import SignaturePad from "react-signature-canvas";

interface SignatureInputProps {
  className?: string;
  field: any;
}

const SignatureInput = React.forwardRef<SignaturePad, SignatureInputProps>(
  ({ className, field }, ref) => {
    const sigCanvas = React.useRef<SignaturePad>(null);

    const clear = () => {
      sigCanvas.current?.clear();
      field.onChange("");
    };

    const save = () => {
      const trimmedDataURL =
        sigCanvas.current?.getTrimmedCanvas().toDataURL("image/png") || null;
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
    }, []);

    return (
      <div className="items-center no-select">
        <SignaturePad
          ref={sigCanvas}
          onEnd={save}
          canvasProps={{
            className: cn(
              "border border-input bg-background rounded-md touch-none w-full h-28",
              className
            ),
          }}
        />
        <div className="flex mt-4 space-x-2">
          <Button onClick={clear} variant="outline">
            Clear
          </Button>
        </div>
      </div>
    );
  }
);

SignatureInput.displayName = "SignatureInput";

export { SignatureInput };
