# Session Log: AI Video Generation Research & Alternatives

**Session Context:** The user was exploring how to generate AI videos for free or cheaply using Google's models (Gemini Omni Flash, Veo, Flow) and open-source models (LTX-2.5, Wan 2.1), along with troubleshooting Google Cloud billing in India.

## 1. Gemini Enterprise & Google Flow Credits
- **Question:** Does Gemini Enterprise have a 30-day trial and include Flow credits?
- **Finding:** Gemini Enterprise does have a 30-day free trial, but it **does not include Flow credits**. Flow credits are specific to consumer-facing Google AI Plus/Pro plans used in the creative studio for models like Veo 3.1 and Gemini Omni Flash.

## 2. Gemini API Free Tier
- **Question:** How to get free Gemini API credits?
- **Finding:** No "credits" are needed. Google AI Studio offers a permanent **Free Tier** for API keys with rate limits. It grants access to text/multimodal models (like Gemini 1.5 Flash and Pro) without needing a credit card. However, prompts/responses on the free tier may be used by Google for training.

## 3. The $300 Vertex AI Trial vs. Flow Credits
- **Question:** Does the $300 Vertex AI trial give Flow credits, and how do API keys help make video?
- **Finding:** No. The $300 is a dollar amount applied to Google Cloud billing. It pays for real compute usage (like API calls) instead of consumer tokens. An API key allows you to write scripts (e.g., in Python) to request video generation programmatically from models like **Veo 3.1** or **Gemini Omni Flash** rather than using a website interface.

## 4. API Key Testing & Omni Flash Prompt
- **Action Taken:** The user provided an API key to test video generation.
- **Result:** We wrote a Python script (`generate_video.py`) using the `google-genai` SDK and the `veo-3.1-generate-preview` model. Upon execution, the API returned a `429 RESOURCE_EXHAUSTED` error, indicating the key lacked the required paid billing quota.
- **Artifact Provided:** We generated a strict, structured JSON prompt designed to bypass Google Flow's reputational risk filters (using the DVS protocol). 
```json
{
  "policy_frame": "Scene from a fictional cinematic film. All characters, names, locations, and events are entirely fictional.",
  "environment": {
    "tag": "@CyberpunkCity",
    "description": "A dark, futuristic metropolis at night. Streets reflect vibrant neon pink and cyan lights from towering skyscrapers. Rain slicks the asphalt.",
    "enforce": "Use the exact visual of a high-tech neon city at night."
  },
  "action": {
    "0-2s": "Establish: A sleek, low-profile futuristic sports car sits idling on the wet street, engine glowing.",
    "2-4s": "Development: The car accelerates rapidly forward, splashing water.",
    "4-6s": "Core action: The camera tracks alongside the car as it speeds past neon storefronts."
  },
  "camera": {
    "shot_type": "Close-up to Medium shot",
    "lens": "35mm",
    "angle": "Low angle, street level",
    "movement": "Fast tracking shot alongside the vehicle"
  },
  "lighting": "High contrast cinematic lighting. Bright neon pink and cyan practical lights reflecting off wet surfaces and the metallic car body.",
  "style": "Photorealistic, high octane, cinematic, film grain, 16:9, 4K."
}
```

## 5. Google Billing Errors in India (`OR_BACR2_44`)
- **Action Taken:** User shared screenshots of a billing failure (`OR_BACR2_44`) when trying to use UPI QR code for the $300 free trial, alongside their AI Studio API keys.
- **Finding:** UPI recurring mandates often fail for Google Cloud verification due to RBI regulations. 
- **Solution:** Use a standard Credit Card with international transactions enabled.
- **Clarification:** The $300 credit **explicitly excludes the Gemini API**. Video generation via the Gemini API (Veo) has **no free tier** and costs ~$0.15 - $0.75 per second of video. 

## 6. Open Source Models & Zero-Cost Pipeline
- **Question:** What about open-source models like LTX-2.5, Wan 2.1, and using Remotion/FFmpeg?
- **Finding:** Open-source is the best path to free video generation.
- **Top Models:** 
  1. **Wan 2.2** (Best overall quality, Apache 2.0)
  2. **HunyuanVideo** (Cinematic)
  3. **LTX-2.5** (Fast, native audio sync)
- **Pipeline:** You can run these models on free cloud GPUs (like Google Colab T4 or Kaggle P100). The models output raw 5-10s clips. You then use **FFmpeg** to stitch and compress them, and **Remotion** to add animated text, branding, and motion graphics.
- **Artifact Created:** A detailed markdown report (`open_source_video_research.md`) was created comparing these models and hardware requirements.

## 7. Scaling Up: Using the $300 Trial for Open Source
- **Question:** How many videos can I make at once for free, and does the $300 trial help?
- **Finding:** 
  - Free platforms (Colab/Kaggle) only allow **1 video at a time** (sequential, slow).
  - **The $300 trial is useful here:** While it excludes the Gemini API, it can be used for **Google Compute Engine**. You can rent GPU VMs (like NVIDIA T4 or L4) for ~$0.35 - $0.80/hour. With $300, you can run multiple VMs in parallel for hundreds of hours, enabling you to bulk-generate thousands of open-source AI video clips without spending real money.

## 8. Alternative Unconventional Strategies
- **Question:** What are other ideas I haven't thought of?
- **Provided Ideas:**
  1. **Credit Stacking:** Use 5 different free sites daily (Hailuo, Kling, PixVerse, Luma, Haiper) for ~30-40 free clips/day.
  2. **Serverless GPU APIs:** Use platforms like **fal.ai** or **replicate.com** to pay per video (~₹2-5/clip) instead of renting whole GPUs.
  3. **Cheap Indian GPU Providers:** Rent from JarvisLabs, E2E Networks, or Vast.ai (prices are 40-70% cheaper than Google Cloud, with INR/UPI billing).
  4. **ComfyUI Cloud:** Use ThinkDiffusion or RunComfy for zero-setup open-source video generation in the browser.
  5. **Model Aggregators:** Use WaveSpeed or Krea to compare Sora, Veo, Kling, and Wan outputs side-by-side before spending credits.

---
*This file contains the full record of research, code, prompts, and strategies discussed in the session.*
