# RAG Implementation in STRIDE-GPT-RAG

## Overview

**STRIDE-GPT-RAG** implements **Retrieval-Augmented Generation (RAG)** to enhance threat modeling by automatically analyzing GitHub repositories and incorporating code context into threat assessments. This provides more accurate, contextual threat identification compared to generic threat modeling tools.

## How RAG Works in STRIDE-GPT-RAG

### 1. Repository Analysis (`utils/repo_analysis.py`)

The RAG implementation automatically extracts and analyzes repository content:

- **README Analysis**: Extracts project documentation to understand purpose and architecture
- **Code Structure**: Analyzes Python, JavaScript, TypeScript, HTML, CSS, Java, Go, and Ruby files
- **Dependency Extraction**: Identifies imports, functions, and classes
- **Content Summarization**: Creates structured summaries while respecting API limits (100k characters)

### 2. Context Integration

The extracted repository context is seamlessly integrated into threat modeling prompts:

```python
def create_threat_model_prompt(app_type, authentication, internet_facing, sensitive_data, app_input):
    prompt = f"""
    Act as a cyber security expert with more than 20 years experience...
    
    Pay special attention to the README content as it often provides valuable context 
    about the project's purpose, architecture, and potential security considerations.
    
    CODE SUMMARY, README CONTENT, AND APPLICATION DESCRIPTION:
    {app_input}  # This includes the RAG-extracted repository context
    """
```

### 3. Enhanced AI Analysis

The AI models receive:
- **Project Documentation**: README content for architectural understanding
- **Code Context**: File structures, imports, and function signatures
- **Technology Stack**: Inferred from code analysis
- **Custom Descriptions**: User-provided application details

## Usage Examples

### Basic RAG Usage

1. **Configure GitHub Access**:
   ```
   # In Streamlit sidebar
   GitHub API Key: [your-github-token]
   ```

2. **Analyze Repository**:
   ```
   Repository URL: https://github.com/owner/repo
   ```

3. **Automatic Analysis**: The system will:
   - Fetch repository structure
   - Extract README content
   - Analyze code files
   - Create contextual summary

### Integration with Threat Models

The RAG-enhanced context improves threat identification:

**Without RAG**: Generic threats based on application type
**With RAG**: Specific threats based on actual code structure, dependencies, and architecture

## Technical Implementation

### Key Files

- **`utils/repo_analysis.py`**: Core RAG functionality
- **`utils/input.py`**: UI integration for repository input
- **`threat_model.py`**: Enhanced prompt creation with RAG context

### RAG Workflow

1. **Repository Fetching**: 
   ```python
   g = Github(st.session_state.get('github_api_key', ''))
   repo = g.get_repo(f"{owner}/{repo_name}")
   tree = repo.get_git_tree(default_branch, recursive=True)
   ```

2. **Content Extraction**:
   ```python
   for file in tree.tree:
       if file.path.lower() == 'readme.md':
           content = repo.get_contents(file.path, ref=default_branch)
           readme_content = base64.b64decode(content.content).decode()
   ```

3. **Context Building**:
   ```python
   system_description = f"Repository: {repo_url}\n\n"
   if readme_content:
       system_description += "README.md Content:\n"
       system_description += readme_content + "\n\n"
   ```

## Benefits of RAG in Threat Modeling

### 1. **Context-Aware Threats**
- Identifies threats specific to actual code structure
- Recognizes technology-specific vulnerabilities
- Understands application architecture from documentation

### 2. **Improved Accuracy**
- Reduces false positives through better context understanding
- Identifies missed threats through code analysis
- Provides more relevant mitigation strategies

### 3. **Automated Analysis**
- No manual code review required
- Scales to large repositories
- Consistent analysis across projects

## Configuration Options

### GitHub API Requirements

- **Personal Access Token**: Required for private repositories
- **Rate Limits**: Handles GitHub API rate limiting
- **Repository Access**: Works with public and accessible private repositories

### Analysis Limits

- **Character Limit**: 100,000 characters to stay within AI model limits
- **File Types**: Focuses on common programming languages
- **Priority Order**: README first, then code files by type

## Example Output

### Without RAG
```
Threat Type: Information Disclosure
Scenario: Sensitive data exposure through logs
```

### With RAG (analyzing a Flask API)
```
Threat Type: Information Disclosure  
Scenario: Database credentials exposed in config.py file identified in repository analysis
Potential Impact: Complete database compromise through hardcoded credentials in source code
```

## Extending RAG Functionality

### Adding New File Types

Modify the file filter in `repo_analysis.py`:
```python
elif file.type == "blob" and file.path.endswith(('.py', '.js', '.ts', '.html', '.css', '.java', '.go', '.rb', '.your_extension')):
```

### Custom Analysis Rules

Extend the `summarize_file` function:
```python
def summarize_file(file_path, content):
    # Add custom parsing for specific file types
    if file_path.endswith('.dockerfile'):
        docker_commands = re.findall(r'^(FROM|RUN|EXPOSE|ENV).*', content, re.MULTILINE)
        # Process Docker-specific security considerations
```

## Integration with Other Features

The RAG system enhances all STRIDE-GPT-RAG features:

- **Threat Modeling**: More accurate threat identification
- **Mitigation Strategies**: Context-aware security recommendations  
- **Attack Trees**: Repository-specific attack scenarios
- **Test Cases**: Code-aware security test generation
- **DREAD Assessment**: Accurate risk scoring based on actual implementation

## Troubleshooting

### Common Issues

1. **GitHub API Rate Limits**: Use authenticated requests with higher limits
2. **Large Repositories**: System automatically truncates at 100k characters
3. **Private Repository Access**: Ensure API token has appropriate permissions

### Debug Information

The system provides feedback on:
- Repository analysis progress
- Content extraction status
- Integration with threat modeling prompts