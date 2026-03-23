---
name: seedance-v2
description: Generate cinematic, high-fidelity AI videos from text prompts and static images using Seedance 2.0 (by ByteDance).
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - MUAPI_API_KEY
      bins:
        - python3.11
    emoji: 🎥
    homepage: https://muapi.ai
    os: ["macos", "linux"]
---

# Seedance V2

Seedance 2.0 is a state-of-the-art video generation model developed by ByteDance. This skill allows you to generate videos from text, animate images, and edit existing videos using natural language commands.

## Prerequisites

- **MUAPI_API_KEY**: You must have an API key from [muapi.ai](https://muapi.ai). Set it as an environment variable.

## Usage Guide

You can use Seedance 2.0 to create videos in various aspect ratios (16:9, 9:16, 4:3, 3:4) and durations.

### Text-to-Video (T2V)
Generate a video from a descriptive text prompt.
```bash
python3.11 skills/seedance-v2/seedance_cli.py t2v --prompt "A cinematic slow-motion shot of a cyberpunk city in the rain" --wait
```

### Image-to-Video (I2V)
Animate one or more static images.
```bash
python3.11 skills/seedance-v2/seedance_cli.py i2v --images "https://example.com/image.jpg" --prompt "Make the clouds move slowly" --wait
```

### Video Rendering & Editing
Edit an existing video or apply styles.
```bash
python3.11 skills/seedance-v2/seedance_cli.py edit --videos "https://example.com/video.mp4" --prompt "Add a sunset filter" --wait
```

### Extending Videos
Extend a previously generated video segment.
```bash
python3.11 skills/seedance-v2/seedance_cli.py extend --request_id "YOUR_REQUEST_ID" --duration 5 --wait
```

## Tips for Best Results

- **Be Descriptive**: Detailed prompts result in better video quality and more accurate motion.
- **Wait for Completion**: Use the `--wait` flag to receive the final video URL directly. Without it, you will receive a `request_id` which you can check later using the `status` command.
- **Aspect Ratios**: Use `16:9` for horizontal videos and `9:16` for vertical content (like TikTok or Reels).
- **Quality**: Use `--quality high` for 2K resolution, though it may take longer to generate.

## Commands Reference

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `t2v` | `--prompt`, `--aspect_ratio`, `--duration`, `--quality`, `--wait` | Text to Video |
| `i2v` | `--images`, `--prompt`, `--aspect_ratio`, `--duration`, `--quality`, `--wait` | Image to Video |
| `edit` | `--prompt`, `--videos`, `--images`, `--aspect_ratio`, `--quality`, `--wait` | Video Editing |
| `extend`| `--request_id`, `--prompt`, `--duration`, `--quality`, `--wait` | Extend Video |
| `status`| `--request_id` | Check Task Status |
