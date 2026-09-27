import time
import os
from google import genai
from google.genai import types

# Set your API key here (get it from aistudio.google.com)
API_KEY = "YOUR_GEMINI_API_KEY"

print("Initializing Gemini API Client...")
client = genai.Client(api_key=API_KEY)

# Describe the video you want to make
prompt = "A cinematic close up of a futuristic sports car driving through a neon-lit cyberpunk city, high quality, 4k"

# We use the Veo model for high quality video generation
model_name = "veo-3.1-generate-preview" 
# You can also use "veo-3.1-fast-generate-preview" for faster results

print(f"Sending prompt to {model_name}...")
print(f"Prompt: '{prompt}'")

try:
    # Start the video generation
    operation = client.models.generate_videos(
        model=model_name,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            negative_prompt="blurry, low quality, distorted",
            aspect_ratio="16:9",
            resolution="720p",
        ),
    )

    print("Generation started. Video creation takes a few minutes. Waiting...")

    # Video generation takes time, so we must poll the server
    while not operation.done:
        print("Still working...")
        time.sleep(20)  # Wait 20 seconds before checking again
        operation = client.operations.get(operation)

    # When done, download the video
    if operation.response and operation.response.generated_videos:
        generated_video = operation.response.generated_videos[0]
        
        output_filename = "generated_ai_video.mp4"
        
        print(f"Video ready! Downloading to {output_filename}...")
        
        # Download and save the video
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_filename)
        
        print(f"Success! Your video is saved in this folder as {output_filename}")
    else:
        print("Video generation failed. No video returned.")

except Exception as e:
    print(f"An error occurred: {e}")
