from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import Optional
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our custom modules
from imagen_client import ImagenClient
from prompt_builder import PromptBuilder
from photo_analyzer import PhotoAnalyzer
from character_library import CharacterLibrary
from utils import generate_unique_id, estimate_generation_time, validate_file_extension

app = FastAPI(
    title="Cosplay AI V1",
    description="AI-powered cosplay image generation for content creators",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our modules
try:
    imagen_client = ImagenClient()
except ValueError as e:
    print(f"Warning: {e}. Running in development mode without Google Cloud.")
    imagen_client = None

prompt_builder = PromptBuilder()
photo_analyzer = PhotoAnalyzer()
character_library = CharacterLibrary()

# In-memory storage for demo (replace with database in production)
generations = {}

@app.get("/")
async def root():
    return {"message": "Cosplay AI V1 API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate-cosplay")
async def generate_cosplay(
    photo: UploadFile = File(...),
    character: str = "sailor-moon",
    style: str = "anime",
    quality: str = "high"
):
    """
    Generate cosplay image from uploaded photo
    """
    try:
        # Validate file type
        if not photo.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if not validate_file_extension(photo.filename):
            raise HTTPException(status_code=400, detail="Invalid file format")
        
        # Read image data
        image_data = await photo.read()
        
        # Temporarily skip validation for testing
        # is_valid, error_msg = photo_analyzer.validate_image(image_data)
        # if not is_valid:
        #     raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate unique ID for this generation
        generation_id = generate_unique_id()
        
        # Analyze photo (simplified for testing)
        analysis = {
            "hair_color": "unknown",
            "skin_tone": "medium",
            "pose": "standard",
            "style_cues": ["test"],
            "dimensions": (600, 600),
            "has_face": True,
            "quality_score": 0.8
        }
        
        # Get character details
        character_data = character_library.get_character(character)
        if not character_data:
            raise HTTPException(status_code=400, detail="Invalid character")
        
        # Build comprehensive cosplay transformation prompt
        transformation_prompt = prompt_builder.build_cosplay_transformation_prompt(analysis, character_data, style)
        enhanced_prompt = prompt_builder.enhance_prompt_for_quality(transformation_prompt, quality)
        final_prompt = prompt_builder.sanitize_prompt(enhanced_prompt)
        
        # Estimate generation time
        estimated_time = estimate_generation_time(character, quality, analysis.get('dimensions', (512, 512)))
        
        # Store generation info
        generations[generation_id] = {
            "id": generation_id,
            "status": "processing",
            "character": character,
            "style": style,
            "quality": quality,
            "created_at": datetime.now().isoformat(),
            "estimated_time": estimated_time,
            "prompt": final_prompt,
            "analysis": analysis
        }
        
        # For demo: Using enhanced Imagen 4 Ultra prompts with realistic placeholder results
        # In production: Will use actual Imagen 4 Ultra API with the comprehensive transformation prompts
        generations[generation_id]["status"] = "completed"
        # Create a more realistic demo image URL based on character
        if character == "sailor-moon":
            generations[generation_id]["result_url"] = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImJnIiB4MT0iMCUiIHkxPSIwJSIgeDI9IjEwMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZmY2YmU3O3N0b3Atb3BhY2l0eToxIiAvPjxzdG9wIG9mZnNldD0iMTAwJSIgc3R5bGU9InN0b3AtY29sb3I6IzRmNDZlNTtzdG9wLW9wYWNpdHk6MSIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2JnKSIvPjxjaXJjbGUgY3g9IjI1NiIgY3k9IjE4MCIgcj0iNjAiIGZpbGw9IiNmZmRiOTkiLz48Y2lyY2xlIGN4PSIyMzUiIGN5PSIxNzAiIHI9IjMiIGZpbGw9IiMzMzMiLz48Y2lyY2xlIGN4PSIyNzciIGN5PSIxNzAiIHI9IjMiIGZpbGw9IiMzMzMiLz48ZWxsaXBzZSBjeD0iMjU2IiBjeT0iMTg1IiByeD0iNCIgcnk9IjIiIGZpbGw9IiNlZTg4NzQiLz48cGF0aCBkPSJNMjIwIDEyMCBRMjU2IDEwMCAyOTIgMTIwIEwyOTAgMTQwIFEyNTYgMTIwIDIyMiAxNDAiIGZpbGw9IiNmZmQ3MDAiLz48Y2lyY2xlIGN4PSIyNTYiIGN5PSIxMDAiIHI9IjgiIGZpbGw9IiNmZmQ3MDAiLz48dGV4dCB4PSI1MCUiIHk9IjkwJSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4IiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5GRICBTY2lsb3IgTW9vbiBDb3NwbGF5IERlbW8g8J+RkTwvdGV4dD48L3N2Zz4="
        elif character == "wonder-woman":
            generations[generation_id]["result_url"] = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImJnMiIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+PHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6I2RjMjYyNjtzdG9wLW9wYWNpdHk6MSIgLz48c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmYWNjMTU7c3RvcC1vcGFjaXR5OjEiIC8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNiZzIpIi8+PGNpcmNsZSBjeD0iMjU2IiBjeT0iMTgwIiByPSI2MCIgZmlsbD0iI2ZmZGI5OSIvPjxjaXJjbGUgY3g9IjIzNSIgY3k9IjE3MCIgcj0iMyIgZmlsbD0iIzMzMyIvPjxjaXJjbGUgY3g9IjI3NyIgY3k9IjE3MCIgcj0iMyIgZmlsbD0iIzMzMyIvPjxlbGxpcHNlIGN4PSIyNTYiIGN5PSIxODUiIHJ4PSI0IiByeT0iMiIgZmlsbD0iI2VlODg3NCIvPjxwYXRoIGQ9Ik0yMjAgMTIwIFEyNTYgMTAwIDI5MiAxMjAgTDI5MCAxNDAgUTI1NiAxMjAgMjIyIDE0MCIgZmlsbD0iIzU0MzMxMyIvPjxjaXJjbGUgY3g9IjI1NiIgY3k9IjEwMCIgcj0iOCIgZmlsbD0iI2ZhY2MxNSIvPjx0ZXh0IHg9IjUwJSIgeT0iOTAlIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiNmZmZmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPvCflrIgV29uZGVyIFdvbWFuIENvc3BsYXkgRGVtbyDwn5ayPC90ZXh0Pjwvc3ZnPg=="
        elif character == "mikasa":
            generations[generation_id]["result_url"] = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9Im1pa2FzYUJnIiB4MT0iMCUiIHkxPSIwJSIgeDI9IjEwMCUiIHkyPSIxMDAlIj48c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNzQ0NzM1O3N0b3Atb3BhY2l0eToxIiAvPjxzdG9wIG9mZnNldD0iMTAwJSIgc3R5bGU9InN0b3AtY29sb3I6IzNhMzYzMTtzdG9wLW9wYWNpdHk6MSIgLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI21pa2FzYUJnKSIvPjxyZWN0IHg9IjAiIHk9IjQ1MCIgd2lkdGg9IjUxMiIgaGVpZ2h0PSI2MiIgZmlsbD0iIzU1NGYzOSIvPjxjaXJjbGUgY3g9IjI1NiIgY3k9IjE4MCIgcj0iNjAiIGZpbGw9IiNmZmRiOTkiLz48Y2lyY2xlIGN4PSIyMzUiIGN5PSIxNzAiIHI9IjMiIGZpbGw9IiMzMzMiLz48Y2lyY2xlIGN4PSIyNzciIGN5PSIxNzAiIHI9IjMiIGZpbGw9IiMzMzMiLz48ZWxsaXBzZSBjeD0iMjU2IiBjeT0iMTg1IiByeD0iNCIgcnk9IjIiIGZpbGw9IiNlZTg4NzQiLz48cGF0aCBkPSJNMjIwIDEyMCBRMjU2IDEwMCAyOTIgMTIwIEwyOTAgMTQwIFEyNTYgMTIwIDIyMiAxNDAiIGZpbGw9IiMzMzMiLz48cmVjdCB4PSIyMDAiIHk9IjI1MCIgd2lkdGg9IjExMiIgaGVpZ2h0PSI4MCIgZmlsbD0iIzc0NDczNSIvPjxyZWN0IHg9IjIxMCIgeT0iMjYwIiB3aWR0aD0iOTIiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmZmZmYiLz48cGF0aCBkPSJNMjMwIDI0MCBMMTI2MCAyNDAgTDI2MCAyNzAgTDIzMCAyNzAiIGZpbGw9IiNkYzI2MjYiLz48dGV4dCB4PSI1MCUiIHk9IjkwJSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4IiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7ijJUgTWlrYXNhIEFja2VybWFuIENvc3BsYXkgKEltYWdlbiA0KSA8L3RleHQ+PC9zdmc+"
        else:
            generations[generation_id]["result_url"] = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImJnMyIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+PHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6Izg4NTVmNztzdG9wLW9wYWNpdHk6MSIgLz48c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM1YjIxYjY7c3RvcC1vcGFjaXR5OjEiIC8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNiZzMpIi8+PGNpcmNsZSBjeD0iMjU2IiBjeT0iMTgwIiByPSI2MCIgZmlsbD0iI2ZmZGI5OSIvPjxjaXJjbGUgY3g9IjIzNSIgY3k9IjE3MCIgcj0iMyIgZmlsbD0iIzMzMyIvPjxjaXJjbGUgY3g9IjI3NyIgY3k9IjE3MCIgcj0iMyIgZmlsbD0iIzMzMyIvPjxlbGxpcHNlIGN4PSIyNTYiIGN5PSIxODUiIHJ4PSI0IiByeT0iMiIgZmlsbD0iI2VlODg3NCIvPjxwYXRoIGQ9Ik0yMjAgMTIwIFEyNTYgMTAwIDI5MiAxMjAgTDI5MCAxNDAgUTI1NiAxMjAgMjIyIDE0MCIgZmlsbD0iIzU0MzMxMyIvPjx0ZXh0IHg9IjUwJSIgeT0iOTAlIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiNmZmZmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPvCfmIwgQ29zcGxheSBSZXN1bHQgKEltYWdlbiA0IFVsdHJhKSDwn5iMPC90ZXh0Pjwvc3ZnPg=="
        generations[generation_id]["metadata"] = {"mode": "demo", "character": character}
        
        return {
            "generation_id": generation_id,
            "status": "processing",
            "estimated_time": estimated_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generation/{generation_id}")
async def get_generation(generation_id: str):
    """
    Get generation status and result
    """
    if generation_id not in generations:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    return generations[generation_id]

@app.get("/characters")
async def get_characters():
    """
    Get available characters
    """
    characters = character_library.get_all_characters()
    return {"characters": characters}

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)