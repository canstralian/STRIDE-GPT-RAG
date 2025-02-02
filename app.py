import os
import google.generativeai as genai
from transformers import pipeline

# Load API keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Debugging: Ensure API keys are loaded (REMOVE in production)
print(f"GOOGLE_API_KEY Loaded: {bool(GOOGLE_API_KEY)}")
print(f"HF_TOKEN Loaded: {bool(HF_TOKEN)}")

# Ensure API keys are set
if not GOOGLE_API_KEY:
    raise ValueError("❌ Missing GOOGLE_API_KEY. Set it as an environment variable.")

if not HF_TOKEN:
    raise ValueError("❌ Missing HF_TOKEN. Set it as an environment variable.")

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Hugging Face pipeline (example: text generation)
try:
    hf_pipe = pipeline("text-generation", model="gpt2", use_auth_token=HF_TOKEN)
except Exception as e:
    raise RuntimeError(f"Error initializing Hugging Face pipeline: {e}")

def generate_gemini_response(prompt):
    """Generate response from Google's Gemini API."""
    try:
        model = genai.GenerativeModel(model_name="gemini-pro")  # Correct usage
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else "No response from Gemini."
    except Exception as e:
        return f"Error with Gemini API: {e}"

def generate_hf_response(prompt):
    """Generate response from Hugging Face model."""
    try:
        response = hf_pipe(prompt, max_length=100, num_return_sequences=1)
        return response[0]["generated_text"] if response else "No response from HF."
    except Exception as e:
        return f"Error with Hugging Face API: {e}"

if __name__ == "__main__":
    test_prompt = "Tell me a fun fact about space."
    
    print("\n🔹 Google Gemini Response:")
    print(generate_gemini_response(test_prompt))

    print("\n🔹 Hugging Face Response:")
    print(generate_hf_response(test_prompt))
