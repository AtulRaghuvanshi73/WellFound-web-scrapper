# Wellfound Job Scraper

A full-stack web application that scrapes job listings from Wellfound (formerly AngelList Talent) based on keywords. The application consists of a Python backend API and a React frontend interface.

## Features

- Real-time job scraping from Wellfound
- Keyword-based job search
- Display of company names, job titles, and other relevant information
- Threaded scraping service for improved performance
- Modern React frontend with dynamic data fetching

## Project Structure

```
wellfound-job-scraper/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── scraper.py        # Job scraping logic
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx       # Main React component
    │   └── ...          # Other React components
    ├── package.json
    └── ...
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

## Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend application will be available at `http://localhost:5173`

## Usage

1. Open your web browser and navigate to `http://localhost:5173`
2. Enter keywords in the search field to find relevant job listings
3. Click the "Scrape Jobs" button to fetch new job listings
4. View the results displayed in a clean, organized format

## API Endpoints

- `GET /api/jobs`: Retrieve all scraped jobs
- `POST /api/scrape`: Trigger new job scraping with specified keywords

## Development

To modify the scraping logic, edit `backend/scraper.py`
To modify the frontend appearance and behavior, edit files in the `frontend/src` directory

## Troubleshooting

### Common Issues

1. **Backend server won't start:**
   - Ensure Python and all dependencies are properly installed
   - Check if port 8000 is available

2. **Frontend development server issues:**
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

3. **CORS issues:**
   - Ensure backend CORS settings are properly configured
   - Verify frontend API calls use correct backend URL


## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes