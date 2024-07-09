"use client";
import React, { useState } from 'react';
import "../styles/accessibility.css";

const MainBody = () => {
  const [step, setStep] = useState(0);
  const [textSize, setTextSize] = useState('text-base');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    dob: '',
    consent: false,
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const totalSteps = 4;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleNext = () => {
    setStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setStep((prevStep) => prevStep - 1);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:3030/post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Network response was not ok');
      }

      const result = await response.json();
      console.log(result);
      setStep(4); // Proceed to the success message step
    } catch (error: unknown) {
      if (error instanceof Error) {
        console.error('There was a problem with your fetch operation:', error);
        setErrorMessage(error.message);
      } else {
        console.error('Unexpected error', error);
        setErrorMessage('An unexpected error occurred');
      }
      setIsModalOpen(true);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setErrorMessage('');
  };

  return (
    <div className="flex flex-col">
      <div className="flex-grow flex items-center justify-center">
        <div className={`max-w-3xl mx-auto p-8 font-roboto bg-primary-foreground shadow-md rounded-lg ${textSize}`}>
          <ProgressBar step={step} totalSteps={totalSteps} />
          <form onSubmit={handleSubmit} className="space-y-6">
            {step === 0 && (
              <div className="text-center py-16">
                <h2 className="text-xl mb-4 font-lora">Welcome to Our Consent Form</h2>
                <button type="button" onClick={handleNext} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition">
                  Begin
                </button>
              </div>
            )}
            {step === 1 && (
              <div className="space-y-6">
                <h2 className="text-2xl mb-4 font-lora">Personal Information</h2>
                <hr className="border-t-2 border-gray-300 mb-4"/>
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <label className="w-32 text-right" htmlFor="name">Name:</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      placeholder="Name"
                      value={formData.name}
                      onChange={handleChange}
                      className="flex-1 p-2 border rounded"
                      required
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <label className="w-32 text-right" htmlFor="email">Email:</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      placeholder="Email"
                      value={formData.email}
                      onChange={handleChange}
                      className="flex-1 p-2 border rounded"
                      required
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <label className="w-32 text-right" htmlFor="phone">Phone:</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      placeholder="Phone Number"
                      value={formData.phone}
                      onChange={handleChange}
                      className="flex-1 p-2 border rounded"
                      required
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <label className="w-32 text-right" htmlFor="address">Address:</label>
                    <input
                      type="text"
                      id="address"
                      name="address"
                      placeholder="Address"
                      value={formData.address}
                      onChange={handleChange}
                      className="flex-1 p-2 border rounded"
                      required
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <label className="w-32 text-right" htmlFor="dob">Date of Birth:</label>
                    <input
                      type="date"
                      id="dob"
                      name="dob"
                      placeholder="Date of Birth"
                      value={formData.dob}
                      onChange={handleChange}
                      className="flex-1 p-2 border rounded"
                      required
                    />
                  </div>
                </div>
                <hr className="border-t-2 border-gray-300 mt-4"/>
                <div className="flex justify-between mt-4">
                  <div className="flex-1"></div>
                  <button type="button" onClick={handleNext} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition">
                    Next
                  </button>
                </div>
              </div>
            )}
            {step === 2 && (
              <div className="space-y-6">
                <h2 className="text-2xl mb-4 font-lora">Consent</h2>
                <hr className="border-t-2 border-gray-300 mb-4"/>
                <div className="p-4 border rounded bg-gray-100 text-left">
                  <p className="mb-4">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean hendrerit dolor et tempus pretium. Nulla viverra egestas lectus. Fusce ullamcorper vestibulum consectetur. Nunc interdum molestie urna vel blandit. Ut tempus metus nec dui sollicitudin, eget malesuada neque pretium. Phasellus ac libero interdum, laoreet diam quis, tristique elit. Curabitur eleifend tincidunt lectus eget tristique. Sed ac dapibus augue. Vestibulum convallis ornare urna eu laoreet. Morbi et velit a quam sagittis dapibus ut condimentum lectus. Phasellus eget semper diam, ac semper metus. Sed tincidunt, purus at vulputate dictum, ligula orci varius neque, a pellentesque lectus velit sed libero. Donec iaculis tellus mauris, eu mattis arcu blandit sit amet. Praesent ornare condimentum hendrerit.
                  </p>
                  <p>
                    In rutrum sed leo vel placerat. Nam pellentesque elementum dolor eu convallis. Quisque dictum nunc turpis, sed dignissim enim mattis varius. Fusce vitae tincidunt leo. Praesent a enim quis nisl volutpat suscipit. Nulla porta tellus id lorem dapibus bibendum. Donec condimentum luctus dolor, et interdum libero sollicitudin porttitor. Nam eu elit posuere, tristique metus quis, condimentum dolor. Aenean molestie accumsan tellus quis vehicula. Etiam egestas hendrerit posuere. Maecenas et mauris ut lectus iaculis aliquet euismod nec eros. Duis vel est quam. Mauris nec volutpat tortor, et scelerisque orci. Pellentesque dapibus nulla non magna maximus facilisis a tempor augue.
                  </p>
                  <br />
                  <hr />
                  <br />
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      name="consent"
                      checked={formData.consent}
                      onChange={handleChange}
                      className="form-checkbox"
                      required
                    />
                    <span>I agree to the terms and conditions</span>
                  </label>
                </div>
                <div className="mt-6 p-4 border rounded bg-white text-left">
                  <p className="mb-2 font-bold">Signature:</p>
                  <div className="border border-gray-300 h-24"></div>
                </div>
                <hr className="border-t-2 border-gray-300 mt-4"/>
                <div className="flex justify-between mt-4">
                  <button type="button" onClick={handleBack} className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600 transition">
                    Back
                  </button>
                  <button type="button" onClick={handleNext} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition">
                    Next
                  </button>
                </div>
              </div>
            )}
            {step === 3 && (
              <div className="space-y-6">
                <h2 className="text-2xl mb-4 font-lora">Confirm Your Information</h2>
                <hr className="border-t-2 border-gray-300 mb-4"/>
                <div className="space-y-4">
                  <div>
                    <strong>Name:</strong> {formData.name}
                  </div>
                  <div>
                    <strong>Email:</strong> {formData.email}
                  </div>
                  <div>
                    <strong>Phone:</strong> {formData.phone}
                  </div>
                  <div>
                    <strong>Address:</strong> {formData.address}
                  </div>
                  <div>
                    <strong>Date of Birth:</strong> {formData.dob}
                  </div>
                  <div>
                    <strong>Consent:</strong> {formData.consent ? "Agreed" : "Not Agreed"}
                  </div>
                </div>
                <hr className="border-t-2 border-gray-300 mt-4"/>
                <div className="flex justify-between mt-4">
                  <button type="button" onClick={handleBack} className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600 transition">
                    Back
                  </button>
                  <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition">
                    Submit
                  </button>
                </div>
              </div>
            )}
            {step === 4 && (
              <div className="text-center py-16">
                <h2 className="text-2xl mb-4 font-lora">Form Submitted Successfully!</h2>
                <p className="mb-4">Thank you for submitting the consent form. We have received your information.</p>
                <button type="button" onClick={() => setStep(0)} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition">
                  Fill Another Form
                </button>
              </div>
            )}
          </form>
        </div>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl mb-4 font-lora">Error</h2>
            <p className="mb-4">{errorMessage}</p>
            <div className="flex justify-end">
              <button onClick={closeModal} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MainBody;



const ProgressBar = ({ step, totalSteps }: { step: number, totalSteps: number }) => {
  const progress = (step / totalSteps) * 100;

  return (
    <div className="w-full bg-gray-200 rounded-full h-2.5 mb-6">
      <div
        className="bg-blue-500 h-2.5 rounded-full transition-width duration-300"
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );
};
