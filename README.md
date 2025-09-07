# Amazon Product Scraper

A full-stack application that scrapes Amazon product search results using Python and displays them in a React frontend.

## Prerequisites

- Python 3.7 or higher
- Node.js 16.x or higher (recommended 16.x LTS)
  - To check your Node.js version: `node --version`
  - Download Node.js from: https://nodejs.org/

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

4. Run the backend server:
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

1. Open http://localhost:3000 in your browser
2. Enter a search term and maximum number of results
3. Click Search to see the results
4. Click on product cards to view them on Amazon

## Troubleshooting

### ModuleNotFoundError: No module named 'fastapi'
This error occurs when packages are not installed correctly. Try these steps:
1. Make sure you're in the backend directory
2. Ensure your virtual environment is activated (you should see (venv) in your terminal)
3. Run:
```bash
pip uninstall fastapi
pip install fastapi
pip install -r requirements.txt
```

If the error persists, try creating a new virtual environment:
```bash
deactivate  # if venv is active
rm -rf venv  # on Unix/MacOS
# OR
rmdir /s /q venv  # on Windows
python -m venv venv
# Then follow activation and installation steps above
```
