const ProgressBar = ({ step, totalSteps }: { step: number, totalSteps: number }) => {
    const progress = (step / (totalSteps)) * 100;

    return (
        <div className="w-full bg-secondary rounded-full h-2.5">
            <div
                className="bg-secondary-foreground h-2.5 rounded-full transition-width duration-300"
                style={{ width: `${progress}%` }}
             />
        </div>
    );
};

export default ProgressBar;