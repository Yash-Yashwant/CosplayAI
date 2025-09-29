"""
Google Imagen Pro API client for cosplay image generation
"""
import os
import base64
from typing import Optional, Dict, Any
import requests
import json
from google.auth import default
from google.auth.transport.requests import Request

class ImagenClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.project_number = os.getenv("GOOGLE_CLOUD_PROJECT_NUMBER")
        self.location = os.getenv("IMAGEN_LOCATION", "us-central1")

        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable is required")

        # Initialize Google Cloud credentials
        try:
            self.credentials, _ = default()
            self.credentials.refresh(Request())
        except Exception as e:
            print(f"Warning: Could not authenticate with Google Cloud: {e}")
            self.credentials = None

        # Imagen 4 Ultra API endpoint
        self.base_url = f"https://{self.location}-aiplatform.googleapis.com/v1"
        self.endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/imagen-4.0-ultra-generate-001:predict"
    
    def generate_image(self, prompt: str, image_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Generate image using Imagen 4 Ultra API

        Args:
            prompt: Text prompt for image generation
            image_data: Optional reference image data for transformation

        Returns:
            Dictionary containing generation result
        """
        try:
            # Prepare the request payload
            payload = {
                "instances": [{
                    "prompt": prompt,
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
                            "editMode": "inpainting-insert",
                            "guidanceScale": 100,
                            "outputImageType": "BASE_IMAGE_MASK"
                        }
                    }
                }]
            }
            
            # Add reference image if provided
            if image_data:
                payload["instances"][0]["image"] = {
                    "bytesBase64Encoded": base64.b64encode(image_data).decode('utf-8')
                }
            
            # Check if we have valid credentials
            if not self.credentials:
                return {
                    "success": False,
                    "error": "No valid Google Cloud credentials available"
                }

            # Make the API request
            headers = {
                "Authorization": f"Bearer {self.credentials.token}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            # Process response
            if response.status_code == 200:
                data = response.json()
                if "predictions" in data and data["predictions"]:
                    prediction = data["predictions"][0]
                    return {
                        "success": True,
                        "image_data": prediction.get("bytesBase64Encoded"),
                        "metadata": prediction.get("metadata", {})
                    }
                else:
                    return {
                        "success": False,
                        "error": "No predictions returned from Imagen API"
                    }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Imagen API error: {str(e)}"
            }
    
    def validate_api_connection(self) -> bool:
        """
        Test API connection with a simple request
        """
        try:
            if not self.credentials:
                return False

            # Simple test request to check API connectivity
            headers = {
                "Authorization": f"Bearer {self.credentials.token}",
                "Content-Type": "application/json"
            }

            test_payload = {
                "instances": [{
                    "prompt": "A simple test image",
                    "parameters": {
                        "sampleCount": 1,
                        "aspectRatio": "1:1"
                    }
                }]
            }

            response = requests.post(
                self.endpoint,
                headers=headers,
                json=test_payload,
                timeout=30
            )

            return response.status_code == 200
        except Exception:
            return False

    def generate_cosplay_transformation(self, prompt: str, base_image: bytes, mask_image: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Generate cosplay transformation using Imagen 4 Ultra with image editing capabilities

        Args:
            prompt: Detailed cosplay transformation prompt
            base_image: Original human photo for transformation
            mask_image: Optional mask to specify areas to transform

        Returns:
            Dictionary containing transformation result
        """
        try:
            # Enhanced payload for cosplay transformation
            payload = {
                "instances": [{
                    "prompt": prompt,
                    "image": {
                        "bytesBase64Encoded": base64.b64encode(base_image).decode('utf-8')
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
                        "stylizationLevel": 100,
                        "seed": None
                    }
                }]
            }

            # Add mask if provided for selective editing
            if mask_image:
                payload["instances"][0]["mask"] = {
                    "bytesBase64Encoded": base64.b64encode(mask_image).decode('utf-8')
                }

            # Check credentials
            if not self.credentials:
                return {
                    "success": False,
                    "error": "No valid Google Cloud credentials available"
                }

            # Make the API request
            headers = {
                "Authorization": f"Bearer {self.credentials.token}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=180  # Longer timeout for transformation
            )

            # Process response
            if response.status_code == 200:
                data = response.json()
                if "predictions" in data and data["predictions"]:
                    prediction = data["predictions"][0]
                    return {
                        "success": True,
                        "image_data": prediction.get("bytesBase64Encoded"),
                        "metadata": prediction.get("metadata", {}),
                        "transformation_type": "cosplay"
                    }
                else:
                    return {
                        "success": False,
                        "error": "No predictions returned from Imagen 4 Ultra"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Transformation failed: {response.status_code} - {response.text}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Cosplay transformation error: {str(e)}"
            }