"""
Smart prompt engineering for cosplay image generation
"""
from typing import Dict, Any, Optional
import re

class PromptBuilder:
    def __init__(self):
        self.base_quality_terms = [
            "professional photography",
            "ultra high quality",
            "extremely detailed",
            "studio lighting",
            "sharp focus",
            "perfect cosplay"
        ]

        self.style_modifiers = {
            "anime": "anime style, cel-shaded, vibrant colors, anime-realistic hybrid",
            "realistic": "photorealistic, detailed textures, natural lighting, hyperrealistic",
            "comic": "comic book style, bold lines, dynamic colors, comic accurate",
            "fantasy": "fantasy art style, magical atmosphere, ethereal lighting, mystical",
            "gaming": "game art style, digital painting, vibrant colors, video game accurate"
        }

        self.transformation_templates = {
            "face_preservation": "preserve facial bone structure and basic features while transforming",
            "outfit_change": "completely transform clothing and accessories to match character",
            "style_consistency": "maintain consistent art style throughout the transformation",
            "pose_enhancement": "enhance pose to match character personality and signature stance"
        }
    
    def build_prompt(self, photo_analysis: Dict[str, Any], character: Dict[str, Any], style: str = "anime") -> str:
        """
        Build enhanced prompt for Imagen Pro
        
        Args:
            photo_analysis: Analysis results from uploaded photo
            character: Character definition from library
            style: Visual style preference
            
        Returns:
            Optimized prompt string
        """
        # Extract photo characteristics
        person_desc = self._build_person_description(photo_analysis)
        
        # Get character details
        character_desc = self._build_character_description(character)
        
        # Get style modifiers
        style_desc = self.style_modifiers.get(style, self.style_modifiers["anime"])
        
        # Combine all elements
        prompt_parts = [
            "Professional cosplay photograph of",
            person_desc,
            "as",
            character_desc,
            style_desc,
            ",".join(self.base_quality_terms)
        ]
        
        return ", ".join(filter(None, prompt_parts))

    def build_cosplay_transformation_prompt(self, photo_analysis: Dict[str, Any], character: Dict[str, Any], style: str = "anime") -> str:
        """
        Build comprehensive cosplay transformation prompt for Imagen 4 Ultra

        Args:
            photo_analysis: Analysis results from uploaded photo
            character: Character definition from library
            style: Visual style preference

        Returns:
            Detailed transformation prompt optimized for Imagen 4 Ultra
        """
        # Core transformation instruction
        base_instruction = "Transform this person into a perfect cosplay of"

        # Character-specific details
        character_details = self._build_detailed_character_description(character)

        # Transformation specifications
        transformation_specs = [
            self.transformation_templates["face_preservation"],
            self.transformation_templates["outfit_change"],
            self.transformation_templates["style_consistency"]
        ]

        # Style and quality terms
        style_desc = self.style_modifiers.get(style, self.style_modifiers["anime"])
        quality_terms = ", ".join(self.base_quality_terms)

        # Environment and lighting
        environment = self._get_character_environment(character)

        # Combine all elements with priority order
        prompt_parts = [
            base_instruction,
            character_details,
            ", ".join(transformation_specs),
            style_desc,
            environment,
            quality_terms
        ]

        return ", ".join(filter(None, prompt_parts))

    def _build_detailed_character_description(self, character: Dict[str, Any]) -> str:
        """Build extremely detailed character description for accurate transformation"""
        parts = []

        # Character name and source
        if character.get("name"):
            parts.append(f"{character['name']}")
            if character.get("series"):
                parts.append(f"from {character['series']}")

        # Physical appearance details
        if character.get("hair_style"):
            parts.append(f"with {character['hair_style']}")
        if character.get("hair_color"):
            parts.append(f"{character['hair_color']} hair")
        if character.get("eye_color"):
            parts.append(f"{character['eye_color']} eyes")

        # Costume details (most important for cosplay)
        if character.get("outfit_details"):
            parts.append(f"wearing {character['outfit_details']}")
        if character.get("accessories"):
            parts.append(f"equipped with {character['accessories']}")
        if character.get("signature_items"):
            parts.append(f"holding {character['signature_items']}")

        # Pose and expression
        if character.get("signature_pose"):
            parts.append(f"in {character['signature_pose']}")
        if character.get("expression"):
            parts.append(f"with {character['expression']} expression")

        return " ".join(parts)

    def _get_character_environment(self, character: Dict[str, Any]) -> str:
        """Get appropriate background/environment for character"""
        if character.get("environment"):
            return f"in {character['environment']}"
        elif character.get("series"):
            series_name = character["series"].lower()
            if "attack on titan" in series_name:
                return "in post-apocalyptic military setting with massive walls in background"
            elif "sailor moon" in series_name:
                return "in magical girl setting with sparkles and moon background"
            elif "wonder woman" in series_name:
                return "in heroic pose with ancient Greek architecture background"
        return "in dramatic lighting with appropriate background"
    
    def _build_person_description(self, analysis: Dict[str, Any]) -> str:
        """Build description of person from photo analysis"""
        parts = []
        
        # Basic appearance
        if analysis.get("hair_color"):
            parts.append(f"{analysis['hair_color']} hair")
        
        if analysis.get("skin_tone"):
            parts.append(f"{analysis['skin_tone']} skin")
        
        if analysis.get("pose"):
            parts.append(f"{analysis['pose']} pose")
        
        # Default if no analysis available
        if not parts:
            parts.append("person")
        
        return " ".join(parts)
    
    def _build_character_description(self, character: Dict[str, Any]) -> str:
        """Build character-specific description"""
        parts = [character.get("name", "character")]
        
        if character.get("costume"):
            parts.append(f"wearing {character['costume']}")
        
        if character.get("accessories"):
            parts.append(f"with {character['accessories']}")
        
        return " ".join(parts)
    
    def enhance_prompt_for_quality(self, prompt: str, quality: str = "high") -> str:
        """
        Enhance prompt with quality-specific terms
        """
        quality_modifiers = {
            "high": ["ultra detailed", "8k resolution", "professional grade"],
            "medium": ["detailed", "high resolution", "good quality"],
            "low": ["basic", "standard quality"]
        }
        
        modifiers = quality_modifiers.get(quality, quality_modifiers["medium"])
        return f"{prompt}, {', '.join(modifiers)}"
    
    def sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize prompt to avoid API issues
        """
        # Remove potentially problematic characters
        prompt = re.sub(r'[^\w\s,.-]', '', prompt)
        
        # Limit length (Imagen has token limits)
        if len(prompt) > 500:
            prompt = prompt[:500].rsplit(',', 1)[0]
        
        return prompt.strip()