"""
Character library for cosplay generation
"""
from typing import Dict, List, Any

class CharacterLibrary:
    def __init__(self):
        self.characters = self._initialize_characters()
    
    def _initialize_characters(self) -> Dict[str, Dict[str, Any]]:
        """Initialize character definitions"""
        return {
            "sailor-moon": {
                "name": "Sailor Moon",
                "style": "anime",
                "costume": "detailed blue sailor costume with white collar and red bow",
                "accessories": "moon tiara, white gloves, red ribbons in hair",
                "hair": "blonde twin tails with red ribbons",
                "pose": "magical girl pose with hand on hip",
                "colors": ["blue", "white", "red", "yellow"],
                "description": "Classic anime magical girl with sailor uniform"
            },
            "wonder-woman": {
                "name": "Wonder Woman",
                "style": "superhero",
                "costume": "red and gold armor with blue star-spangled briefs",
                "accessories": "golden tiara, lasso of truth, silver bracelets",
                "hair": "long dark hair",
                "pose": "heroic power pose with arms crossed",
                "colors": ["red", "gold", "blue", "silver"],
                "description": "Amazonian warrior princess with iconic superhero costume"
            },
            "dva": {
                "name": "D.Va",
                "style": "gaming",
                "costume": "white and pink mech pilot suit with blue accents",
                "accessories": "gaming headset, pink bunny ears, blue visor",
                "hair": "brown hair in twin tails",
                "pose": "gaming victory pose",
                "colors": ["white", "pink", "blue", "brown"],
                "description": "Professional gamer and mech pilot from Overwatch"
            },
            "harley-quinn": {
                "name": "Harley Quinn",
                "style": "comic",
                "costume": "red and black jester outfit with diamond patterns",
                "accessories": "red and black hair, white face paint, mallet",
                "hair": "red and black pigtails",
                "pose": "mischievous pose with mallet",
                "colors": ["red", "black", "white"],
                "description": "Chaotic villain with jester-inspired costume"
            },
            "zelda": {
                "name": "Princess Zelda",
                "style": "fantasy",
                "costume": "elegant white and gold dress with royal symbols",
                "accessories": "golden crown, royal jewelry, magical aura",
                "hair": "blonde hair in elegant style",
                "pose": "regal pose with hand extended",
                "colors": ["white", "gold", "blue", "green"],
                "description": "Royal princess with magical powers and elegant attire"
            },
            "power-girl": {
                "name": "Power Girl",
                "style": "superhero",
                "costume": "white costume with blue cape and red S symbol",
                "accessories": "blue cape, red boots, confident expression",
                "hair": "blonde hair in ponytail",
                "pose": "superhero flying pose",
                "colors": ["white", "blue", "red"],
                "description": "Powerful superhero with classic costume design"
            },
            "2b": {
                "name": "2B",
                "style": "gaming",
                "costume": "black and white maid outfit with combat elements",
                "accessories": "white blindfold, black gloves, combat boots",
                "hair": "white hair in elegant style",
                "pose": "combat ready pose",
                "colors": ["black", "white", "silver"],
                "description": "Android combat unit with elegant maid-inspired design"
            },
            "mikasa": {
                "name": "Mikasa Ackerman",
                "series": "Attack on Titan",
                "style": "anime",
                "hair_style": "short black bob cut with straight bangs",
                "hair_color": "black",
                "eye_color": "dark gray",
                "outfit_details": "Survey Corps military uniform with brown cropped jacket over white long-sleeve shirt, white pants with brown knee-high boots, leather harness straps across chest and waist",
                "accessories": "iconic red knitted scarf around neck, ODM gear (Omni-Directional Mobility gear) with gas tanks and blade holders, brown leather straps and buckles, military insignia patches",
                "signature_items": "dual steel blades for ODM gear, silver blade handles",
                "signature_pose": "determined military stance with hand on blade hilt",
                "expression": "serious and determined with piercing gaze",
                "environment": "post-apocalyptic military setting with massive stone walls",
                "costume": "complete Survey Corps uniform with ODM gear harness",
                "hair": "short black bob with bangs",
                "pose": "determined warrior stance",
                "colors": ["brown", "white", "red", "black", "silver", "gray"],
                "description": "Elite soldier from Attack on Titan with iconic red scarf and ODM gear",
                "personality_traits": "fierce, protective, stoic, loyal",
                "key_features": "red scarf (most important), military precision, intense expression, combat-ready posture"
            },
            "catwoman": {
                "name": "Catwoman",
                "style": "comic",
                "costume": "black leather catsuit with cat ears",
                "accessories": "black mask, whip, cat ears, claws",
                "hair": "black hair",
                "pose": "stealthy cat pose",
                "colors": ["black", "silver"],
                "description": "Feline-themed thief with sleek black costume"
            },
            "ahri": {
                "name": "Ahri",
                "style": "gaming",
                "costume": "elegant white and gold outfit with fox elements",
                "accessories": "nine fox tails, golden jewelry, magical orbs",
                "hair": "white hair with fox ears",
                "pose": "mystical fox pose",
                "colors": ["white", "gold", "blue"],
                "description": "Nine-tailed fox spirit with elegant magical attire"
            }
        }
    
    def get_character(self, character_id: str) -> Dict[str, Any]:
        """Get character by ID"""
        return self.characters.get(character_id, {})
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """Get all characters"""
        return [
            {
                "id": char_id,
                "name": char_data["name"],
                "style": char_data["style"],
                "description": char_data["description"]
            }
            for char_id, char_data in self.characters.items()
        ]
    
    def get_characters_by_style(self, style: str) -> List[Dict[str, Any]]:
        """Get characters filtered by style"""
        return [
            {
                "id": char_id,
                "name": char_data["name"],
                "style": char_data["style"],
                "description": char_data["description"]
            }
            for char_id, char_data in self.characters.items()
            if char_data["style"] == style
        ]
    
    def get_character_prompt_template(self, character_id: str) -> str:
        """Get prompt template for character"""
        character = self.get_character(character_id)
        if not character:
            return ""
        
        template_parts = [
            character["name"],
            character["costume"],
            character["accessories"],
            character["hair"],
            character["pose"]
        ]
        
        return ", ".join(filter(None, template_parts))
    
    def get_character_colors(self, character_id: str) -> List[str]:
        """Get character's color palette"""
        character = self.get_character(character_id)
        return character.get("colors", [])
    
    def search_characters(self, query: str) -> List[Dict[str, Any]]:
        """Search characters by name or description"""
        query_lower = query.lower()
        results = []
        
        for char_id, char_data in self.characters.items():
            if (query_lower in char_data["name"].lower() or 
                query_lower in char_data["description"].lower() or
                query_lower in char_data["style"].lower()):
                results.append({
                    "id": char_id,
                    "name": char_data["name"],
                    "style": char_data["style"],
                    "description": char_data["description"]
                })
        
        return results