# Perplexcipe

A modern web application that distills recipes into their essential components using AI. Simply paste a recipe URL, and get a clean, organized version of the recipe with just the important parts.

## Features

- Dark mode interface with a cooking-themed design
- URL input for recipe processing
- AI-powered recipe distillation using Perplexity's Sonar model
- Clean, organized output format
- Mobile-responsive design

## Tech Stack

- Frontend: React.js with styled-components
- Backend: FastAPI
- AI: Perplexity API (Sonar model)
- Styling: TailwindCSS

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```
   PERPLEXCIPE_PERPLEXITY_API_KEY=your_api_key_here
   ```

4. Run the development servers:
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload

   # Frontend
   cd frontend
   npm start
   ```

## License

MIT 