---
title: STRIDE GPT RAG
emoji: 🐠
colorFrom: purple
colorTo: yellow
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: false
short_description: Eenhancement with Retrieval-Augmented Generation
license: apache-2.0
---

# STRIDE GPT RAG 🐠

## Overview

**STRIDE GPT RAG** is an advanced threat modeling tool that leverages Retrieval-Augmented Generation (RAG) to provide accurate and context-aware threat analyses. By integrating the STRIDE framework with cutting-edge AI, it assists cybersecurity professionals in identifying and mitigating potential threats effectively.

## Features

- **STRIDE Framework Integration:** Utilizes the STRIDE methodology to systematically identify threats.
- **Retrieval-Augmented Generation (RAG):** Enhances threat analysis by retrieving and analyzing GitHub repository content for context-aware threat modeling.
- **Repository Analysis:** Automatically extracts README content, code structure, dependencies, and architectural information from GitHub repositories.
- **Context-Aware AI:** Feeds repository context to AI models for more accurate and specific threat identification.
- **Interactive Interface:** Offers a user-friendly Streamlit interface for seamless interaction.
- **Multiple AI Providers:** Supports OpenAI, Azure OpenAI, Google Gemini, Anthropic Claude, Mistral, and Ollama.
- **Comprehensive Output:** Generates threat models, mitigations, attack trees, test cases, and DREAD assessments.

## Installation

To run the application locally:

1. **Clone the Repository:**

   ```bash
   git clone https://huggingface.co/spaces/Canstralian/STRIDE-GPT-RAG
   cd STRIDE-GPT-RAG
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

   Access the app at `http://localhost:8501`.

## Usage

### Basic Threat Modeling

1. **Configure AI Provider:** Select your preferred AI model (OpenAI, Google, Anthropic, etc.) and enter API credentials in the sidebar.
2. **Input Application Details:** Provide application type, authentication methods, and other relevant details in the sidebar.
3. **Describe Your Application:** Enter a description of the application in the main text area.
4. **Generate Analysis:** Click "Generate Threat Model" to create a comprehensive STRIDE-based threat analysis.

### RAG-Enhanced Analysis

For more accurate, context-aware threat modeling:

1. **GitHub Integration:** Enter your GitHub API key in the RAG Configuration section.
2. **Repository Analysis:** Provide a GitHub repository URL in the "Enter GitHub repository URL" field.
3. **Automatic Context Extraction:** The system will automatically:
   - Extract README documentation
   - Analyze code structure and dependencies
   - Identify technology stack and architecture
   - Create contextual summaries for enhanced AI analysis
4. **Enhanced Threat Modeling:** The AI will generate threats specific to your actual codebase and architecture.

### Advanced Features

- **Mitigations:** Generate specific mitigation strategies for identified threats
- **Attack Trees:** Create visual attack scenarios using Mermaid diagrams
- **Test Cases:** Generate Gherkin-formatted security test cases
- **DREAD Assessment:** Perform quantitative risk assessment using the DREAD methodology

For detailed information about RAG implementation, see [RAG_IMPLEMENTATION.md](RAG_IMPLEMENTATION.md).

## Requirements

- **Python Version:** 3.8 or higher.
- **Dependencies:** Listed in `requirements.txt`.
- **AI Provider API Key:** At least one API key from supported providers (OpenAI, Google, Anthropic, etc.).
- **GitHub API Key (Optional):** For RAG-enhanced repository analysis - provides more accurate threat modeling.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Streamlit:** For providing an intuitive framework for building interactive applications.
- **Hugging Face Spaces:** For hosting and deploying machine learning applications seamlessly.
- **OpenAI/Anthropic:** For their advanced language models that power the threat analysis.

## Contact

For questions or support, please contact [12lb6o3m7@mozmail.com](mailto:12lb6o3m7@mozmail.com).

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces-overview)
- [STRIDE Threat Modeling Framework](https://www.microsoft.com/en-us/security/blog/2020/06/25/introducing-stride-a-threat-modeling-framework/)
