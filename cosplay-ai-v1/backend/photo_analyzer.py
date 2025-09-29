"""
Image analysis utilities for cosplay generation
"""
import cv2
import numpy as np
from PIL import Image
import io
from typing import Dict, Any, Optional, Tuple
import colorsys

class PhotoAnalyzer:
    def __init__(self):
        self.min_size = (512, 512)
        self.max_size = (2048, 2048)
        
        # Color ranges for hair detection (HSV)
        self.hair_colors = {
            "blonde": [(20, 50, 50), (30, 255, 255)],
            "brunette": [(10, 50, 50), (20, 255, 255)],
            "black": [(0, 0, 0), (180, 255, 50)],
            "red": [(0, 50, 50), (10, 255, 255)],
            "gray": [(0, 0, 50), (180, 30, 200)]
        }
        
        # Skin tone ranges
        self.skin_tones = {
            "light": [(0, 20, 70), (20, 150, 255)],
            "medium": [(0, 20, 20), (20, 150, 200)],
            "dark": [(0, 20, 0), (20, 150, 150)]
        }
    
    def analyze_photo(self, image_data: bytes) -> Dict[str, Any]:
        """
        Analyze uploaded photo for cosplay generation
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Load and validate image
            image = self._load_image(image_data)
            if not image:
                return {"error": "Invalid image format"}
            
            # Perform analysis
            analysis = {
                "dimensions": image.shape[:2],
                "aspect_ratio": image.shape[1] / image.shape[0],
                "quality_score": self._assess_quality(image),
                "hair_color": self._detect_hair_color(image),
                "skin_tone": self._detect_skin_tone(image),
                "pose": self._detect_pose(image),
                "style_cues": self._detect_style_cues(image),
                "face_detected": self._detect_face(image)
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _load_image(self, image_data: bytes) -> Optional[np.ndarray]:
        """Load and validate image"""
        try:
            # Convert bytes to PIL Image
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to OpenCV format
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Validate size
            if image.shape[0] < self.min_size[0] or image.shape[1] < self.min_size[1]:
                return None
            
            return image
            
        except Exception:
            return None
    
    def _assess_quality(self, image: np.ndarray) -> float:
        """Assess image quality using Laplacian variance"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Normalize to 0-1 scale
        return min(laplacian_var / 1000, 1.0)
    
    def _detect_hair_color(self, image: np.ndarray) -> str:
        """Detect dominant hair color"""
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Simple approach: analyze top portion of image for hair
        height, width = image.shape[:2]
        hair_region = hsv[:height//3, :]  # Top third of image
        
        # Count pixels in each hair color range
        color_counts = {}
        for color_name, (lower, upper) in self.hair_colors.items():
            mask = cv2.inRange(hair_region, np.array(lower), np.array(upper))
            color_counts[color_name] = cv2.countNonZero(mask)
        
        # Return most common color
        return max(color_counts, key=color_counts.get) if color_counts and any(color_counts.values()) else "unknown"
    
    def _detect_skin_tone(self, image: np.ndarray) -> str:
        """Detect skin tone"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Analyze center portion for skin
        height, width = image.shape[:2]
        skin_region = hsv[height//3:2*height//3, width//4:3*width//4]
        
        # Count pixels in each skin tone range
        tone_counts = {}
        for tone_name, (lower, upper) in self.skin_tones.items():
            mask = cv2.inRange(skin_region, np.array(lower), np.array(upper))
            tone_counts[tone_name] = cv2.countNonZero(mask)
        
        return max(tone_counts, key=tone_counts.get) if tone_counts and any(tone_counts.values()) else "unknown"
    
    def _detect_pose(self, image: np.ndarray) -> str:
        """Detect basic pose type"""
        # Simple pose detection based on image dimensions and content
        height, width = image.shape[:2]
        aspect_ratio = width / height
        
        if aspect_ratio > 1.2:
            return "wide pose"
        elif aspect_ratio < 0.8:
            return "tall pose"
        else:
            return "standard pose"
    
    def _detect_style_cues(self, image: np.ndarray) -> list:
        """Detect style cues from image"""
        cues = []
        
        # Analyze brightness
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        if brightness > 150:
            cues.append("bright lighting")
        elif brightness < 80:
            cues.append("dark lighting")
        
        # Analyze color saturation
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = np.mean(hsv[:, :, 1])
        
        if saturation > 100:
            cues.append("vibrant colors")
        elif saturation < 50:
            cues.append("muted colors")
        
        return cues
    
    def _detect_face(self, image: np.ndarray) -> bool:
        """Detect if face is present in image"""
        # Load Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return len(faces) > 0
    
    def validate_image(self, image_data: bytes) -> Tuple[bool, str]:
        """
        Validate image for cosplay generation
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            image = self._load_image(image_data)
            if not image:
                return False, "Invalid image format"
            
            # Check size
            height, width = image.shape[:2]
            if height < self.min_size[0] or width < self.min_size[1]:
                return False, f"Image too small. Minimum size: {self.min_size}"
            
            if height > self.max_size[0] or width > self.max_size[1]:
                return False, f"Image too large. Maximum size: {self.max_size}"
            
            # Check quality
            quality_score = self._assess_quality(image)
            if quality_score < 0.1:
                return False, "Image quality too low"
            
            return True, ""
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"