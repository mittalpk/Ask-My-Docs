# AskMyDocs Frontend

React frontend for the AskMyDocs AI-powered document query system.

## Features

- **User Authentication**: Login and registration pages
- **Document Upload**: Upload PDF files or enter text manually
- **AI Chat Interface**: Ask questions about your documents
- **Responsive Design**: Clean, modern UI that works on all devices

## Quick Start with Docker

From the root project directory:

```bash
docker-compose up --build
```

Access the app at `http://localhost:3000`

## Manual Development Setup

1. Install dependencies:
```bash
npm install
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start the dev server:
```bash
npm start
```

App runs at `http://localhost:5173`

## Environment Variables

Create a `.env` file with:

```env
VITE_API_BASE=http://localhost:8000
```

Notes

This frontend expects the backend FastAPI server to expose the following endpoints:
- POST /auth/register
- POST /auth/login
- POST /upload/ (multipart form)
- POST /chat/add_document
- POST /chat/query
