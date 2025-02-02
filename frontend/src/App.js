import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { ArrowPathIcon } from '@heroicons/react/24/solid';
import ProgressBar from "@ramonak/react-progress-bar";
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [recipe, setRecipe] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);

  // Debug logging for state changes
  useEffect(() => {
    console.log('State updated:', { url, recipe, loading, error, progress });
  }, [url, recipe, loading, error, progress]);

  const simulateProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 90) {
          clearInterval(interval);
          return 90;
        }
        return prevProgress + 10;
      });
    }, 500);
    return interval;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted with URL:', url);
    
    setLoading(true);
    setError('');
    setRecipe('');
    
    // Start progress simulation
    const progressInterval = simulateProgress();

    try {
      console.log('Making API request to /api/recipe');
      const response = await axios.post('/api/recipe', {
        url: url
      });
      
      console.log('API response:', response.data);
      
      if (response.data && response.data.recipe) {
        setRecipe(response.data.recipe);
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (err) {
      console.error('Detailed error:', {
        message: err.message,
        response: err.response,
        status: err.response?.status,
        data: err.response?.data
      });
      
      let errorMessage = 'An error occurred while processing your request.';
      
      if (err.response?.status === 404) {
        errorMessage = 'The recipe endpoint is not available. Please try again later.';
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message) {
        errorMessage = err.message;
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
                customLabel={progress === 100 ? "Done!" : `${progress}%`}
                height="15px"
                labelSize="12px"
                baseBgColor="#1f2937"
                bgColor="#f97316"
                borderRadius="10px"
                labelAlignment="center"
                transitionDuration="0.3s"
                animateOnRender
                maxCompleted={100}
              />
            </div>
          )}

          {error && (
            <div className="mb-8 p-4 bg-red-900/50 border border-red-800 rounded-lg text-red-200">
              <p>{error}</p>
            </div>
          )}

          {recipe && (
            <div className="p-6 bg-gray-800 rounded-lg border border-gray-700">
              <ReactMarkdown 
                className="prose prose-invert max-w-none prose-headings:text-orange-500 prose-strong:text-orange-300 prose-p:text-gray-300 prose-li:text-gray-300"
              >
                {recipe}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 