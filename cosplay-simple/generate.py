#!/usr/bin/env python3
"""
🎭 Cosplay AI Generator - Imagen 4 Ultra
Simple all-in-one cosplay transformation

Usage:
    python generate.py <image_file> <character> [output_name]

Examples:
    python generate.py model1.jpg mikasa
    python generate.py model1.jpg sailor-moon custom_name
"""

import os
import json
import base64
import time
import sys
from datetime import datetime
from pathlib import Path
from PIL import Image
import requests
from dotenv import load_dotenv
from google.auth import default
from google.auth.transport.requests import Request

# Load environment variables
load_dotenv()

class CosplayGenerator:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("IMAGEN_LOCATION", "us-central1")

        # Folders
        self.models_folder = Path("models")
        self.output_folder = Path("output")
        self.characters_file = Path("characters.json")

        # Create folders
        self.models_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)

        # Load characters
        with open(self.characters_file, 'r') as f:
            self.characters = json.load(f)

        # Initialize Google Cloud
        self._init_auth()

    def _init_auth(self):
        """Initialize Google Cloud authentication"""
        if not self.project_id:
            print("❌ GOOGLE_CLOUD_PROJECT_ID not set in .env file")
            self.credentials = None
            return

        try:
            self.credentials, _ = default()
            self.credentials.refresh(Request())
            print("✅ Google Cloud authentication successful!")

            # Imagen 4 Ultra endpoint
            self.endpoint = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/imagen-4.0-ultra-generate-001:predict"

        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("💡 Running in demo mode")
            self.credentials = None

    def generate(self, image_file, character_id, output_name=None):
        """Generate cosplay transformation"""

        # Validate inputs
        image_path = self.models_folder / image_file
        if not image_path.exists():
            print(f"❌ Image not found: {image_path}")
            return None

        if character_id not in self.characters:
            print(f"❌ Character '{character_id}' not found")
            print(f"Available: {list(self.characters.keys())}")
            return None

        character = self.characters[character_id]
        print(f"🎭 Generating {character['name']} cosplay...")
        print(f"📸 Input: {image_file}")

        if not self.credentials:
            return self._demo_mode(image_path, character_id, character['name'], output_name)

        # Load and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()

        image_b64 = base64.b64encode(image_data).decode('utf-8')

        # Prepare API payload
        payload = {
            "instances": [{
                "prompt": character['prompt'],
                "image": {
                    "bytesBase64Encoded": image_b64
                },
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "1:1",
                    "safetyFilterLevel": "block_some",
                    "personGeneration": "allow_adult",
                    "outputOptions": {
                        "compressionQuality": "lossless",
                        "mimeType": "image/png"
                    },
                    "editConfig": {
                        "editMode": "inpainting-replace",
                        "guidanceScale": 120,
                        "outputImageType": "EDITED_IMAGE"
                    },
                    "stylizationLevel": 100
                }
            }]
        }

        # Make API request
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Content-Type": "application/json"
        }

        try:
            print("🚀 Calling Imagen 4 Ultra API...")
            start_time = time.time()

            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=180
            )

            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                if "predictions" in data and data["predictions"]:
                    prediction = data["predictions"][0]
                    result_b64 = prediction.get("bytesBase64Encoded")

                    if result_b64:
                        result_path = self._save_result(result_b64, character_id, character['name'], output_name)
                        print(f"⏱️  Generation time: {end_time - start_time:.2f} seconds")
                        print(f"🎉 Success! Result saved: {result_path}")
                        return result_path
                    else:
                        print("❌ No image data in response")
                        return None
                else:
                    print("❌ No predictions in response")
                    return None
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def _demo_mode(self, image_path, character_id, character_name, output_name):
        """Demo mode - creates a placeholder result"""
        print(f"🎭 Demo Mode: Creating placeholder for {character_name}")

        # Create a simple demonstration image
        demo_img = Image.new('RGB', (512, 512), color='lightblue')

        # Save demo result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not output_name:
            output_name = f"{character_id}_{timestamp}_demo"

        output_path = self.output_folder / f"{output_name}.png"
        demo_img.save(output_path)

        print(f"✅ Demo result saved: {output_path}")
        return output_path

    def _save_result(self, image_b64, character_id, character_name, output_name):
        """Save the generated image"""
        # Decode image
        image_data = base64.b64decode(image_b64)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not output_name:
            output_name = f"{character_id}_{timestamp}"

        output_path = self.output_folder / f"{output_name}.png"

        # Save image
        with open(output_path, 'wb') as f:
            f.write(image_data)

        print(f"✅ {character_name} cosplay saved: {output_path}")
        return output_path

    def list_models(self):
        """List available model images"""
        model_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            model_files.extend(list(self.models_folder.glob(ext)))

        print(f"📸 Found {len(model_files)} model images:")
        for i, file_path in enumerate(model_files):
            print(f"  {i+1}. {file_path.name}")

        return model_files

    def list_characters(self):
        """List available characters"""
        print("🎭 Available characters:")
        for char_id, char_data in self.characters.items():
            print(f"  • {char_id}: {char_data['name']} ({char_data['series']})")

        return list(self.characters.keys())

def main():
    """Command line interface"""
    if len(sys.argv) < 3:
        print("🎭 Cosplay AI Generator - Imagen 4 Ultra")
        print()
        print("Usage:")
        print("  python generate.py <image_file> <character> [output_name]")
        print()
        print("Examples:")
        print("  python generate.py model1.jpg mikasa")
        print("  python generate.py model1.jpg sailor-moon custom_name")
        print()

        generator = CosplayGenerator()
        generator.list_models()
        print()
        generator.list_characters()
        return

    # Parse arguments
    image_file = sys.argv[1]
    character = sys.argv[2]
    output_name = sys.argv[3] if len(sys.argv) > 3 else None

    # Generate cosplay
    generator = CosplayGenerator()
    result = generator.generate(image_file, character, output_name)

    if result:
        print(f"\\n🎉 Cosplay generation complete!")
        print(f"📁 Check output folder: {generator.output_folder.absolute()}")
    else:
        print("\\n❌ Generation failed")

if __name__ == "__main__":
    main()