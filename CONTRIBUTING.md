# Contributing Guide & Code of Conduct

Welcome, and thanks for your interest in contributing to this project! 🎉 This document outlines how to contribute effectively and our community expectations.

## 🛠️ Getting Started

1. **Fork** the repository and **clone** your fork:
   ```
   git clone https://github.com/Asiandayboy/domain.git
   cd your-flask-app
   ```

2. **Set up a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the app locally**:
   ```
   python src/app.py
   ```



## ✏️ Making Contributions

1. **Create a new branch**:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, write clear commit messages, and ensure code is formatted and linted:
   ```
   flake8 .
   ```

3. **Push your changes**:
   ```
   git push origin feature/your-feature-name
   ```

4. Open a **Pull Request** and describe your changes clearly.

## 📚 Code Style

- Follow [PEP 8](https://pep8.org)
- Use docstrings for all functions, especially API routes
- Keep functions small and focused
- Write comments where helpful, but favor readable code
- Prefer clarity over cleverness

### Flasgger-Compatible API Docstring Example:
```python
"""
Get item by ID.
---
parameters:
  - name: id
    in: path
    type: integer
    required: true
    description: ID of the item
responses:
  200:
    description: A JSON object containing the item
"""
```


## 🤝 Code of Conduct

We are committed to creating a safe and inclusive environment for everyone.

### Expected Behavior:
- Be respectful, inclusive, and considerate
- Use welcoming and inclusive language
- Be constructive in feedback and collaboration
- Respect different viewpoints and experiences

### Unacceptable Behavior:
- Harassment, threats, or discrimination
- Personal attacks, trolling, or insulting remarks
- Use of sexualized language or imagery
- Any behavior that makes others feel unsafe or unwelcome

### Reporting:
If you experience or witness unacceptable behavior, please contact a maintainer directly or open a confidential issue. Reports will be handled seriously and privately.

By participating in this project, you agree to follow this Code of Conduct.

---

Thank you for contributing and helping us improve! 💛

