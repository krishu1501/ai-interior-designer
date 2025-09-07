# Room Redesign Assistant

A full-stack application that helps users redesign their rooms by suggesting new furniture or decor items based on a theme. The app uses Google Gemini's image generation model to visualize the redesigned room and fetches product details from Amazon for easy purchase.

It leverages Google Gemini's image generation model to help users visualize and redesign their rooms. Users can upload a room's image and specify a theme (e.g., modern, vintage, relaxed). The app suggests new furniture or decor items, fetches their details from Amazon, and generates a new room image incorporating the changes. This innovative tool simplifies interior design and shopping, making it accessible and user-friendly.

## Prerequisites

- Python 3.7 or higher
- Node.js 16.x or higher (recommended 16.x LTS)
  - To check your Node.js version: `node --version`
  - Download Node.js from: https://nodejs.org/
- Set the environment variable `GEMINI_API_KEY` with your Google Gemini API key.
  - Instructions for obtaining the API key can be found at: https://ai.google.dev/gemini-api/docs/api-key

## Setup and Running

### Backend Setup

1. Navigate to the backend directory and create virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate the virtual environment:
   - On Windows:
```bash
venv\Scripts\activate
```
   - On Unix or MacOS:
```bash
source venv/bin/activate
```

3. Install required packages (make sure your virtual environment is activated, you should see (venv) in your terminal):
```bash
pip install -r requirements.txt
```
If you get any errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Set the `GEMINI_API_KEY` environment variable:
   - On Windows:
```bash
set GEMINI_API_KEY=your_api_key_here
```
   - On Unix or MacOS:
```bash
export GEMINI_API_KEY=your_api_key_here
```

5. Run the backend server:
```bash
python main.py
```
The backend will run on http://localhost:8000

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the frontend development server:
```bash
npm start
```
The frontend will run on http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser.
2. Upload an image of your room.
3. Optionally, enter a theme (e.g., relaxed, vintage, calm, modern, gadget freak).
4. Click Submit to see the redesigned room image alongside the original.
5. View the list of suggested items with their details and clickable Amazon links.

## Results

###
[Theme: Vintage](screenshots/vintage.jpg)

###
[Theme: Calm](screenshots/calm.jpg)
