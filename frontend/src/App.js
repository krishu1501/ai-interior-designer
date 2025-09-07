import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/search/${query}/${maxResults}`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Amazon Product Scraper</h1>
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter search term"
          />
          <input
            type="number"
            value={maxResults}
            onChange={(e) => setMaxResults(e.target.value)}
            placeholder="Max results"
            min="1"
            max="50"
          />
          <button type="submit">Search</button>
        </form>
      </header>
      <main>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="products-grid">
            {products.map((product, index) => (
              <div key={index} className="product-card">
                <img src={product.image} alt={product.title} />
                <h3>{product.title}</h3>
                <p className="price">{product.price}</p>
                <a href={product.url} target="_blank" rel="noopener noreferrer">
                  View on Amazon
                </a>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
