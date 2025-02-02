import base64
import os
import re
import requests
import streamlit as st
import streamlit.components.v1 as components
from collections import defaultdict
from github import Github
from dotenv import load_dotenv
from threat_model import (
    create_threat_model_prompt,
    get_threat_model,
    get_threat_model_azure,
    get_threat_model_google,
    get_threat_model_mistral,
    get_threat_model_ollama,
    get_threat_model_anthropic
)
from attack_tree import (
    create_attack_tree_prompt,
    get_attack_tree,
    get_attack_tree_azure,
    get_attack_tree_mistral,
    get_attack_tree_ollama,
    get_attack_tree_anthropic
)
from mitigations import (
    create_mitigations_prompt,
    get_mitigations,
    get_mitigations_azure,
    get_mitigations_google,
    get_mitigations_mistral,
    get_mitigations_ollama,
    get_mitigations_anthropic
)
from test_cases import (
    create_test_cases_prompt,
    get_test_cases,
    get_test_cases_azure,
    get_test_cases_google,
    get_test_cases_mistral,
    get_test_cases_ollama,
    get_test_cases_anthropic
)
from dread import (
    create_dread_assessment_prompt,
    get_dread_assessment,
    get_dread_assessment_azure,
    get_dread_assessment_google,
    get_dread_assessment_mistral,
    get_dread_assessment_ollama,
    get_dread_assessment_anthropic
)


def get_input():
    github_url = st.text_input(
        label="Enter GitHub repository URL (optional)",
        placeholder="https://github.com/owner/repo",
        key="github_url",
        help="Enter the URL of the GitHub repository you want to analyze.",
    )

    if github_url and github_url != st.session_state.get('last_analyzed_url', ''):
        if 'github_api_key' not in st.session_state or not st.session_state['github_api_key']:
            st.warning("Please enter a GitHub API key to analyze the repository.")
        else:
            with st.spinner('Analyzing GitHub repository...'):
                system_description = analyze_github_repo(github_url)
                st.session_state['github_analysis'] = system_description
                st.session_state['last_analyzed_url'] = github_url
                st.session_state['app_input'] = system_description + "\n\n" + st.session_state.get('app_input', '')

    input_text = st.text_area(
        label="Describe the application to be modelled",
        value=st.session_state.get('app_input', ''),
        placeholder="Enter your application details...",
        height=300,
        key="app_desc",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )

    st.session_state['app_input'] = input_text

    return input_text


def analyze_github_repo(repo_url):
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1]

    g = Github(st.session_state.get('github_api_key', ''))
    repo = g.get_repo(f"{owner}/{repo_name}")
    default_branch = repo.default_branch
    tree = repo.get_git_tree(default_branch, recursive=True)

    file_summaries = defaultdict(list)
    total_chars = 0
    char_limit = 100000
    readme_content = ""

    for file in tree.tree:
        if file.path.lower() == 'readme.md':
            content = repo.get_contents(file.path, ref=default_branch)
            readme_content = base64.b64decode(content.content).decode()
        elif file.type == "blob" and file.path.endswith(('.py', '.js', '.ts', '.html', '.css', '.java', '.go', '.rb')):
            content = repo.get_contents(file.path, ref=default_branch)
            decoded_content = base64.b64decode(content.content).decode()
            summary = summarize_file(file.path, decoded_content)
            file_summaries[file.path.split('.')[-1]].append(summary)
            total_chars += len(summary)
            if total_chars > char_limit:
                break

    system_description = f"Repository: {repo_url}\n\n"
    if readme_content:
        system_description += "README.md Content:\n"
        if len(readme_content) > 5000:
            system_description += readme_content[:5000] + "...\n(README truncated due to length)\n\n"
        else:
            system_description += readme_content + "\n\n"

    for file_type, summaries in file_summaries.items():
        system_description += f"{file_type.upper()} Files:\n"
        for summary in summaries:
            system_description += summary + "\n"
        system_description += "\n"

    return system_description


def summarize_file(file_path, content):
    imports = re.findall(r'^import .*|^from .* import .*', content, re.MULTILINE)
    functions = re.findall(r'def .*\\(.*\\):', content)
    classes = re.findall(r'class .*:', content)

    summary = f"File: {file_path}\n"
    if imports:
        summary += "Imports:\n" + "\n".join(imports[:5]) + "\n"
    if functions:
        summary += "Functions:\n" + "\n".join(functions[:5]) + "\n"
    if classes:
        summary += "Classes:\n" + "\n".join(classes[:5]) + "\n"

    return summary


def mermaid(code: str, height: int = 500) -> None:
    components.html(
        f"""
        <pre class="mermaid" style="height: {height}px;">
            {code}
        </pre>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,
    )


def load_env_variables():
    if os.path.exists('.env'):
        load_dotenv('.env')

    github_api_key = os.getenv('GITHUB_API_KEY')
    if github_api_key:
        st.session_state['github_api_key'] = github_api_key

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        st.session_state['openai_api_key'] = openai_api_key

    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_api_key:
        st.session_state['anthropic_api_key'] = anthropic_api_key

    azure_api_key = os.getenv('AZURE_API_KEY')
    if azure_api_key:
        st.session_state['azure_api_key'] = azure_api_key

    azure_api_endpoint = os.getenv('AZURE_API_ENDPOINT')
    if azure_api_endpoint:
        st.session_state['azure_api_endpoint'] = azure_api_endpoint

    azure_deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME')
    if azure_deployment_name:
        st.session_state['azure_deployment_name'] = azure_deployment_name

    google_api_key = os.getenv('GOOGLE_API_KEY')
    if google_api_key:
        st.session_state['google_api_key'] = google_api_key

    mistral_api_key = os.getenv('MISTRAL_API_KEY')
    if mistral_api_key:
        st.session_state['mistral_api_key'] = mistral_api_key


load_env_variables()

st.set_page_config(
    page_title="STRIDE GPT",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        STRIDE is a threat modeling methodology that helps to identify and categorise potential security risks in software applications. It stands for **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure, **D**enial of service, and **E**levation of privilege.
        """
    )
    st.markdown(
        """
        ### **How does STRIDE GPT work?**
        When you enter an application description and other relevant details, the tool will use a GPT model to generate a threat model for your application. The model uses the application description to identify potential threats and suggest mitigations.
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
        No, the threat models are not 100% accurate. STRIDE GPT uses GPT Large Language Models (LLMs) to generate its output. The GPT models are powerful, but they sometimes make mistakes and are prone to hallucination.
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
        A threat model helps identify and evaluate potential security threats to applications / systems. It provides a systematic approach to 
        understanding possible vulnerabilities and attack vectors. Use this tab to generate a threat model using the STRIDE methodology.
        """
    )
    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    if 'app_input' not
