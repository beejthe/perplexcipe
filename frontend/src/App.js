import React, { useState } from 'react';
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
    setLoading(true);
    setError('');
    setRecipe('');
    
    // Start progress simulation
    const progressInterval = simulateProgress();

    try {
      const response = await axios.post('/api/recipe', {
        url: url
      });
      setRecipe(response.data.recipe);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while processing your request');
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
    <div className="min-h-screen bg-dark-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-primary-500 mb-2">Perplexcipe</h1>
          <p className="text-dark-300">Transform any recipe into its essential components</p>
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
                className="flex-1 px-4 py-2 rounded-lg bg-dark-700 border border-dark-600 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 text-white placeholder-dark-400"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg font-medium transition-colors disabled:opacity-50"
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
            <div className="progress-container">
              <ProgressBar 
                completed={progress}
                customLabel={progress === 100 ? "Done!" : `${progress}%`}
                height="15px"
                labelSize="12px"
                baseBgColor="#e0e0e0"
                bgColor="#4CAF50"
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
              {error}
            </div>
          )}

          {recipe && (
            <div className="p-6 bg-dark-700 rounded-lg border border-dark-600">
              <ReactMarkdown 
                className="prose prose-invert max-w-none prose-headings:text-primary-500 prose-strong:text-primary-300"
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