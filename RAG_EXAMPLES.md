# RAG Functionality Examples

This document provides examples of how RAG (Retrieval-Augmented Generation) enhances threat modeling in STRIDE-GPT-RAG.

## Example 1: Web Application Analysis

### Input: GitHub Repository URL
```
Repository: https://github.com/example/flask-blog-app
```

### RAG Extraction Output
```
Repository: https://github.com/example/flask-blog-app

README.md Content:
# Flask Blog Application
A simple blog application built with Flask and SQLAlchemy.

## Features
- User authentication with Flask-Login
- Blog post creation and editing
- SQLite database with SQLAlchemy ORM
- File upload for images
- Admin panel for user management

## Dependencies
- Flask 2.0
- SQLAlchemy 1.4
- Flask-Login 0.6
- Werkzeug 2.0

PY Files:
File: app.py
Imports:
from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_required, current_user
from werkzeug.utils import secure_filename
import sqlite3

Functions:
def create_app():
def upload_file():
def admin_panel():
def delete_user(user_id):

File: models.py
Classes:
class User(UserMixin, db.Model):
class BlogPost(db.Model):
class Comment(db.Model):
```

### Enhanced Threat Analysis with RAG

**Without RAG (Generic):**
- SQL Injection in web forms
- Cross-site scripting (XSS)
- Authentication bypass

**With RAG (Context-Aware):**
- **File Upload Vulnerability**: The `upload_file()` function using `secure_filename()` may still be vulnerable to path traversal attacks if not properly configured
- **SQLAlchemy ORM Injection**: Direct SQLAlchemy queries in admin functions could be vulnerable to ORM injection
- **Flask-Login Session Hijacking**: Session management weaknesses specific to Flask-Login implementation
- **SQLite Concurrency Issues**: SQLite database may have race conditions in multi-user scenarios
- **Admin Panel Privilege Escalation**: The `delete_user()` function in admin panel lacks proper authorization checks
- **Werkzeug Debug Mode**: If debug mode is enabled in production, could expose sensitive information

## Example 2: API Service Analysis

### Input: GitHub Repository URL
```
Repository: https://github.com/example/fastapi-microservice
```

### RAG Extraction Output
```
Repository: https://github.com/example/fastapi-microservice

README.md Content:
# FastAPI Microservice
RESTful API service with JWT authentication and Redis caching.

## Architecture
- FastAPI framework
- PostgreSQL database
- Redis for caching and session storage
- JWT tokens for authentication
- Docker containerization

PY Files:
File: main.py
Imports:
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import redis
import asyncpg

Functions:
def verify_jwt_token(credentials: HTTPAuthorizationCredentials):
def get_user_from_cache(user_id: str):
async def database_query(query: str, params: list):

File: auth.py
Functions:
def create_access_token(data: dict):
def verify_password(plain_password: str, hashed_password: str):
```

### Enhanced Threat Analysis with RAG

**Without RAG (Generic):**
- API authentication bypass
- Injection attacks
- Rate limiting issues

**With RAG (Context-Aware):**
- **JWT Secret Management**: Hard-coded JWT secrets or weak key generation in `create_access_token()`
- **Redis Cache Poisoning**: Unvalidated data stored in Redis cache through `get_user_from_cache()`
- **AsyncPG SQL Injection**: The `database_query()` function with string parameters vulnerable to SQL injection
- **FastAPI Dependency Injection**: Improper dependency injection in `verify_jwt_token()` could bypass authentication
- **Docker Container Escape**: Misconfigured Docker containers running with elevated privileges
- **PostgreSQL Connection String Exposure**: Database credentials potentially exposed in environment variables

## Example 3: Comparison Output

### Traditional Threat Model (No RAG)
```json
{
  "threat_model": [
    {
      "Threat Type": "Spoofing",
      "Scenario": "An attacker could impersonate a legitimate user",
      "Potential Impact": "Unauthorized access to user accounts"
    }
  ]
}
```

### RAG-Enhanced Threat Model
```json
{
  "threat_model": [
    {
      "Threat Type": "Spoofing", 
      "Scenario": "An attacker could exploit the Flask-Login session management by stealing session cookies from the SQLite database identified in the repository analysis, specifically targeting the User model's session storage",
      "Potential Impact": "Complete user account takeover with persistent access through compromised session data stored in the SQLite database"
    }
  ],
  "improvement_suggestions": [
    "Implement secure session storage with Redis instead of SQLite for better session management",
    "Add session timeout and rotation mechanisms in the Flask-Login configuration",
    "Use HTTPS-only and SameSite cookie attributes for session cookies"
  ]
}
```

## Key Benefits Demonstrated

1. **Technology-Specific Threats**: Identifies threats specific to Flask, FastAPI, SQLAlchemy, etc.
2. **Architecture-Aware**: Understands the actual system architecture from README and code
3. **Code-Based Evidence**: Points to specific functions and files where vulnerabilities exist
4. **Contextual Mitigations**: Provides recommendations specific to the technology stack
5. **Reduced False Positives**: Avoids generic threats that don't apply to the specific implementation