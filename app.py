import streamlit as st
import google.generativeai as palm
import anthropic
import os

# Initialize APIs
palm_api_key = os.getenv('GOOGLE_PALM_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

# Function to validate API keys
def validate_api_keys():
    if not palm_api_key:
        st.error("Google PaLM API key is missing. Please set the 'GOOGLE_PALM_API_KEY' environment variable.")
        return False
    if not anthropic_api_key:
        st.error("Anthropic API key is missing. Please set the 'ANTHROPIC_API_KEY' environment variable.")
        return False
    return True

# Function to generate response using Google PaLM
def generate_palm_response(prompt):
    try:
        palm.configure(api_key=palm_api_key)
        response = palm.generate_text(
            model='models/text-bison-001',
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=512,
        )
        return response.result
    except Exception as e:
        st.error(f"An error occurred while generating response with Google PaLM: {e}")
        return None

# Function to generate response using Anthropic Claude
def generate_claude_response(prompt):
    try:
        anthropic_client = anthropic.Client(api_key=anthropic_api_key)
        claude_prompt = f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}"
        response = anthropic_client.completions.create(
            model="claude-1",
            prompt=claude_prompt,
            max_tokens_to_sample=512,
            temperature=0.7,
        )
        return response.completion
    except Exception as e:
        st.error(f"An error occurred while generating response with Anthropic Claude: {e}")
        return None

# Streamlit Interface
def main():
    st.title("STRIDE GPT RAG")

    if not validate_api_keys():
        return

    # User input
    user_input = st.text_area("Enter your threat modeling query:")

    # Model selection
    model_choice = st.selectbox("Choose the model to generate response:", ("Google PaLM", "Anthropic Claude"))

    if st.button("Generate Response"):
        if user_input.strip():
            if model_choice == "Google PaLM":
                with st.spinner("Generating response with Google PaLM..."):
                    response = generate_palm_response(user_input)
            else:
                with st.spinner("Generating response with Anthropic Claude..."):
                    response = generate_claude_response(user_input)

            if response:
                st.subheader("Generated Response:")
                st.write(response)
        else:
            st.warning("Please enter a valid query.")

if __name__ == '__main__':
    main()