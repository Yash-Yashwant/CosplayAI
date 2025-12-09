# Cosplay AI V1

An AI-powered tool for creators and cosplay enthusiasts to generate professional cosplay images from their photos using Google Imagen Pro API.

## Features

- **Photo Upload & Analysis**: Smart image analysis for optimal results
- **Character Library**: 10+ popular characters across different styles (anime, superhero, gaming, comic, fantasy)
- **Smart Prompt Engineering**: AI-optimized prompts for better generation quality
- **Real-time Generation**: Live progress tracking and status updates
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

## Architecture

### Backend (FastAPI + Python)
- **FastAPI**: Modern, fast web framework for building APIs
- **Google Imagen Pro**: AI image generation engine
- **Image Processing**: OpenCV and Pillow for photo analysis
- **Smart Prompting**: Intelligent prompt engineering system

### Frontend (React + TypeScript)
- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first approach

## 📁 Project Structure

```
cosplay-ai-v1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── imagen_client.py     # Google Imagen integration
│   ├── prompt_builder.py    # Smart prompt generation
│   ├── photo_analyzer.py    # Image analysis utilities
│   ├── character_library.py # Character/style definitions
│   └── utils.py             # Helper functions
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   └── utils/          # Utility functions
│   └── public/             # Static assets
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Cloud Project with Imagen Pro API access

### Backend Setup

1. **Clone and navigate to the project:**
   ```bash
   cd cosplay-ai-v1/backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp ../.env.example .env
   # Edit .env with your Google Cloud credentials
   ```

4. **Run the backend server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd cosplay-ai-v1/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
IMAGEN_LOCATION=us-central1

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
FRONTEND_URL=http://localhost:3000
```

### Google Cloud Setup

1. Create a Google Cloud Project
2. Enable the Vertex AI API
3. Set up authentication credentials
4. Configure Imagen Pro access

## 📚 API Documentation

### Endpoints

- `GET /` - API health check
- `GET /health` - Detailed health status
- `POST /generate-cosplay` - Generate cosplay image
- `GET /generation/{id}` - Get generation status
- `GET /characters` - List available characters

### Example Usage

```bash
# Generate cosplay image
curl -X POST "http://localhost:8000/generate-cosplay" \
  -F "photo=@/path/to/photo.jpg" \
  -F "character=sailor-moon" \
  -F "style=anime" \
  -F "quality=high"

# Check generation status
curl "http://localhost:8000/generation/{generation_id}"
```

## Character Library

### Available Characters

| Character | Style | Description |
|-----------|-------|-------------|
| Sailor Moon | Anime | Classic magical girl with sailor uniform |
| Wonder Woman | Superhero | Amazonian warrior princess |
| D.Va | Gaming | Professional gamer and mech pilot |
| Harley Quinn | Comic | Chaotic villain with jester costume |
| Princess Zelda | Fantasy | Royal princess with magical powers |
| Power Girl | Superhero | Powerful superhero with classic costume |
| 2B | Gaming | Android combat unit with elegant design |
| Mikasa Ackerman | Anime | Skilled soldier with military uniform |
| Catwoman | Comic | Feline-themed thief with sleek costume |
| Ahri | Gaming | Nine-tailed fox spirit with magical attire |

## 🔄 Development Workflow

### Phase 1: Foundation ✅
- [x] Project structure setup
- [x] FastAPI backend with core modules
- [x] React frontend with TypeScript
- [x] Tailwind CSS styling
- [x] Basic API endpoints

### Phase 2: Core Logic (In Progress)
- [ ] Google Imagen Pro API integration
- [ ] Photo analysis implementation
- [ ] Prompt building system
- [ ] Character library integration

### Phase 3: User Experience
- [ ] Frontend-backend integration
- [ ] Real-time progress tracking
- [ ] Error handling and validation
- [ ] Result display and download

### Phase 4: Polish & Testing
- [ ] Beta user testing
- [ ] Performance optimization
- [ ] Quality control measures
- [ ] Launch preparation

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Backend (AWS/Vercel)
```bash
# Build for production
pip install -r requirements.txt

# Deploy to your preferred platform
```

### Frontend (Vercel/Netlify)
```bash
# Build for production
npm run build

# Deploy to your preferred platform
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## Roadmap

### V1 (Current)
- Google Imagen Pro integration
- Basic character library
- Smart prompt engineering
- Web interface

### V2 (Future)
- SDXL + IP-Adapter integration
- Face preservation technology
- Advanced character customization
- Batch processing
- API rate limiting and monetization

---

Built with ❤️ for the cosplay community
