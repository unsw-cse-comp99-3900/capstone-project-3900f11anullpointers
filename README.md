## Project Structure

Below is the structure of the project:

```plaintext

.
├── README.md
├── backend
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── src
│   │   ├── __init__.py
│   │   ├── doc_printing.py
│   │   ├── fonts
│   │   │   ├── Roboto-Black.pkl
│   │   │   ├── Roboto-Black.ttf
│   │   │   ├── Roboto-Bold.pkl
│   │   │   ├── Roboto-Bold.ttf
│   │   │   ├── Roboto-Regular.cw127.pkl
│   │   │   ├── Roboto-Regular.pkl
│   │   │   ├── Roboto-Regular.ttf
│   │   │   ├── __init__.py
│   │   │   ├── font_config.json
│   │   │   └── fonts.py
│   │   ├── form_text
│   │   │   ├── adult.json
│   │   │   └── child.json
│   │   ├── logo
│   │   │   ├── logo.png
│   │   │   └── old_logo.png
│   │   ├── pdf_gen.py
│   │   └── send_email.py
│   └── tests
│       ├── run_tests.py
│       ├── test_doc_printing.py
│       ├── test_flask_app.py
│       ├── test_fonts.py
│       ├── test_pdf_gen.py
│       └── test_send_email.py
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── Dockerfile.test
│   ├── README.md
│   ├── __tests__
│   │   ├── CardHeaderConsent.test.tsx
│   │   ├── CheckboxWithText.test.tsx
│   │   ├── Footer.test.tsx
│   │   ├── FormButtons.test.tsx
│   │   ├── Header.test.tsx
│   │   ├── ModeToggle.test.tsx
│   │   ├── ProgressBar.test.tsx
│   │   ├── ThemeProvider.test.tsx
│   │   └── TimeoutFeature.test.tsx
│   ├── components.json
│   ├── cypress
│   │   ├── e2e
│   │   │   ├── adult.cy.ts
│   │   │   └── child.cy.ts
│   │   ├── fixtures
│   │   │   └── example.json
│   │   └── support
│   │       ├── commands.ts
│   │       └── e2e.ts
│   ├── cypress.config.ts
│   ├── env.local
│   ├── jest.config.js
│   ├── jest.setup.js
│   ├── next-env.d.ts
│   ├── next.config.mjs
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── public
│   │   ├── next.svg
│   │   ├── unsw_logo.png
│   │   └── vercel.svg
│   ├── setupTests.d.ts
│   ├── src
│   │   ├── app
│   │   │   ├── child-form
│   │   │   │   ├── components
│   │   │   │   │   └── FormButtons.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components
│   │   │   ├── CardHeaderContent.tsx
│   │   │   ├── CheckboxWithText.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── FormButtons.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── ModeToggle.tsx
│   │   │   ├── NavigationButton.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   ├── StepWrapper.tsx
│   │   │   ├── TimeoutFeature.css
│   │   │   ├── TimeoutFeature.tsx
│   │   │   ├── formSteps
│   │   │   │   ├── ConsentStep.tsx
│   │   │   │   ├── NameStep.tsx
│   │   │   │   ├── ReviewStep.tsx
│   │   │   │   └── SuccessStep.tsx
│   │   │   └── ui
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── checkbox.tsx
│   │   │       ├── dialog.tsx
│   │   │       ├── dropdown-menu.tsx
│   │   │       ├── form.tsx
│   │   │       ├── input.tsx
│   │   │       ├── label.tsx
│   │   │       ├── radio-group.tsx
│   │   │       ├── select.tsx
│   │   │       ├── signature-input.tsx
│   │   │       ├── toast.tsx
│   │   │       ├── toaster.tsx
│   │   │       └── use-toast.ts
│   │   ├── context
│   │   │   └── theme-context.tsx
│   │   ├── deprecated
│   │   │   ├── RadioWithText.tsx
│   │   │   └── Steven-Forms.tsx
│   │   ├── forms
│   │   │   ├── AdultFormStepConfig.tsx
│   │   │   └── ChildFormStepConfig.tsx
│   │   ├── lib
│   │   │   └── utils.ts
│   │   ├── styles
│   │   │   ├── accessibility.css
│   │   │   └── globals.css
│   │   └── validators
│   │       ├── adult-auth.ts
│   │       └── child-auth.ts
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── package-lock.json
└── package.json
```
