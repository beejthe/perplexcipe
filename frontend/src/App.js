import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { ArrowPathIcon } from '@heroicons/react/24/solid';
import ProgressBar from "@ramonak/react-progress-bar";
import config from './config';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [recipe, setRecipe] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const simulateProgress = () => {
    return setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) return prev;
        return prev + Math.random() * 10;
      });
    }, 500);
  };

  useEffect(() => {
    // Reset progress when loading is complete
    if (!loading) {
      setTimeout(() => setProgress(0), 1000);
    }
  }, [loading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setLoading(true);
    setError('');
    setRecipe('');
    
    // Start progress simulation
    const progressInterval = simulateProgress();

    try {
      const response = await axios.post(`${config.apiUrl}/api/recipe`, { url }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.data && typeof response.data.recipe === 'string') {
        setRecipe(response.data.recipe);
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (err) {
      let errorMessage = 'An error occurred while processing your request.';
      
      if (err.response) {
        // Server responded with an error
        if (err.response.status === 404) {
          errorMessage = 'The recipe endpoint is not available. Please try again later.';
        } else if (err.response.data && typeof err.response.data.error === 'string') {
          errorMessage = err.response.data.error;
        }
      } else if (err.request) {
        // Request was made but no response received
        errorMessage = 'Unable to reach the server. Please check your internet connection.';
      } else {
        // Something else went wrong
        errorMessage = err.message || 'An unexpected error occurred.';
      }
      
      setError(errorMessage);
      setRecipe('');
    } finally {
      clearInterval(progressInterval);
      setProgress(100);
      setTimeout(() => {
        setLoading(false);
        setProgress(0);
      }, 500);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-orange-500 mb-2">Perplexcipe</h1>
          <p className="text-gray-300">Transform any recipe into its essential components</p>
        </header>

        <div className="max-w-2xl mx-auto">
          <form onSubmit={handleSubmit} className="mb-8">
            <div className="flex gap-4">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste your recipe URL here..."
                required
                className="flex-1 px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 focus:border-orange-500 focus:ring-1 focus:ring-orange-500 text-gray-100 placeholder-gray-400"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-orange-600 hover:bg-orange-700 rounded-lg font-medium transition-colors disabled:opacity-50 text-white"
              >
                {loading ? (
                  <ArrowPathIcon className="h-5 w-5 animate-spin" />
                ) : (
                  'Distill'
                )}
              </button>
            </div>
          </form>

          {loading && (
            <div className="mb-8">
              <ProgressBar
                completed={progress}
                customLabel=" "
                height="4px"
                bgColor="#f97316"
                baseBgColor="#1f2937"
                isLabelVisible={false}
              />
            </div>
          )}

          {error && (
            <div className="p-4 mb-8 bg-red-900/50 border border-red-500 rounded-lg text-red-200">
              {error}
            </div>
          )}

          {recipe && (
            <div className="p-6 bg-gray-800 rounded-lg prose prose-invert max-w-none">
              <ReactMarkdown>{recipe}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 