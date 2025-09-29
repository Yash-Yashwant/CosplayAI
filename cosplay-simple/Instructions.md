# Cosplay AI V1 - Development Instructions

## Project Overview
Building an AI tool for OnlyFans creators to generate cosplay images from their photos. V1 uses Google Imagen Pro API with smart prompt engineering. V2 will add face preservation with SDXL + IP-Adapter.

### Core Value Proposition
Upload photo + select character → AI generates professional cosplay image in that style

### Target Users
OnlyFans creators, cosplay enthusiasts, content creators

## Technical Architecture V1

### Stack Decision
- **Backend**: FastAPI + Python
- **AI Engine**: Google Imagen Pro API (V1), SDXL + IP-Adapter (V2)
- **Frontend**: React + TypeScript + Tailwind
- **Image Processing**: Pillow, OpenCV
- **Deployment**: AWS/Vercel

### Why Imagen Pro for V1
- Fast to market (2-4 weeks vs 8+ weeks)
- Market validation before complex tech investment
- Learn user preferences and pain points
- Generate revenue to fund V2 development

## Project Structure
```
cosplay-ai-v1/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── imagen_client.py     # Google Imagen integration
│   ├── prompt_builder.py    # Smart prompt generation
│   ├── photo_analyzer.py    # Image analysis utilities
│   ├── character_library.py # Character/style definitions
│   └── utils.py             # Helper functions
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   └── package.json
├── .env                     # Environment variables
├── requirements.txt
└── README.md
```

## Core Features V1

### 1. Photo Upload & Analysis
- Accept JPEG/PNG uploads
- Basic image analysis (hair color, skin tone, pose)
- Quality validation (size, clarity)

### 2. Smart Prompt Engineering
- Analyze uploaded photo for visual cues
- Combine with character selection
- Generate enhanced Imagen Pro prompts
- Style consistency across generations

### 3. Character Library
**Popular Characters (Launch with 10+):**
- Sailor Moon (anime style)
- Wonder Woman (superhero)
- D.Va (gaming)
- Harley Quinn (comic)
- Zelda (fantasy)
- Power Girl (superhero)
- 2B (gaming)
- Mikasa (anime)
- Catwoman (comic)
- Ahri (gaming)

### 4. Generation Pipeline
```
Photo Upload → Analysis → Prompt Building → Imagen API → Post-processing → Delivery
```

## Development Phases

### Phase 1: Foundation (Week 1)
- [ ] Set up development environment
- [ ] Google Cloud project + Imagen Pro API setup
- [ ] Basic FastAPI structure
- [ ] React app initialization
- [ ] Test API connectivity

### Phase 2: Core Logic (Week 2)
- [ ] Photo upload endpoint
- [ ] Image analysis utilities
- [ ] Prompt building system
- [ ] Imagen Pro integration
- [ ] Basic character library

### Phase 3: User Experience (Week 3)
- [ ] Frontend upload interface
- [ ] Character selection UI
- [ ] Generation progress tracking
- [ ] Result display and download
- [ ] Error handling

### Phase 4: Polish & Testing (Week 4)
- [ ] Beta user testing
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Quality control measures
- [ ] Launch preparation

## Technical Implementation Details

### Google Imagen Pro Setup
```bash
# Environment variables needed
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
IMAGEN_LOCATION=us-central1
```

### Smart Prompt Engineering Strategy
```python
def build_prompt(photo_analysis, character, style):
    # Extract: "Asian woman, long black hair, casual pose"
    # Character: "Sailor Moon"
    # Result: "Professional cosplay photograph of Asian woman with long black hair as Sailor Moon, anime style, detailed blue sailor costume, moon tiara, magical girl pose, studio lighting, high quality"
```

### Character Prompt Templates
```python
CHARACTERS = {
    "sailor-moon": {
        "style": "anime style",
        "costume": "detailed blue sailor costume, moon tiara, white gloves",
        "pose": "magical girl pose",
        "hair": "blonde twin tails with red ribbons"
    },
    "wonder-woman": {
        "style": "superhero realistic",
        "costume": "red and gold armor, lasso of truth, tiara",
        "pose": "heroic power pose",
        "hair": "long dark hair"
    }
}
```

### Image Analysis Components
- Hair color detection (blonde, brunette, black, red)
- Skin tone approximation (light, medium, dark)
- Pose estimation (standing, sitting, action)
- Style cues (casual, formal, athletic)

## API Endpoints Design

### POST /generate-cosplay
```python
{
    "photo": "multipart/form-data",
    "character": "sailor-moon",
    "style": "anime",
    "quality": "high"
}

Response: {
    "generation_id": "uuid",
    "status": "processing",
    "estimated_time": 30
}
```

### GET /generation/{id}
```python
Response: {
    "id": "uuid",
    "status": "completed",
    "result_url": "https://...",
    "metadata": {...}
}
```