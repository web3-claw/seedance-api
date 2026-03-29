# Seedance 2.0 — Character Consistency

Generate videos featuring the same fictional character across multiple scenes using the Seedance 2.0 character workflow.

---

## How It Works

The workflow has two steps:

1. **Create a character sheet** — Upload 1–5 reference photos of a real person plus an outfit/style description. The API renders a structured character sheet (front view, back view, side profile, action pose, facial expressions, accessories) at 4K / 21:9. You receive a `request_id`.
2. **Use the character in videos** — Reference the character inline in any prompt using `@character:<request_id>`. Works with Text-to-Video, Image-to-Video, and Omni-Reference.

---

## Step 1 — Create a Character

**Endpoint:** `POST /api/v1/seedance-2-character`

| Field | Type | Required | Description |
|---|---|---|---|
| `images_list` | array of URLs | Yes | 1–5 photos of the reference person |
| `outfit_description` | string | Yes | Desired outfit/style for the character |
| `character_name` | string | No | Optional display name |

**Example request:**
```json
{
  "images_list": ["https://example.com/person.jpg"],
  "outfit_description": "cyberpunk jacket with neon blue accents, black tactical pants, worn boots",
  "character_name": "Nova"
}
```

**Example response:**
```json
{
  "request_id": "ab539e5f-1234-5678-abcd-ef0123456789"
}
```

Poll `GET /api/v1/predictions/<request_id>/result` until `status` is `completed`. The result contains the character sheet image URL.

**Cost:** $0.18 per character sheet

---

## Step 2 — Use the Character in a Video

Once the character is ready, embed it in any prompt with:

```
@character:<request_id>
```

### Text-to-Video

```json
{
  "prompt": "@character:ab539e5f-1234-... walks through a rain-soaked neon city at night",
  "aspect_ratio": "16:9",
  "duration": 5,
  "quality": "basic"
}
```

### Image-to-Video

```json
{
  "prompt": "@character:ab539e5f-1234-... looks out over the city from a rooftop",
  "images_list": ["https://example.com/background.jpg"],
  "aspect_ratio": "16:9",
  "duration": 5
}
```

### Omni-Reference (image + video + audio)

```json
{
  "prompt": "@character:ab539e5f-1234-... enters the scene and picks up the artifact",
  "aspect_ratio": "16:9",
  "duration": 6,
  "images_list": ["https://example.com/scene.jpg"],
  "video_files": ["https://example.com/intro_clip.mp4"]
}
```

### Multiple Characters

You can reference more than one character in the same prompt:

```
"@character:ab539e5f-... and @character:cd781a2b-... face each other in the arena"
```

---

## Python Example

```python
from seedance_api import SeedanceAPI

api = SeedanceAPI()

# Step 1 — Create the character
char = api.create_character(
    images_list=["https://example.com/person.jpg"],
    outfit_description="cyberpunk jacket with neon blue accents, black tactical pants",
    character_name="Nova"
)
char_id = char["request_id"]
print(f"Character ID: {char_id}")

# Wait for the character sheet to render
api.wait_for_completion(char_id)
print("Character sheet ready.")

# Step 2 — Generate a video using the character
video = api.text_to_video(
    prompt=f"@character:{char_id} rides a motorcycle through a neon-lit city at night",
    aspect_ratio="16:9",
    duration=5,
    quality="basic"
)
result = api.wait_for_completion(video["request_id"])
print(f"Video URL: {result['url']}")
```

---

## Tips for Best Results

- **Reference photos:** Use clear, well-lit frontal and 3/4-angle shots. Avoid heavy shadows or obscured faces.
- **Outfit description:** Be specific — mention materials, colors, and distinctive details. Vague descriptions produce generic outfits.
- **Prompt framing:** Describe what the character *does*, not what they *look like* — the sheet already carries the visual identity.
- **Consistency across scenes:** Reuse the same `request_id` across all shots in a series to keep the character identical.
- **Duration:** For scenes with complex character movement, use `duration=8` and `quality=high` for smoother results.
