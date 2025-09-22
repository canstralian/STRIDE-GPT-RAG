import streamlit as st
import os
from utils.input import get_input
from utils.load_env import load_env
from threat_model import get_threat_model, get_threat_model_azure, get_threat_model_google, get_threat_model_anthropic, get_threat_model_mistral, get_threat_model_ollama, create_threat_model_prompt, json_to_markdown
from mitigations import get_mitigations, get_mitigations_azure, get_mitigations_google, get_mitigations_anthropic, get_mitigations_mistral, get_mitigations_ollama, create_mitigations_prompt
from attack_tree import get_attack_tree, get_attack_tree_azure, get_attack_tree_anthropic, get_attack_tree_mistral, get_attack_tree_ollama, create_attack_tree_prompt
from test_cases import get_test_cases, get_test_cases_azure, get_test_cases_google, get_test_cases_anthropic, get_test_cases_mistral, get_test_cases_ollama, create_test_cases_prompt
from dread import get_dread_assessment, get_dread_assessment_azure, get_dread_assessment_google, get_dread_assessment_anthropic, get_dread_assessment_mistral, get_dread_assessment_ollama, create_dread_assessment_prompt, dread_json_to_markdown
from utils.mermaid import mermaid

# Load environment variables
load_env()

def main():
    st.set_page_config(
        page_title="STRIDE GPT RAG",
        page_icon="🐠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("🐠 STRIDE GPT RAG")
    st.write("**Enhanced Threat Modeling with Retrieval-Augmented Generation**")
    
    # Sidebar for configuration
    st.sidebar.title("⚙️ Configuration")
    
    # Model selection
    model_provider = st.sidebar.selectbox(
        "Select Model Provider",
        ["OpenAI", "Azure OpenAI", "Google", "Anthropic", "Mistral", "Ollama"],
        help="Choose your AI model provider for threat analysis"
    )

    # API Configuration based on provider
    if model_provider == "OpenAI":
        api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        model_name = st.sidebar.selectbox("Model", ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"])
        if api_key:
            st.session_state['openai_api_key'] = api_key
            st.session_state['model_name'] = model_name
    
    elif model_provider == "Azure OpenAI":
        azure_api_endpoint = st.sidebar.text_input("Azure API Endpoint", help="Enter your Azure OpenAI endpoint")
        azure_api_key = st.sidebar.text_input("Azure API Key", type="password", help="Enter your Azure OpenAI API key")
        azure_api_version = st.sidebar.text_input("Azure API Version", value="2023-05-15", help="Enter your Azure OpenAI API version")
        azure_deployment_name = st.sidebar.text_input("Azure Deployment Name", help="Enter your Azure OpenAI deployment name")
        if azure_api_key and azure_api_endpoint and azure_deployment_name:
            st.session_state['azure_api_endpoint'] = azure_api_endpoint
            st.session_state['azure_api_key'] = azure_api_key
            st.session_state['azure_api_version'] = azure_api_version
            st.session_state['azure_deployment_name'] = azure_deployment_name
    
    elif model_provider == "Google":
        google_api_key = st.sidebar.text_input("Google API Key", type="password", help="Enter your Google API key")
        google_model = st.sidebar.selectbox("Model", ["gemini-pro", "gemini-pro-vision"])
        if google_api_key:
            st.session_state['google_api_key'] = google_api_key
            st.session_state['google_model'] = google_model
    
    elif model_provider == "Anthropic":
        anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password", help="Enter your Anthropic API key")
        anthropic_model = st.sidebar.selectbox("Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"])
        if anthropic_api_key:
            st.session_state['anthropic_api_key'] = anthropic_api_key
            st.session_state['anthropic_model'] = anthropic_model
    
    elif model_provider == "Mistral":
        mistral_api_key = st.sidebar.text_input("Mistral API Key", type="password", help="Enter your Mistral API key")
        mistral_model = st.sidebar.selectbox("Model", ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"])
        if mistral_api_key:
            st.session_state['mistral_api_key'] = mistral_api_key
            st.session_state['mistral_model'] = mistral_model
    
    elif model_provider == "Ollama":
        ollama_model = st.sidebar.text_input("Ollama Model", value="llama2", help="Enter the Ollama model name (e.g., llama2, codellama)")
        if ollama_model:
            st.session_state['ollama_model'] = ollama_model

    # GitHub API Key for RAG functionality
    st.sidebar.subheader("🔍 RAG Configuration")
    github_api_key = st.sidebar.text_input(
        "GitHub API Key (Optional)", 
        type="password", 
        help="Enter your GitHub API key to enable repository analysis for enhanced threat modeling"
    )
    if github_api_key:
        st.session_state['github_api_key'] = github_api_key

    # Application details
    st.sidebar.subheader("🏗️ Application Details")
    app_type = st.sidebar.selectbox(
        "Application Type",
        ["Web Application", "Mobile Application", "Desktop Application", "API", "Cloud Service", "IoT Device", "Other"],
        help="Select the type of application you're modeling"
    )

    authentication = st.sidebar.multiselect(
        "Authentication Methods",
        ["OAuth", "SAML", "API Keys", "JWT", "Basic Auth", "Multi-factor", "SSO", "None"],
        help="Select all authentication methods used by the application"
    )

    internet_facing = st.sidebar.radio(
        "Internet Facing",
        ["Yes", "No"],
        help="Is this application accessible from the internet?"
    )

    sensitive_data = st.sidebar.multiselect(
        "Sensitive Data",
        ["PII", "Financial", "Health Records", "Credentials", "API Keys", "None"],
        help="Select all types of sensitive data handled by the application"
    )

    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📝 Application Description & Repository Analysis")
        
        # RAG functionality explanation
        with st.expander("ℹ️ About RAG Support", expanded=False):
            st.markdown("""
            **STRIDE GPT RAG** enhances threat modeling through **Retrieval-Augmented Generation (RAG)**:
            
            🔍 **Repository Analysis**: Automatically analyze GitHub repositories to understand your codebase
            📊 **Context-Aware Analysis**: Extract README files, code structure, and dependencies
            🧠 **Enhanced AI Understanding**: Feed repository context to AI models for more accurate threat identification
            
            **How to use RAG:**
            1. Enter your GitHub API key in the sidebar
            2. Provide a GitHub repository URL below
            3. The system will automatically extract and analyze the repository
            4. This context enhances the threat modeling accuracy
            """)
        
        # Get application input (includes RAG functionality)
        app_input = get_input()
        
    with col2:
        if st.button("🔍 Generate Threat Model", use_container_width=True):
            if not app_input.strip():
                st.error("Please provide an application description or GitHub repository URL.")
                return
            
            # Create the threat model prompt
            prompt = create_threat_model_prompt(app_type, authentication, internet_facing, sensitive_data, app_input)
            
            with st.spinner("🔮 Analyzing threats..."):
                try:
                    if model_provider == "OpenAI" and 'openai_api_key' in st.session_state:
                        threat_model = get_threat_model(st.session_state['openai_api_key'], st.session_state['model_name'], prompt)
                    elif model_provider == "Azure OpenAI" and 'azure_api_key' in st.session_state:
                        threat_model = get_threat_model_azure(
                            st.session_state['azure_api_endpoint'],
                            st.session_state['azure_api_key'],
                            st.session_state['azure_api_version'],
                            st.session_state['azure_deployment_name'],
                            prompt
                        )
                    elif model_provider == "Google" and 'google_api_key' in st.session_state:
                        threat_model = get_threat_model_google(st.session_state['google_api_key'], st.session_state['google_model'], prompt)
                    elif model_provider == "Anthropic" and 'anthropic_api_key' in st.session_state:
                        threat_model = get_threat_model_anthropic(st.session_state['anthropic_api_key'], st.session_state['anthropic_model'], prompt)
                    elif model_provider == "Mistral" and 'mistral_api_key' in st.session_state:
                        threat_model = get_threat_model_mistral(st.session_state['mistral_api_key'], st.session_state['mistral_model'], prompt)
                    elif model_provider == "Ollama" and 'ollama_model' in st.session_state:
                        threat_model = get_threat_model_ollama(st.session_state['ollama_model'], prompt)
                    else:
                        st.error(f"Please configure {model_provider} API credentials in the sidebar.")
                        return
                    
                    if threat_model:
                        st.session_state['threat_model'] = threat_model
                        st.success("✅ Threat model generated successfully!")
                    else:
                        st.error("❌ Failed to generate threat model. Please check your API configuration.")
                        
                except Exception as e:
                    st.error(f"❌ Error generating threat model: {str(e)}")

    # Display threat model results
    if 'threat_model' in st.session_state and st.session_state['threat_model']:
        st.subheader("🛡️ Threat Model Results")
        
        threat_model = st.session_state['threat_model']
        improvement_suggestions = threat_model.get('improvement_suggestions', [])
        
        # Convert JSON to markdown and display
        markdown_output = json_to_markdown(threat_model, improvement_suggestions)
        st.markdown(markdown_output)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🛠️ Generate Mitigations"):
                # Implementation for mitigations
                st.info("Mitigation generation feature coming soon...")
        
        with col2:
            if st.button("🌳 Create Attack Tree"):
                # Implementation for attack tree
                st.info("Attack tree generation feature coming soon...")
        
        with col3:
            if st.button("🧪 Generate Test Cases"):
                # Implementation for test cases
                st.info("Test case generation feature coming soon...")
        
        with col4:
            if st.button("📊 DREAD Assessment"):
                # Implementation for DREAD assessment
                st.info("DREAD assessment feature coming soon...")

if __name__ == "__main__":
    main()
