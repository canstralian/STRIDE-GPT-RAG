import base64
import re
from collections import defaultdict
from github import Github
import streamlit as st

def analyze_github_repo(repo_url):
    try:
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
    except Exception as e:
        st.error(f"Error analyzing GitHub repository: {e}")
        return ""

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
