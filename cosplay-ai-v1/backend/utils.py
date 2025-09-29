"""
Utility functions for Cosplay AI
"""
import os
import uuid
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json

def generate_unique_id() -> str:
    """Generate unique ID for generations"""
    return str(uuid.uuid4())

def hash_image_data(image_data: bytes) -> str:
    """Generate hash for image data"""
    return hashlib.md5(image_data).hexdigest()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_file_extension(filename: str, allowed_extensions: list = None) -> bool:
    """Validate file extension"""
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    
    _, ext = os.path.splitext(filename.lower())
    return ext in allowed_extensions

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace problematic characters
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
    sanitized = ''.join(c if c in safe_chars else '_' for c in filename)
    
    # Limit length
    if len(sanitized) > 100:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:100-len(ext)] + ext
    
    return sanitized

def create_upload_path(base_dir: str, filename: str) -> str:
    """Create upload path with date-based organization"""
    now = datetime.now()
    date_path = now.strftime("%Y/%m/%d")
    full_path = os.path.join(base_dir, date_path)
    
    # Create directory if it doesn't exist
    os.makedirs(full_path, exist_ok=True)
    
    # Generate unique filename
    name, ext = os.path.splitext(filename)
    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    
    return os.path.join(full_path, unique_name)

def estimate_generation_time(character: str, quality: str, image_size: tuple) -> int:
    """Estimate generation time in seconds"""
    base_time = 30  # Base time for Imagen Pro
    
    # Adjust for quality
    quality_multipliers = {
        "high": 1.5,
        "medium": 1.0,
        "low": 0.7
    }
    
    # Adjust for image size
    size_multiplier = 1.0
    if image_size[0] * image_size[1] > 1024 * 1024:  # Large image
        size_multiplier = 1.2
    
    # Adjust for character complexity
    complex_characters = ["wonder-woman", "zelda", "2b"]
    complexity_multiplier = 1.1 if character in complex_characters else 1.0
    
    estimated_time = int(
        base_time * 
        quality_multipliers.get(quality, 1.0) * 
        size_multiplier * 
        complexity_multiplier
    )
    
    return max(estimated_time, 15)  # Minimum 15 seconds

def format_generation_status(status: str) -> str:
    """Format generation status for display"""
    status_map = {
        "processing": "Generating your cosplay image...",
        "completed": "Generation complete!",
        "failed": "Generation failed",
        "queued": "Waiting in queue..."
    }
    
    return status_map.get(status, status.title())

def create_error_response(error_type: str, message: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create standardized error response"""
    response = {
        "error": True,
        "error_type": error_type,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if details:
        response["details"] = details
    
    return response

def create_success_response(data: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

def validate_environment_variables() -> Dict[str, bool]:
    """Validate required environment variables"""
    required_vars = [
        "GOOGLE_CLOUD_PROJECT_ID",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "IMAGEN_LOCATION"
    ]
    
    validation_results = {}
    for var in required_vars:
        validation_results[var] = os.getenv(var) is not None
    
    return validation_results

def get_api_rate_limit_info() -> Dict[str, Any]:
    """Get API rate limit information"""
    return {
        "requests_per_minute": 60,
        "requests_per_hour": 1000,
        "concurrent_generations": 5,
        "max_image_size": "2048x2048",
        "supported_formats": ["JPEG", "PNG", "WebP"]
    }

def calculate_cost_estimate(quality: str, image_count: int = 1) -> Dict[str, Any]:
    """Calculate estimated cost for generation"""
    # Imagen Pro pricing (approximate)
    cost_per_image = {
        "high": 0.05,
        "medium": 0.03,
        "low": 0.02
    }
    
    base_cost = cost_per_image.get(quality, 0.03)
    total_cost = base_cost * image_count
    
    return {
        "cost_per_image": base_cost,
        "total_cost": total_cost,
        "currency": "USD",
        "quality": quality,
        "image_count": image_count
    }