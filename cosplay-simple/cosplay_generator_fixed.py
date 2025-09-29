# 🎭 Cosplay AI Generator - Imagen 4 Ultra (Fixed Authentication)
# 
# This is a fixed version of the notebook with proper OAuth scope configuration

import os
import json
import base64
import time
from datetime import datetime
from pathlib import Path
from PIL import Image
import requests
from dotenv import load_dotenv
from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("IMAGEN_LOCATION", "us-central1")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Folders
MODELS_FOLDER = Path("models")
OUTPUT_FOLDER = Path("output")
CHARACTERS_FILE = Path("characters.json")

# Create folders if they don't exist
MODELS_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

print(f"📁 Models folder: {MODELS_FOLDER.absolute()}")
print(f"📁 Output folder: {OUTPUT_FOLDER.absolute()}")
print(f"🚀 Project ID: {PROJECT_ID}")
print(f"🌍 Location: {LOCATION}")

# Load character definitions
with open(CHARACTERS_FILE, 'r') as f:
    CHARACTERS = json.load(f)

print("Available characters:")
for char_id, char_data in CHARACTERS.items():
    print(f"  • {char_id}: {char_data['name']} ({char_data['series']})")

# 🔑 Google Cloud Authentication (FIXED)
class ImagenGenerator:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.location = LOCATION
        
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID not set in .env file")
        
        # Initialize credentials with proper scopes
        try:
            if CREDENTIALS_PATH and os.path.exists(CREDENTIALS_PATH):
                # Use service account credentials with correct scopes
                self.credentials = service_account.Credentials.from_service_account_file(
                    CREDENTIALS_PATH,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                print("✅ Google Cloud authentication successful!")
            else:
                # Fallback to default credentials (for local development)
                self.credentials, _ = default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
                print("✅ Google Cloud authentication successful!")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("💡 Make sure your .env file is configured correctly")
            print("💡 Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account JSON file")
            self.credentials = None
        
        # Imagen 4 Ultra endpoint
        self.endpoint = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/imagen-4.0-ultra-generate-001:predict"
    
    def generate_from_scratch(self, character_id, output_name=None):
        """Generate cosplay from scratch (text-to-image)"""

        if not self.credentials:
            print("❌ No valid credentials - running in demo mode")
            return self._demo_mode(None, character_id, output_name)

        # Get character prompt
        if character_id not in CHARACTERS:
            raise ValueError(f"Character '{character_id}' not found")

        # Create a new prompt optimized for text-to-image generation
        base_prompt = CHARACTERS[character_id]['prompt']
        scratch_prompt = f"Professional cosplay photography. Beautiful female cosplay model as {CHARACTERS[character_id]['name']}. {base_prompt.replace('PRESERVE ORIGINAL FACE:', '').replace('Keep the exact same facial features, bone structure, eye color, skin tone, and facial expression from the input image. Only transform the outfit and hair.', 'Attractive female model with detailed facial features.')}"

        character_name = CHARACTERS[character_id]['name']

        print(f"🎭 Generating {character_name} cosplay from scratch...")

        # Prepare API payload for text-to-image
        payload = {
            "instances": [{
                "prompt": scratch_prompt,
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "9:16",
                    "safetyFilterLevel": "block_some",
                    "personGeneration": "allow_adult",
                    "outputOptions": {
                        "compressionQuality": "lossless",
                        "mimeType": "image/png"
                    },
                    "stylizationLevel": 100
                }
            }]
        }

        # Make API request
        try:
            # Get access token
            self.credentials.refresh(Request())
            access_token = self.credentials.token

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            print("🚀 Sending text-to-image request to Imagen 4 Ultra...")
            response = requests.post(self.endpoint, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()

                if "predictions" in result and len(result["predictions"]) > 0:
                    # Decode and save image
                    image_data = base64.b64decode(result["predictions"][0]["bytesBase64Encoded"])

                    # Generate output filename
                    if not output_name:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_name = f"{character_id}_scratch_{timestamp}.png"

                    output_path = OUTPUT_FOLDER / output_name

                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    print(f"✅ Cosplay generated successfully!")
                    print(f"💾 Saved to: {output_path}")
                    return str(output_path)
                else:
                    print("❌ No predictions returned from API")
                    return None
            else:
                print(f"❌ API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error during generation: {e}")
            return None

    def generate_cosplay(self, image_path, character_id, output_name=None):
        """Generate cosplay transformation using Imagen 4 Ultra"""
        
        if not self.credentials:
            print("❌ No valid credentials - running in demo mode")
            return self._demo_mode(image_path, character_id, output_name)
        
        # Load and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Get character prompt
        if character_id not in CHARACTERS:
            raise ValueError(f"Character '{character_id}' not found")
        
        prompt = CHARACTERS[character_id]['prompt']
        character_name = CHARACTERS[character_id]['name']
        
        print(f"🎭 Generating {character_name} cosplay...")
        print(f"📸 Input: {image_path}")
        
        # Prepare API payload
        payload = {
            "instances": [{
                "prompt": prompt,
                "image": {
                    "bytesBase64Encoded": image_b64
                },
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "9:16",
                    "safetyFilterLevel": "block_some",
                    "personGeneration": "allow_adult",
                    "outputOptions": {
                        "compressionQuality": "lossless",
                        "mimeType": "image/png"
                    },
                    "editConfig": {
                        "editMode": "inpainting-replace",
                        "guidanceScale": 150,
                        "outputImageType": "EDITED_IMAGE"
                    },
                    "stylizationLevel": 50
                }
            }]
        }
        
        # Make API request
        try:
            # Get access token
            self.credentials.refresh(Request())
            access_token = self.credentials.token
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            print("🚀 Sending request to Imagen 4 Ultra...")
            response = requests.post(self.endpoint, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if "predictions" in result and len(result["predictions"]) > 0:
                    # Decode and save image
                    image_data = base64.b64decode(result["predictions"][0]["bytesBase64Encoded"])
                    
                    # Generate output filename
                    if not output_name:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_name = f"{character_id}_{timestamp}.png"
                    
                    output_path = OUTPUT_FOLDER / output_name
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✅ Cosplay generated successfully!")
                    print(f"💾 Saved to: {output_path}")
                    return str(output_path)
                else:
                    print("❌ No predictions returned from API")
                    return None
            else:
                print(f"❌ API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error during generation: {e}")
            return None
    
    def _demo_mode(self, image_path, character_id, output_name=None):
        """Demo mode when credentials are not available"""
        print("🎭 DEMO MODE - No actual generation will occur")
        print(f"📸 Would process: {image_path}")
        print(f"🎭 Would transform to: {CHARACTERS[character_id]['name']}")
        
        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{character_id}_demo_{timestamp}.txt"
        
        output_path = OUTPUT_FOLDER / output_name
        
        with open(output_path, 'w') as f:
            f.write(f"Demo mode - would generate {CHARACTERS[character_id]['name']} cosplay\n")
            f.write(f"Input image: {image_path}\n")
            f.write(f"Character: {character_id}\n")
            f.write(f"Prompt: {CHARACTERS[character_id]['prompt']}\n")
        
        print(f"💾 Demo file saved to: {output_path}")
        return str(output_path)

# Test the generator
if __name__ == "__main__":
    generator = ImagenGenerator()

    print("\n🧪 TESTING: Generate Mikasa from scratch (no input image)")
    print("This will test if Imagen 4 Ultra can create good cosplay when not constrained by face preservation")
    print("-" * 80)

    # Test from-scratch generation with detailed prompt
    result = generator.generate_from_scratch("mikasa-detailed", "mikasa_detailed_prompt_test")

    if result:
        print(f"✅ From-scratch generation complete! Check: {result}")
    else:
        print("❌ From-scratch generation failed.")

    print("\n" + "="*80)
    print("📊 COMPARISON TEST COMPLETE")
    print("Compare this result with the previous face-preservation attempts to see the difference.")