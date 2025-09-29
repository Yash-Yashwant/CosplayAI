# Cosplay AI Prompt History & Testing Results

This file contains all prompts tested with Imagen 4 Ultra and their performance results.

## Summary
- **Best performing prompt**: User's detailed Mikasa prompt (v4)
- **Key finding**: Face preservation severely limits quality
- **Recommendation**: Use from-scratch generation with detailed prompts

---

## Prompt Version 1 (Initial - Poor Results)
**Character**: Mikasa Ackerman
**Type**: Face preservation attempt
**Result**: ❌ Very poor - anime-style, wrong costume, face not preserved

```
Strictly preserve the exact face, unique identity, and all original facial features of the person from the input image. Do not alter their facial bone structure, skin tone, or expression in any way.

The rest of the person and the scene should be transformed into a hyperrealistic, professional cosplay of Mikasa Ackerman from Attack on Titan. She has short, slightly wavy dark brown hair (like Mikasa's, but integrated naturally with the preserved face). She is wearing a highly detailed, rugged Survey Corps military uniform: a brown cropped leather jacket with the 'Wings of Freedom' emblem prominently displayed on the back and shoulders, a white long-sleeve collared shirt, white pants tucked into tall brown knee-high leather boots, and a complex leather harness system with intricate straps, buckles, and small gas tanks across her chest and waist. A distinctive red knitted scarf is wrapped around her neck, positioned just below the preserved facial features. She is in a determined, powerful military stance, with one hand resting on the hilt of a realistic steel blade, part of the Omni-Directional Mobility (ODM) gear. Her expression remains the same as the original input image but conveys a serious and determined gaze.

The background is a desolate, post-apocalyptic urban environment with ruined, massive stone buildings and debris, reminiscent of the Attack on Titan world. Cinematic, dramatic lighting, sharp focus, ultra high quality, extremely detailed, photorealistic, 8K. No anime style, no cel-shading, no cartoon elements.
```

**API Parameters**:
- editMode: inpainting-replace
- guidanceScale: 120
- stylizationLevel: 100

---

## Prompt Version 2 (Simplified - Poor Results)
**Character**: Mikasa Ackerman
**Type**: Face preservation attempt
**Result**: ❌ Poor - still anime-style, basic costume, face not preserved

```
Keep the exact same face, facial features, skin tone, and facial structure from the original image. Only change the outfit and hair to match Mikasa Ackerman cosplay. Photorealistic style, not anime. The person should wear: dark brown short hair in Mikasa's style, brown cropped military jacket with Wings of Freedom emblem, white shirt, brown leather straps and gear, red scarf. Realistic military cosplay photoshoot, studio lighting, professional photography.
```

**API Parameters**:
- editMode: inpainting-insert
- guidanceScale: 50
- stylizationLevel: (not set)

---

## Prompt Version 3 (Enhanced Details - Poor Results)
**Character**: Mikasa Ackerman
**Type**: Face preservation attempt
**Result**: ❌ Poor - 3D rendering look, wrong costume, face not preserved

```
Professional cosplay photography of this exact person as Mikasa Ackerman from Attack on Titan. PRESERVE ORIGINAL FACE: Keep the exact same facial features, bone structure, eye color, skin tone, and facial expression from the input image. Only transform the outfit and hair.

OUTFIT DETAILS: Highly detailed Survey Corps uniform - brown cropped military leather jacket with intricate stitching and weathered texture, prominent Wings of Freedom emblem embroidered on shoulders and back, crisp white cotton long-sleeve shirt underneath, brown leather ODM gear harness with realistic metal buckles and straps across chest and waist, white military pants tucked into tall brown leather boots with detailed lacing, signature red knitted scarf draped around neck.

HAIR: Transform to Mikasa's iconic short, straight, dark brown bob cut that falls just below the ears, with subtle layers and natural texture.

POSE & SETTING: Confident military stance in a realistic indoor training facility or military headquarters, dramatic cinematic lighting with strong directional shadows, professional photography quality.

STYLE: Hyperrealistic, photographic quality, sharp focus, detailed textures, high-end cosplay photography, studio lighting, 8K resolution. NO anime style, NO cartoon elements, NO 3D rendering look.
```

**API Parameters**:
- editMode: inpainting-replace
- guidanceScale: 150
- stylizationLevel: 50

---

## Prompt Version 4a (From Scratch - Good Results)
**Character**: Mikasa Ackerman
**Type**: Text-to-image generation (no face preservation)
**Result**: ✅ Good - accurate costume, proper hair, photorealistic

```
Professional cosplay photography. Beautiful female cosplay model as Mikasa Ackerman (Face Preserved). Attractive female model with detailed facial features.

OUTFIT DETAILS: Highly detailed Survey Corps uniform - brown cropped military leather jacket with intricate stitching and weathered texture, prominent Wings of Freedom emblem embroidered on shoulders and back, crisp white cotton long-sleeve shirt underneath, brown leather ODM gear harness with realistic metal buckles and straps across chest and waist, white military pants tucked into tall brown leather boots with detailed lacing, signature red knitted scarf draped around neck.

HAIR: Transform to Mikasa's iconic short, straight, dark brown bob cut that falls just below the ears, with subtle layers and natural texture.

POSE & SETTING: Confident military stance in a realistic indoor training facility or military headquarters, dramatic cinematic lighting with strong directional shadows, professional photography quality.

STYLE: Hyperrealistic, photographic quality, sharp focus, detailed textures, high-end cosplay photography, studio lighting, 8K resolution. NO anime style, NO cartoon elements, NO 3D rendering look.
```

**API Parameters**:
- Text-to-image (no editMode)
- stylizationLevel: 100

---

## Prompt Version 4b (User's Detailed Prompt - Excellent Results)
**Character**: Mikasa Ackerman
**Type**: Text-to-image generation (no face preservation)
**Result**: ✅ Excellent - photorealistic, accurate costume, cinematic quality

```
Ultra-realistic, cinematic full-body portrait of Mikasa Ackerman, highly attractive and sensual. She has a seductive expression, dark gray eyes, and short black bob hair with straight bangs.

She is wearing a deconstructed and revealing version of her Survey Corps uniform, reimagined for high fashion and allure. This includes an unbuttoned, cropped brown leather jacket barely covering her, revealing a form-fitting, sheer white bralette or top that accentuates her figure. The iconic red knitted scarf is draped loosely around her neck, drawing attention to her collarbones. Her harness system is stylized and made of sleek, dark leather straps that tastefully highlight her curves, leading to fitted, high-waisted dark shorts or briefs. Tall, glossy brown leather thigh-high boots complete the look.

Her pose is confident and alluring, with a subtle smirk and direct gaze, suggesting power and sensuality. She is leaning against a crumbling, war-torn stone wall in a desolate urban environment, with dramatic, moody lighting casting strong shadows and highlights on her skin and costume. Volumetric dust motes fill the air.

Shot on a high-end cinema camera with a shallow depth of field, sharp focus on her, natural skin texture, incredibly detailed, octane render, 8K, photorealistic, ultra quality, detailed lighting, masterpiece.
```

## Prompt Version 4c

Ultra-realistic, cinematic full-body portrait of Mikasa Ackerman, exquisitely attractive, captivating, and alluring. She has a perfectly symmetrical face, striking dark gray eyes with long, defined eyelashes, and subtle, glossy lips with a natural hue. Her expression is a confident and seductive smirk, enhanced by a direct, piercing gaze. Her hair is a short black bob with straight bangs, styled flawlessly.

She is wearing a deconstructed and revealing version of her Survey Corps uniform, reimagined for high fashion and allure. This includes an unbuttoned, cropped brown leather jacket barely covering her, revealing a form-fitting, sheer white bralette or top that accentuates her figure. The iconic red knitted scarf is draped loosely around her neck, drawing attention to her collarbones. Her harness system is stylized and made of sleek, dark leather straps that tastefully highlight her curves, leading to fitted, high-waisted dark shorts or briefs. Tall, glossy brown leather thigh-high boots complete the look.

Her pose is confident and alluring, with her body language reflecting power and sensuality. She is leaning against a crumbling, war-torn stone wall in a desolate urban environment, with dramatic, moody lighting artfully highlighting her facial contours, cheekbones, and the natural texture of her skin. Volumetric dust motes fill the air.

Shot on a high-end cinema camera with a shallow depth of field, extremely sharp focus on her face and eyes, natural skin texture, incredibly detailed, octane render, 8K, photorealistic, ultra quality, detailed lighting, masterpiece.





**API Parameters**:
- Text-to-image (no editMode)
- stylizationLevel: 100

---

## Key Findings

### What Works:
1. **Text-to-image generation** (no face preservation) produces much better results
2. **Detailed technical specifications** - "Shot on high-end cinema camera", "octane render", "8K"
3. **Professional photography terminology** - Imagen 4 responds well to industry terms
4. **Specific lighting descriptions** - "volumetric dust motes", "dramatic moody lighting"
5. **Quality keywords** - "masterpiece", "ultra quality", "photorealistic"

### What Doesn't Work:
1. **Face preservation** - Severely limits quality and accuracy
2. **Contradictory instructions** - Asking for "no anime" while trying to preserve faces
3. **Low guidance scale** - Under 100 produces poor results
4. **Generic descriptions** - Vague terms don't give good control

### Recommended API Parameters:
- **For text-to-image**: stylizationLevel: 100, aspectRatio: "9:16"
- **For face preservation**: Currently not recommended with Imagen 4 Ultra

### Future Testing:
- Test other characters with user's detailed prompt structure
- Experiment with different stylization levels (50-200)
- Try different aspect ratios for different poses



    "prompt": "Ultra-realistic, cinematic portrait of Mikasa Ackerman, portrayed as an authentically beautiful and captivating real person with a seductive allure. Her face is strikingly lifelike, modeled after a real human with subtle, natural asymmetry, soft contours, and authentic bone structure that conveys depth and personality; hyper-detailed skin texture with visible pores, faint freckles, subtle wrinkles around the eyes and mouth from natural expressions, and minor imperfections like a small mole or uneven skin tone for added realism. Her eyes are a striking dark gray, intensely realistic with intricate iris patterns, subtle blood vessels in the whites, lifelike catchlights reflecting the environment, long natural eyelashes, and slight moisture for a glossy, human-like sheen; they convey depth and emotion as if staring into a real person's soul. Her lips have a natural, slightly parted texture with subtle creases and a hint of color variation, hinting at invitation. Her expression is a sultry and nuanced smirk, with a gaze that is both direct and teasing, featuring lifelike micro-expressions like a subtle twitch at the corner of her mouth or a faint crinkle in her brow, evoking playful desire. Her short black bob hair has a realistic texture, with a few stray strands catching the light, breaking the perfect silhouette and framing her face enticingly. She is wearing a highly detailed Survey Corps uniform with a provocative twist. The brown leather of the cropped jacket is partially unzipped, revealing a glimpse of her toned cleavage and the white shirt beneath, which clings slightly to her form with realistic fabric folds and a few buttons undone for added allure. The iconic red knitted scarf is loosely draped around her neck, made of a believable, tangible wool texture. Her harness system has intricate, functional-looking leather straps and buckles that accentuate her curves. The look is completed with fitted dark shorts that hug her hips tightly, and tall, worn leather boots that add to her commanding yet tempting presence. Her pose is confident, natural, and flirtatious—she is leaning against a crumbling, war-torn stone wall in a desolate urban environment, with one leg slightly bent and her hips subtly tilted forward, emphasizing her figure. The lighting is dramatic but grounded in realism, creating soft shadows and highlights that reveal the texture of her skin, clothing, and the subtle sheen of perspiration on her exposed skin. Shot to emulate a professional portrait photograph taken with a Sony A7R IV and an 85mm F1.4 lens, creating a shallow depth of field. The focus is razor-sharp on her eyes. The final image should be a hyperrealistic, 8K masterpiece, indistinguishable from a real photograph."
