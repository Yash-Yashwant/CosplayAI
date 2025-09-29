# 🎭 Cosplay AI Generator - Imagen 4 Ultra

**Simple, all-in-one cosplay transformation using Google's Imagen 4 Ultra**

Transform any photo into professional cosplay images with detailed character accuracy.

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Google Cloud**
   - Edit `.env` file with your project details
   - Add your `google-credentials.json` file

3. **Add Model Photos**
   - Put your photos in the `models/` folder
   - Supported formats: JPG, PNG, JPEG

4. **Generate Cosplay**
   ```bash
   python generate.py model1.jpg mikasa
   python generate.py model1.jpg sailor-moon custom_name
   ```

## 📁 Project Structure

```
cosplay-simple/
├── models/           # Put your model photos here
├── output/          # Generated cosplay images
├── .env             # Google Cloud configuration
├── characters.json  # Character definitions & prompts
├── generate.py      # Command line generator
├── cosplay_generator.ipynb  # Jupyter notebook version
└── requirements.txt # Python dependencies
```

## 🎭 Available Characters

- **Mikasa Ackerman** (Attack on Titan) - Military uniform, red scarf, ODM gear
- **Sailor Moon** - Blue sailor costume, twin tails, moon tiara
- **Wonder Woman** - Red/gold armor, lasso of truth, heroic pose

## 💻 Usage Options

### Command Line
```bash
python generate.py <image_file> <character> [output_name]
```

### Jupyter Notebook
Open `cosplay_generator.ipynb` for interactive generation with detailed feedback.

## ⚙️ Configuration

### .env File
```
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
IMAGEN_LOCATION=us-central1
```

### Google Cloud Setup
1. Create Google Cloud project
2. Enable Vertex AI API
3. Create service account with Vertex AI User role
4. Download service account key as `google-credentials.json`

## 🎨 Character Customization

Edit `characters.json` to add new characters or modify prompts:

```json
{
  "character_id": {
    "name": "Character Name",
    "series": "Series Name",
    "prompt": "Detailed transformation prompt with all visual elements..."
  }
}
```

## 💰 Cost

- **Imagen 4 Ultra**: $0.06 per image
- **High quality results** with detailed character accuracy
- **Perfect for professional cosplay transformations**

## 🎯 For OnlyFans Creators

- High-quality results suitable for professional content
- Detailed character accuracy for authentic cosplay
- Fast generation times for content creation workflows
- Batch processing capabilities for multiple characters

## 🔧 Demo Mode

Runs automatically if Google Cloud credentials aren't configured - creates placeholder images for testing the workflow.

## 📊 Example Results

Generated images are saved with timestamps in the `output/` folder:
- `mikasa_20241227_143022.png`
- `sailor-moon_20241227_143045.png`

Perfect for presentations, demos, and production use!