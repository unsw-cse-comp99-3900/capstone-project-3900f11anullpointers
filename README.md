## Project Structure

Below is the structure of the project:

```plaintext

.
├── README.md
├── backend
│   ├── Dockerfile
│   ├── __init__.py
│   ├── app.py
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── doc_printing.py
│       ├── fonts
│       │   ├── Roboto-Black.pkl
│       │   ├── Roboto-Black.ttf
│       │   ├── Roboto-Bold.pkl
│       │   ├── Roboto-Bold.ttf
│       │   ├── Roboto-Regular.cw127.pkl
│       │   ├── Roboto-Regular.pkl
│       │   ├── Roboto-Regular.ttf
│       │   ├── __init__.py
│       │   ├── font_config.json
│       │   └── fonts.py
│       ├── form_text
│       │   ├── adult.json
│       │   └── child.json
│       ├── logo
│       │   ├── logo.png
│       │   └── old_logo.png
│       ├── pdf_gen.py
│       ├── send_email.py
│       ├── signatures
│       │   └── test1.png
│       └── tests
│           ├── test_doc_printing.py
│           └── test_fonts.py
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── components.json
│   ├── next-env.d.ts
│   ├── next.config.mjs
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── public
│   │   ├── next.svg
│   │   ├── unsw_logo.png
│   │   └── vercel.svg
│   ├── src
│   │   ├── app
│   │   │   ├── child-form
│   │   │   │   ├── components
│   │   │   │   │   ├── CardHeaderContent.tsx
│   │   │   │   │   ├── FormButtons.tsx
│   │   │   │   │   └── Forms.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components
│   │   │   ├── CardHeaderContent.tsx
│   │   │   ├── CheckboxWithText.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── FormButtons.tsx
│   │   │   ├── Forms.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── ModeToggle.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   ├── RadioWithText.tsx
│   │   │   ├── Steven-Forms.tsx
│   │   │   ├── TimeoutFeature.css
│   │   │   ├── TimeoutFeature.tsx
│   │   │   └── ui
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── checkbox.tsx
│   │   │       ├── dropdown-menu.tsx
│   │   │       ├── form.tsx
│   │   │       ├── input.tsx
│   │   │       ├── label.tsx
│   │   │       ├── radio-group.tsx
│   │   │       ├── select.tsx
│   │   │       ├── signature-input.tsx
│   │   │       ├── toast.tsx
│   │   │       ├── toaster.tsx
│   │   │       └── use-toast.ts
│   │   ├── context
│   │   │   └── theme-context.tsx
│   │   ├── lib
│   │   │   └── utils.ts
│   │   ├── styles
│   │   │   ├── accessibility.css
│   │   │   └── globals.css
│   │   └── validators
│   │       ├── adult-auth.ts
│   │       └── child-auth.ts
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── package-lock.json
├── package.json
└── structure.txt
```
