# UNSW Optometry Clinic - Electronic consent form

### Context
All new patients at the UNSW Optometry Clinic are required to sign a consent form when attending their initial appointment.

### Problem
At the moment, patients complete and sign a paper consent form, that reception scans, emails and attaches to the patient record in a patient management system. This is too manual and time consuming for clinic staff.

### Solution
Digitise the form process as an electronic consent form that can be filled out on a clinic iPad, and is automatically exported to the clinic inbox.

### Folder Structure

```
.
├── README.md
├── backend
│   ├── .env
│   ├── .env.local
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── src
│   │   ├── doc_printing.py
│   │   ├── fonts
│   │   │   ├── Roboto-*.ttf
│   │   │   ├── font_config.json
│   │   │   └── fonts.py
│   │   ├── form_text
│   │   │   ├── adult.json
│   │   │   └── child.json
│   │   ├── logo
│   │   │   └── logo.png
│   │   ├── pdf_gen.py
│   │   └── send_email.py
│   └── tests
│       ├── run_tests.py
│       └── test_*.py
├── docker-compose.yml
├── frontend
│   ├── .env.local
│   ├── Dockerfile
│   ├── __tests__
│   │   └── *.test.tsx
│   ├── cypress
│   │   └── e2e
│   │       ├── adult.cy.ts
│   │       └── child.cy.ts
│   ├── package.json
│   ├── public
│   │   └── unsw_logo.png
│   ├── src
│   │   ├── app
│   │   │   ├── child-form
│   │   │   │   └── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components
│   │   │   ├── *.tsx
│   │   │   └── ui
│   │   │       └── *.tsx
│   │   ├── context
│   │   │   └── theme-context.tsx
│   │   ├── forms
│   │   │   ├── AdultFormStepConfig.tsx
│   │   │   └── ChildFormStepConfig.tsx
│   │   └── validators
│   │       ├── adult-auth.ts
│   │       └── child-auth.ts
│   └── tsconfig.json
└── package.json
```
