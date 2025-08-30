import React, { useState } from 'react';
import './App.css';

interface GenerateRequest {
  prompt: string;
  height: number;
  width: number;
  guidance_scale: number;
  num_inference_steps: number;
  seed?: number;
}

function App() {
  const [formData, setFormData] = useState<GenerateRequest>({
    prompt: '',
    height: 1024,
    width: 1024,
    guidance_scale: 4.0,
    num_inference_steps: 30,
  });
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiUrl, setApiUrl] = useState('http://localhost:8000');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'prompt' ? value : parseFloat(value)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedImage(null);

    try {
      const response = await fetch(`${apiUrl}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setGeneratedImage(imageUrl);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate image');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRandomSeed = () => {
    setFormData(prev => ({
      ...prev,
      seed: Math.floor(Math.random() * 1000000)
    }));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎨 Lumina Text-to-Image Generator</h1>
        <p>Transform your imagination into stunning visuals</p>
      </header>

      <main className="App-main">
        <div className="container">
          <div className="form-section">
            <form onSubmit={handleSubmit} className="generation-form">
              <div className="form-group">
                <label htmlFor="apiUrl">API URL:</label>
                <input
                  type="text"
                  id="apiUrl"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  placeholder="http://localhost:8000"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="prompt">Prompt:</label>
                <textarea
                  id="prompt"
                  name="prompt"
                  value={formData.prompt}
                  onChange={handleInputChange}
                  placeholder="Describe the image you want to generate..."
                  className="form-textarea"
                  rows={3}
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="height">Height:</label>
                  <input
                    type="number"
                    id="height"
                    name="height"
                    value={formData.height}
                    onChange={handleInputChange}
                    min="256"
                    max="2048"
                    step="64"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="width">Width:</label>
                  <input
                    type="number"
                    id="width"
                    name="width"
                    value={formData.width}
                    onChange={handleInputChange}
                    min="256"
                    max="2048"
                    step="64"
                    className="form-input"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="guidance_scale">Guidance Scale:</label>
                  <input
                    type="number"
                    id="guidance_scale"
                    name="guidance_scale"
                    value={formData.guidance_scale}
                    onChange={handleInputChange}
                    min="1"
                    max="20"
                    step="0.5"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="num_inference_steps">Inference Steps:</label>
                  <input
                    type="number"
                    id="num_inference_steps"
                    name="num_inference_steps"
                    value={formData.num_inference_steps}
                    onChange={handleInputChange}
                    min="10"
                    max="100"
                    step="5"
                    className="form-input"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="seed">Seed (optional):</label>
                <div className="seed-input-group">
                  <input
                    type="number"
                    id="seed"
                    name="seed"
                    value={formData.seed || ''}
                    onChange={handleInputChange}
                    placeholder="Leave empty for random"
                    className="form-input"
                  />
                  <button
                    type="button"
                    onClick={handleRandomSeed}
                    className="btn-secondary"
                  >
                    🎲 Random
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary"
              >
                {isLoading ? '🔄 Generating...' : '✨ Generate Image'}
              </button>
            </form>

            {error && (
              <div className="error-message">
                ❌ {error}
              </div>
            )}
          </div>

          <div className="image-section">
            {isLoading && (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Generating your image...</p>
              </div>
            )}

            {generatedImage && (
              <div className="generated-image-container">
                <h3>Generated Image</h3>
                <img
                  src={generatedImage}
                  alt="Generated from prompt"
                  className="generated-image"
                />
                <a
                  href={generatedImage}
                  download="lumina-generated-image.png"
                  className="btn-secondary"
                >
                  💾 Download Image
                </a>
              </div>
            )}

            {!isLoading && !generatedImage && (
              <div className="placeholder">
                <div className="placeholder-icon">🎨</div>
                <p>Your generated image will appear here</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>Powered by Lumina-Image-2.0 • Built with React & FastAPI</p>
      </footer>
    </div>
  );
}

export default App;
