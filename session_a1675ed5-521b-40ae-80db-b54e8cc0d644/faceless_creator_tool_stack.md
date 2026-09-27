# The Complete Faceless Creator Tool Stack

This document contains every software, AI, and GitHub repository discussed for building a faceless YouTube channel pipeline.

> [!WARNING]
> Do not simply download the `.zip` file from GitHub for the open-source tools. Python and Node.js tools require dependency management. Use `git clone` followed by `npm install` or `pip install` to ensure they work correctly.

---

## 1. Open Source CLI & Programmatic Tools (GitHub Repos)

### Whiteboard & Animation Engines
*   **anything2explainer** (⭐ ~1,300 stars)
    *   **Link:** [https://github.com/Vincentwei1021/anything2explainer](https://github.com/Vincentwei1021/anything2explainer)
    *   **What it does:** Remotion-based explainer generator (generates vector line art and TTS from a topic). PolyForm Noncommercial license.
    *   **How to start:** Clone the repo, run `npm install`, add your API keys to the `.env` file, and run the Remotion build command.
*   **whiteboard-video-engine** (⭐ ~307 stars)
    *   **Link:** [https://github.com/gnipbao/whiteboard-video-engine](https://github.com/gnipbao/whiteboard-video-engine)
    *   **What it does:** Pure Python CLI rendering engine that takes SVGs and text and renders them into whiteboard animations via FFmpeg.
    *   **How to start:** Clone the repo, install requirements (`pip install -r requirements.txt`), and run the CLI script passing your SVG files as arguments.
*   **handanim** (⭐ 48 stars)
    *   **Link:** [https://github.com/subroy13/handanim](https://github.com/subroy13/handanim)
    *   **What it does:** Programmatic Python library for coding math/educational sketches with sketchy human-drawn fills.
    *   **How to start:** Install Cairo on your system, `pip install handanim`, and write a Python script defining your shapes.
*   **whiteboard-animator** (⭐ 37 stars)
    *   **Link:** [https://github.com/masihsultani/whiteboard-animator](https://github.com/masihsultani/whiteboard-animator)
    *   **What it does:** Image-to-video conversion CLI. Creates a stroke-by-stroke reveal of a static image synced to audio.
    *   **How to start:** `pip install whiteboard-animator`. Then run `whiteboard-animate input.png --duration 8 -o output.mp4`.
*   **Inkplainer-OS** (⭐ Unindexed/New)
    *   **Link:** [https://github.com/NadirWeb-App/Inkplainer-OS](https://github.com/NadirWeb-App/Inkplainer-OS)
    *   **What it does:** A completely free, open-source browser-based GUI clone of VideoScribe.
*   **GreaseWriter (Blender)** (⭐ Unindexed/Niche)
    *   **Link:** [https://github.com/doakey3/GreaseWriter](https://github.com/doakey3/GreaseWriter)
    *   **What it does:** A Blender Python add-on that physically simulates human writing physics for text using Grease Pencil.

### Automation, Audio & Subtitles
*   **WhisperX** (⭐ ~23,800 stars)
    *   **Link:** [https://github.com/m-bain/whisperX](https://github.com/m-bain/whisperX)
    *   **What it does:** Generates high-accuracy, word-level timestamps (for kinetic Alex Hormozi-style subtitles) using forced alignment.
    *   **How to start:** `pip install git+https://github.com/m-bain/whisperx.git`. Run: `whisperx video.mp4 --model large-v2`.
*   **faster-whisper** (⭐ ~11,000+ stars)
    *   **Link:** [https://github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
    *   **What it does:** Highly optimized version of OpenAI's Whisper for generating `.srt`/`.vtt` subtitle files 4x faster.
*   **Auto-Editor** (⭐ ~5,000+ stars)
    *   **Link:** [https://github.com/WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor)
    *   **What it does:** CLI tool that automatically removes silence, pauses, and dead air from raw video/audio files.
    *   **How to start:** `pip install auto-editor`. Run: `auto-editor my_video.mp4`.
*   **AI-Youtube-Shorts-Generator** (⭐ ~215 stars)
    *   **Link:** [https://github.com/SaarD00/AI-Youtube-Shorts-Generator](https://github.com/SaarD00/AI-Youtube-Shorts-Generator)
    *   **What it does:** Focuses on automatically fetching stock footage and making smart jump-cuts via FFmpeg.
*   **FreeFaceless** (⭐ Unindexed/New)
    *   **Link:** [https://github.com/nils44344/FreeFaceless](https://github.com/nils44344/FreeFaceless)
    *   **What it does:** End-to-end pipeline (LLM Script -> Edge-TTS -> Scrapes Pexels B-roll -> FFmpeg stitch).

---

## 2. Commercial / Professional Software (Non-GitHub)

### The "Nitish Rajput" Cinematic Stack
*   **Adobe After Effects:** Industry-standard animation software for cinematic motion graphics and parallax photo effects.
*   **GeoLayers 3:** A paid After Effects plugin used to generate high-quality, zooming 3D maps (mandatory for geopolitics).
*   **Adobe Premiere Pro / DaVinci Resolve:** Timeline video editors for final assembly, sound design, and color grading. (DaVinci is free).
*   **Adobe Photoshop:** For cutting out subjects from backgrounds to animate them in After Effects.

### The "Atomic Habits" Whiteboard Stack
*   **VideoScribe (Sparkol):** The exact paid GUI software used in the video analyzed. Auto-animates a hand drawing SVGs.
*   **Doodly:** Budget-friendly, one-time-purchase alternative to VideoScribe.
*   **Explaindio / Vyond:** Commercial GUI software that mixes whiteboard sketching with standard 2D animation.

---

## 3. Web Frameworks & AI Assets

*   **Remotion:** (remotion.dev) (⭐ 20,000+ stars) React-based framework to code videos. Use `@remotion/paths` to programmatically track SVG lines and attach a custom hand image.
*   **ElevenLabs:** The absolute best AI text-to-speech for generating hyper-realistic Hindi and English voiceovers.
*   **Suno:** Generates custom background music based on text prompts.
*   **Envato Elements / Freepik:** Paid/Freemium libraries to download the raw SVG graphics, stock photos, and B-roll.
