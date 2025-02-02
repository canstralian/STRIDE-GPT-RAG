import streamlit as st
import random
from utils.input import get_input
from utils.repo_analysis import analyze_github_repo
from utils.load_env import load_env_variables
from utils.mermaid import mermaid

# STRIDE categories
STRIDE_CATEGORIES = {
    'Spoofing': 'Impersonating another user or system.',
    'Tampering': 'Modifying data or code to disrupt or manipulate.',
    'Repudiation': 'Claiming to have not performed an action that has occurred.',
    'Information Disclosure': 'Exposing confidential information.',
    'Denial of Service': 'Disrupting or denying access to services.',
    'Elevation of Privilege': 'Gaining unauthorized access to resources.'
}

def rag_model(query):
    """Simulates a retrieval-augmented generation model."""
    responses = [
        "Consider implementing multi-factor authentication.",
        "Regularly audit your systems for vulnerabilities.",
        "Use encryption for sensitive data in transit.",
        "Implement logging and monitoring to detect anomalies.",
        "Conduct regular security training for employees."
    ]
    return random.choice(responses)

def analyze_threats(threat_description):
    """Analyzes the threat based on the STRIDE framework."""
    threats = []
    for category, description in STRIDE_CATEGORIES.items():
        if category.lower() in threat_description.lower():
            threats.append((category, description))
    
    if not threats:
        return "No threats identified based on the STRIDE framework."
    
    return threats

# Load environment variables
load_env_variables()

# Streamlit page configuration
st.set_page_config(
    page_title="STRIDE GPT",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar configuration
st.sidebar.image("logo.png")
st.sidebar.header("How to use STRIDE GPT")

with st.sidebar:
    model_provider = st.selectbox(
        "Select your preferred model provider:",
        ["OpenAI API", "Anthropic API", "Azure OpenAI Service", "Google AI API", "Mistral API", "Ollama"],
        key="model_provider",
        help="Select the model provider you would like to use. This will determine the models available for selection.",
    )

    if model_provider == "OpenAI API":
        st.markdown(
            """
            1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) and chosen model below 🔑
            2. Provide details of the application that you would like to threat model  📝
            3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
            """
        )
        openai_api_key = st.text_input(
            "Enter your OpenAI API key:",
            value=st.session_state.get('openai_api_key', ''),
            type="password",
            help="You can find your OpenAI API key on the [OpenAI dashboard](https://platform.openai.com/account/api-keys).",
        )
        if openai_api_key:
            st.session_state['openai_api_key'] = openai_api_key

        selected_model = st.selectbox(
            "Select the model you would like to use:",
            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            key="selected_model",
            help="GPT-4o and GPT-4o mini are OpenAI's latest models and are recommended."
        )

    if model_provider == "Anthropic API":
        st.markdown(
            """
            1. Enter your [Anthropic API key](https://console.anthropic.com/settings/keys) and chosen model below 🔑
            2. Provide details of the application that you would like to threat model  📝
            3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
            """
        )
        anthropic_api_key = st.text_input(
            "Enter your Anthropic API key:",
            value=st.session_state.get('anthropic_api_key', ''),
            type="password",
            help="You can find your Anthropic API key on the [Anthropic console](https://console.anthropic.com/settings/keys).",
        )
        if anthropic_api_key:
            st.session_state['anthropic_api_key'] = anthropic_api_key

        anthropic_model = st.selectbox(
            "Select the model you would like to use:",
            ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest"],
            key="selected_model",
        )

    if model_provider == "Azure OpenAI Service":
        st.markdown(
            """
            1. Enter your Azure OpenAI API key, endpoint and deployment name below 🔑
            2. Provide details of the application that you would like to threat model  📝
            3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
            """
        )

        azure_api_key = st.text_input(
            "Azure OpenAI API key:",
            value=st.session_state.get('azure_api_key', ''),
            type="password",
            help="You can find your Azure OpenAI API key on the [Azure portal](https://portal.azure.com/).",
        )
        if azure_api_key:
            st.session_state['azure_api_key'] = azure_api_key

        azure_api_endpoint = st.text_input(
            "Azure OpenAI endpoint:",
            value=st.session_state.get('azure_api_endpoint', ''),
            help="Example endpoint: https://YOUR_RESOURCE_NAME.openai.azure.com/",
        )
        if azure_api_endpoint:
            st.session_state['azure_api_endpoint'] = azure_api_endpoint

        azure_deployment_name = st.text_input(
            "Deployment name:",
            value=st.session_state.get('azure_deployment_name', ''),
        )
        if azure_deployment_name:
            st.session_state['azure_deployment_name'] = azure_deployment_name

        st.info("Please note that you must use an 1106-preview model deployment.")
        azure_api_version = '2023-12-01-preview'
        st.write(f"Azure API Version: {azure_api_version}")

    if model_provider == "Google AI API":
        st.markdown(
            """
            1. Enter your [Google AI API key](https://makersuite.google.com/app/apikey) and chosen model below 🔑
            2. Provide details of the application that you would like to threat model  📝
            3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
            """
        )
        google_api_key = st.text_input(
            "Enter your Google AI API key:",
            value=st.session_state.get('google_api_key', ''),
            type="password",
            help="You can generate a Google AI API key in the [Google AI Studio](https://makersuite.google.com/app/apikey).",
        )
        if google_api_key:
            st.session_state['google_api_key'] = google_api_key

        google_model = st.selectbox(
            "Select the model you would like to use:",
            ["gemini-1.5-pro-latest", "gemini-1.5-pro"],
            key="selected_model",
        )

    if model_provider == "Mistral API":
        st.markdown(
            """
            1. Enter your [Mistral API key](https://console.mistral.ai/api-keys/) and chosen model below 🔑
            2. Provide details of the application that you would like to threat model  📝
            3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
            """
        )
        mistral_api_key = st.text_input(
            "Enter your Mistral API key:",
            value=st.session_state.get('mistral_api_key', ''),
            type="password",
            help="You can generate a Mistral API key in the [Mistral console](https://console.mistral.ai/api-keys/).",
        )
        if mistral_api_key:
            st.session_state['mistral_api_key'] = mistral_api_key

        mistral_model = st.selectbox(
            "Select the model you would like to use:",
            ["mistral-large-latest", "mistral-small-latest"],
            key="selected_model",
        )

    if model_provider == "Ollama":
        try:
            response = requests.get("http://localhost:11434/api/tags")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error("Ollama endpoint not found, please select a different model provider.")
            response = None

        if response:
            data = response.json()
            available_models = [model["name"] for model in data["models"]]
            ollama_model = st.selectbox(
                "Select the model you would like to use:",
                available_models,
                key="selected_model",
            )

    github_api_key = st.sidebar.text_input(
        "Enter your GitHub API key (optional):",
        value=st.session_state.get('github_api_key', ''),
        type="password",
        help="You can find or create your GitHub API key in your GitHub account settings under Developer settings > Personal access tokens.",
    )
    if github_api_key:
        st.session_state['github_api_key'] = github_api_key

    st.markdown("---")

st.sidebar.header("About")

with st.sidebar:
    st.markdown(
        "Welcome to STRIDE GPT, an AI-powered tool designed to help teams produce better threat models for their applications."
    )
    st.markdown(
        "Threat modelling is a key activity in the software development lifecycle, but is often overlooked or poorly executed. STRIDE GPT aims to help teams produce more comprehensive threat models."
    )
    st.markdown("Created by [Matt Adams](https://www.linkedin.com/in/matthewrwadams/).")
    st.sidebar.markdown(
        "⭐ Star on GitHub: [![Star on GitHub](https://img.shields.io/github/stars/mrwadams/stride-gpt?style=social)](https://github.com/mrwadams/stride-gpt)"
    )
    st.markdown("---")

st.sidebar.header("Example Application Description")

with st.sidebar:
    st.markdown(
        "Below is an example application description that you can use to test STRIDE GPT:"
    )
    st.markdown(
        "> A web application that allows users to create, store, and share personal notes. The application is built using the React frontend framework and a Node.js backend with a MongoDB database."
    )
    st.markdown("---")

st.sidebar.header("FAQs")

with st.sidebar:
    st.markdown(
        """
        ### **What is STRIDE?**
        STRIDE is a threat modeling methodology that helps to identify and categorise potential security risks in software applications. It stands for **S**poofing, **T**ampering, **R**epudiation, **I**nformation Disclosure, **D**enial of Service, and **E**levation of Privilege.
        """
    )
    st.markdown(
        """
        ### **How does STRIDE GPT work?**
        When you enter an application description and other relevant details, the tool will use a GPT model to generate a threat model for your application. The model uses the application description to identify potential threats and provide suggestions for mitigating those threats.
        """
    )
    st.markdown(
        """
        ### **Do you store the application details provided?**
        No, STRIDE GPT does not store your application description or other details. All entered data is deleted after you close the browser tab.
        """
    )
    st.markdown(
        """
        ### **Why does it take so long to generate a threat model?**
        If you are using a free OpenAI API key, it will take a while to generate a threat model. This is because the free API key has strict rate limits. To speed up the process, you can use a paid API key.
        """
    )
    st.markdown(
        """
        ### **Are the threat models 100% accurate?**
        No, the threat models are not 100% accurate. STRIDE GPT uses GPT Large Language Models (LLMs) to generate its output. The GPT models are powerful, but they sometimes make mistakes and are prone to hallucinations. Always review the generated threat models and use them as a guide.
        """
    )
    st.markdown(
        """
        ### **How can I improve the accuracy of the threat models?**
        You can improve the accuracy of the threat models by providing a detailed description of the application and selecting the correct application type, authentication methods, and other relevant details.
        """
    )

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Threat Model", "Attack Tree", "Mitigations", "DREAD", "Test Cases"])

with tab1:
    st.markdown(
        """
        A threat model helps identify and evaluate potential security threats to applications/systems. It provides a systematic approach to 
        understanding possible vulnerabilities and attack vectors. Use this tab to generate a threat model using the STRIDE methodology.
        """
    )
    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    threat_description = st.text_input("Please describe the potential threat:")

    if st.button("Analyze Threat"):
        identified_threats = analyze_threats(threat_description)
        
        if isinstance(identified_threats, str):
            st.write(identified_threats)
        else:
            st.write("Identified Threats:")
            for category, description in identified_threats:
                st.write(f"{category}: {description}")
            
            # Generate RAG response
            rag_response = rag_model(threat_description)
            st.write(f"\nRAG Suggestion: {rag_response}")

if 'app_input' not in st.session_state:
    st.write("app_input not found in session state.")
