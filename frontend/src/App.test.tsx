import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('Lumina Frontend', () => {
  test('renders the main heading', () => {
    render(<App />);
    const headingElement = screen.getByText(/🎨 Lumina Text-to-Image Generator/i);
    expect(headingElement).toBeInTheDocument();
  });

  test('renders the prompt input field', () => {
    render(<App />);
    const promptInput = screen.getByPlaceholderText(/Describe the image you want to generate/i);
    expect(promptInput).toBeInTheDocument();
  });

  test('renders the generate button', () => {
    render(<App />);
    const generateButton = screen.getByText(/✨ Generate Image/i);
    expect(generateButton).toBeInTheDocument();
  });

  test('allows entering a prompt', () => {
    render(<App />);
    const promptInput = screen.getByPlaceholderText(/Describe the image you want to generate/i);
    fireEvent.change(promptInput, { target: { value: 'A beautiful sunset' } });
    expect(promptInput).toHaveValue('A beautiful sunset');
  });

  test('shows error when submitting without prompt', async () => {
    render(<App />);
    const generateButton = screen.getByText(/✨ Generate Image/i);
    
    fireEvent.click(generateButton);
    
    await waitFor(() => {
      const errorMessage = screen.getByText(/Please enter a prompt/i);
      expect(errorMessage).toBeInTheDocument();
    });
  });

  test('renders parameter controls', () => {
    render(<App />);
    
    // Check for height and width inputs
    expect(screen.getByLabelText(/Height/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Width/i)).toBeInTheDocument();
    
    // Check for guidance scale and inference steps
    expect(screen.getByLabelText(/Guidance Scale/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Inference Steps/i)).toBeInTheDocument();
  });

  test('random seed button works', () => {
    render(<App />);
    const randomButton = screen.getByText(/🎲 Random/i);
    const seedInput = screen.getByPlaceholderText(/Leave empty for random/i) as HTMLInputElement;
    
    fireEvent.click(randomButton);
    
    expect(seedInput).toHaveValue();
    expect(Number(seedInput.value)).toBeGreaterThan(0);
  });

  test('API URL field is present and editable', () => {
  render(<App />);
    const apiUrlInput = screen.getByDisplayValue('https://lumina-backend-cwms2mqttq-el.a.run.app');
    expect(apiUrlInput).toBeInTheDocument();
    
    fireEvent.change(apiUrlInput, { target: { value: 'http://api.example.com' } });
    expect(apiUrlInput).toHaveValue('http://api.example.com');
  });
});
