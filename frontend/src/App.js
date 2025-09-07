import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [theme, setTheme] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const themes = ['relaxed', 'vintage', 'calm', 'modern', 'gadget freak'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('image', image);
    formData.append('theme', theme || 'modern');

    try {
      const response = await axios.post('http://localhost:8000/api/design-room', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Room Designer AI</h1>
      </header>
      
      <main className="container">
        <form onSubmit={handleSubmit} className="design-form">
          <div className="file-input">
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files[0])}
              required
            />
            {image && (
              <img 
                src={URL.createObjectURL(image)} 
                alt="Room preview" 
                className="preview-image"
              />
            )}
          </div>
          
          <input
            type="text"
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            placeholder="Choose a theme (e.g., modern, vintage)"
            list="themes"
            className="theme-input"
          />
          <datalist id="themes">
            {themes.map(t => <option key={t} value={t} />)}
          </datalist>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Design Room'}
          </button>
        </form>

        {result && (
          <div className="results">
            <div className="images-container">
              {image && (
                <div className="image-box">
                  <h3>Original Room</h3>
                  <img src={URL.createObjectURL(image)} alt="Original room" />
                </div>
              )}
              <div className="image-box">
                <h3>Redesigned Room</h3>
                <img 
                  src={`data:image/jpeg;base64,${result.newImage}`}
                  alt="Redesigned room"
                />
              </div>
            </div>

            <div className="suggestions">
              <h2>Suggested Changes</h2>
              <div className="products-grid">
                {result.suggestions.map((item, index) => (
                  <div key={index} className="product-card">
                    {item.amazonDetails && (
                      <>
                        <img src={item.amazonDetails.image} alt={item.newProduct} />
                        <h3>{item.newProduct}</h3>
                        {item.oldProduct && (
                          <p className="replace-text">
                            Replaces: {item.oldProduct}
                          </p>
                        )}
                        <p className="price">{item.amazonDetails.price}</p>
                        <a 
                          href={item.amazonDetails.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                        >
                          View on Amazon
                        </a>
                      </>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
