# 🎭 Cosplay AI Generator - Imagen 4 Ultra (HIGH QUALITY VERSION)
# 
# This version includes proper quality parameters and better prompts

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

# 🎭 IMPROVED Character definitions with better prompts
IMPROVED_CHARACTERS = {
    "mikasa": {
        "name": "Mikasa Ackerman",
        "series": "Attack on Titan",
        "prompt": "Professional cosplay photography of Mikasa Ackerman from Attack on Titan. The person in the image should be transformed to look exactly like Mikasa: short black bob haircut with straight bangs, dark gray eyes, wearing the iconic Survey Corps military uniform with brown cropped jacket over white long-sleeve shirt, white pants with brown knee-high boots, leather harness straps across chest and waist, red knitted scarf around neck, ODM gear with gas tanks and blade holders, brown leather straps and buckles, military insignia patches. The person should maintain their facial structure and bone structure but be transformed to match Mikasa's appearance. Professional studio lighting, ultra high quality, extremely detailed, sharp focus, perfect cosplay transformation, preserve original person's identity while transforming to character."
    },
    "sailor-moon": {
        "name": "Sailor Moon",
        "series": "Sailor Moon",
        "prompt": "Professional cosplay photography of Sailor Moon. The person in the image should be transformed to look exactly like Sailor Moon: blonde hair in twin tails with red ribbons, blue eyes, wearing detailed blue sailor costume with white collar and red bow, moon tiara, white gloves, red ribbons in hair. The person should maintain their facial structure and bone structure but be transformed to match Sailor Moon's appearance. Professional studio lighting, ultra high quality, extremely detailed, sharp focus, perfect cosplay transformation, preserve original person's identity while transforming to character."
    },
    "wonder-woman": {
        "name": "Wonder Woman",
        "series": "DC Comics",
        "prompt": "Professional cosplay photography of Wonder Woman. The person in the image should be transformed to look exactly like Wonder Woman: long dark hair, brown eyes, wearing red and gold armor with blue star-spangled briefs, golden tiara, lasso of truth, silver bracelets. The person should maintain their facial structure and bone structure but be transformed to match Wonder Woman's appearance. Professional studio lighting, ultra high quality, extremely detailed, sharp focus, perfect cosplay transformation, preserve original person's identity while transforming to character."
    }
}

print("Available characters:")
for char_id, char_data in IMPROVED_CHARACTERS.items():
    print(f"  • {char_id}: {char_data['name']} ({char_data['series']})")

# 🔑 Google Cloud Authentication (FIXED)
class HighQualityImagenGenerator:
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
    
    def generate_cosplay(self, image_path, character_id, output_name=None, quality="high"):
        """Generate high-quality cosplay transformation using Imagen 4 Ultra"""
        
        if not self.credentials:
            print("❌ No valid credentials - running in demo mode")
            return self._demo_mode(image_path, character_id, output_name)
        
        # Load and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Get character prompt
        if character_id not in IMPROVED_CHARACTERS:
            raise ValueError(f"Character '{character_id}' not found")
        
        prompt = IMPROVED_CHARACTERS[character_id]['prompt']
        character_name = IMPROVED_CHARACTERS[character_id]['name']
        
        print(f"🎭 Generating HIGH QUALITY {character_name} cosplay...")
        print(f"📸 Input: {image_path}")
        
        # HIGH QUALITY API payload with proper parameters
        payload = {
            "instances": [{
                "prompt": prompt,
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
                        "guidanceScale": 150,  # Higher guidance for better quality
                        "outputImageType": "EDITED_IMAGE",
                        "seed": None,  # Random seed for variety
                        "negativePrompt": "blurry, low quality, distorted, deformed, bad anatomy, bad proportions, extra limbs, missing limbs, mutated hands, poorly drawn face, poorly drawn hands, poorly drawn eyes, poorly drawn hair, poorly drawn body, poorly drawn clothes, poorly drawn background, poorly drawn details, low resolution, pixelated, grainy, noisy, artifacts, compression artifacts, jpeg artifacts, watermark, signature, text, logo, brand, commercial, advertisement, promotional, stock photo, generic, amateur, unprofessional, bad lighting, bad composition, bad framing, bad angle, bad perspective, bad proportions, bad anatomy, bad structure, bad form, bad shape, bad design, bad style, bad art, bad drawing, bad painting, bad photography, bad image, bad quality, bad result, bad output, bad generation, bad creation, bad production, bad work, bad job, bad performance, bad execution, bad implementation, bad realization, bad manifestation, bad materialization, bad actualization, bad concretization, bad embodiment, bad incarnation, bad personification, bad representation, bad depiction, bad portrayal, bad characterization, bad description, bad illustration, bad visualization, bad conceptualization, bad interpretation, bad translation, bad transformation, bad conversion, bad adaptation, bad modification, bad alteration, bad change, bad variation, bad deviation, bad divergence, bad difference, bad distinction, bad differentiation, bad discrimination, bad separation, bad division, bad partition, bad segmentation, bad classification, bad categorization, bad organization, bad arrangement, bad ordering, bad sequencing, bad structuring, bad formatting, bad layout, bad design, bad composition, bad construction, bad assembly, bad construction, bad building, bad creation, bad making, bad production, bad manufacturing, bad fabrication, bad construction, bad building, bad erection, bad establishment, bad foundation, bad base, bad ground, bad support, bad structure, bad framework, bad skeleton, bad backbone, bad spine, bad core, bad center, bad heart, bad essence, bad soul, bad spirit, bad energy, bad force, bad power, bad strength, bad might, bad vigor, bad vitality, bad life, bad existence, bad being, bad presence, bad reality, bad actuality, bad truth, bad fact, bad reality, bad actuality, bad truth, bad fact, bad reality, bad actuality, bad truth, bad fact"
                    }
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
            
            print("🚀 Sending HIGH QUALITY request to Imagen 4 Ultra...")
            print("⏳ This may take 30-60 seconds for high quality generation...")
            
            response = requests.post(self.endpoint, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if "predictions" in result and len(result["predictions"]) > 0:
                    # Decode and save image
                    image_data = base64.b64decode(result["predictions"][0]["bytesBase64Encoded"])
                    
                    # Generate output filename
                    if not output_name:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_name = f"{character_id}_hq_{timestamp}.png"
                    
                    output_path = OUTPUT_FOLDER / output_name
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    # Check image dimensions
                    with Image.open(output_path) as img:
                        width, height = img.size
                        print(f"✅ HIGH QUALITY cosplay generated successfully!")
                        print(f"📐 Image dimensions: {width}x{height}")
                        print(f"💾 Saved to: {output_path}")
                    
                    return str(output_path)
                else:
                    print("❌ No predictions returned from API")
                    print(f"Response: {result}")
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
        print(f"🎭 Would transform to: {IMPROVED_CHARACTERS[character_id]['name']}")
        
        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{character_id}_demo_{timestamp}.txt"
        
        output_path = OUTPUT_FOLDER / output_name
        
        with open(output_path, 'w') as f:
            f.write(f"Demo mode - would generate {IMPROVED_CHARACTERS[character_id]['name']} cosplay\n")
            f.write(f"Input image: {image_path}\n")
            f.write(f"Character: {character_id}\n")
            f.write(f"Prompt: {IMPROVED_CHARACTERS[character_id]['prompt']}\n")
        
        print(f"💾 Demo file saved to: {output_path}")
        return str(output_path)

# Test the high-quality generator
if __name__ == "__main__":
    generator = HighQualityImagenGenerator()
    
    # List available model images
    model_images = list(MODELS_FOLDER.glob("*.jpg")) + list(MODELS_FOLDER.glob("*.jpeg")) + list(MODELS_FOLDER.glob("*.png"))
    
    if model_images:
        print(f"\n📸 Found {len(model_images)} model images:")
        for img in model_images:
            print(f"  • {img.name}")
        
        # Generate HIGH QUALITY cosplay for first image and first character
        if model_images and IMPROVED_CHARACTERS:
            first_image = model_images[0]
            first_character = list(IMPROVED_CHARACTERS.keys())[0]
            
            print(f"\n🎭 Generating HIGH QUALITY {IMPROVED_CHARACTERS[first_character]['name']} cosplay...")
            result = generator.generate_cosplay(str(first_image), first_character, quality="high")
            
            if result:
                print(f"✅ Success! Check the output folder for your HIGH QUALITY cosplay image.")
            else:
                print("❌ Generation failed. Check the error messages above.")
    else:
        print("\n📸 No model images found in the models/ folder.")
        print("Please add some photos to the models/ folder and run again.")