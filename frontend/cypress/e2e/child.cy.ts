describe('NameStep Component', () => {
    beforeEach(() => {
        cy.visit('http://localhost:3000/');
    });

    it('should allow switching to the child form', () => {
        cy.contains('Click for Child Form').click();
        cy.contains('Patient\'s Consent & Information Sheet (Children)').should('be.visible');
    });

    describe('After switching to the child form', () => {
        beforeEach(() => {
            cy.contains('Click for Child Form').click();
        });

        it('should display the name and email fields', () => {
            cy.get('input[name="name"]').should('be.visible');
            cy.get('input[name="email"]').should('be.visible');
        });

        it('should display validation errors when fields are empty', () => {
            cy.contains('button', 'Next Page').click();
            cy.contains('Please enter a name').should('be.visible');
            cy.contains('Invalid email').should('be.visible');
        });

        it('should allow typing in the name and email fields', () => {
            cy.get('input[name="name"]').type('John Doe').should('have.value', 'John Doe');
            cy.get('input[name="email"]').type('john.doe@example.com').should('have.value', 'john.doe@example.com');
            cy.contains('button', 'Next Page').click();
        });

        describe('After filling name and email', () => {
            beforeEach(() => {
                cy.get('input[name="name"]').type('John Doe').should('have.value', 'John Doe');
                cy.get('input[name="email"]').type('john.doe@example.com').should('have.value', 'john.doe@example.com');
                cy.contains('button', 'Next Page').click();
            });

            it('should display validation errors when both checkboxes are chosen', () => {
                cy.contains('I CONSENT').click();
                cy.contains('I DO NOT CONSENT').click();
                cy.contains('button', 'Next Page').click();
                cy.contains('Please select ONE option').should('be.visible');
            });


            it('should display validation errors when consent checkboxes are not checked correctly', () => {
                cy.contains('button', 'Next Page').click();
                cy.contains('Please select ONE option').should('be.visible');
            });

            it('should correctly handle the consent form', () => {
                cy.contains('I CONSENT to the use of my de-identified* clinical information for the purpose of research').click();
                cy.contains('button', 'Next Page').click();
                cy.contains('I CONSENT to be contacted with invitations to take part in teaching or clinical studies').click();
                cy.contains('button', 'Next Page').click();
                cy.contains('I CONSENT to be examined by a student under supervision').click();
            });

            describe('After filling out the consent section', () => {
                beforeEach(() => {
                    cy.contains('I CONSENT to the use of my de-identified* clinical information for the purpose of research').click();
                    cy.contains('button', 'Next Page').click();
                    cy.contains('I CONSENT to be contacted with invitations to take part in teaching or clinical studies').click();
                    cy.contains('button', 'Next Page').click();
                    cy.contains('I CONSENT to be examined by a student under supervision').click();
                    cy.contains('button', 'Review').click();
                });

                it('should display validation errors when no signature is present', () => {
                    cy.contains('button', 'Submit').click();
                    cy.contains('Please draw your signature to sign').should('be.visible');
                });

                it('should allow drawing a signature', () => {
                    cy.get('canvas')
                        .then($canvas => {
                            const canvas = $canvas[0];
                            const rect = canvas.getBoundingClientRect();

                            cy.wrap(canvas)
                                .trigger('mousedown', {
                                    which: 1,
                                    clientX: rect.left + 10,
                                    clientY: rect.top + 10,
                                })
                                .trigger('mousemove', {
                                    which: 1,
                                    clientX: rect.left + 50,
                                    clientY: rect.top + 50,
                                })
                                .trigger('mouseup');
                        });
                    cy.contains('button', 'Submit').click();
                    cy.contains('button', 'Restart').click();
                });
            });
        });
    });
});