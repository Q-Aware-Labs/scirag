# Contributing to SciRAG

First off, thank you for considering contributing to SciRAG! 🎉

It's people like you that make SciRAG such a great tool for the research community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Areas for Contribution](#areas-for-contribution)

---

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this commitment.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** (if applicable)
- **Environment details** (OS, browser, versions)
- **Error messages** or logs

**Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 96]
- Version: [e.g., 0.1.0]
```

### ✨ Suggesting Features

Feature requests are welcome! Please:
- **Use a clear, descriptive title**
- **Provide detailed description** of the proposed feature
- **Explain why this would be useful** to most users
- **List any alternatives** you've considered
- **Include mockups** if applicable

### 🔧 Pull Requests

We actively welcome your pull requests!

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the style guidelines
6. Issue that pull request!

---

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- Anthropic API key

### Setup Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/scirag.git
   cd scirag
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY to .env
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env.local
   # Update VITE_API_BASE_URL if needed
   ```

4. **Run Tests**
   ```bash
   # Backend tests
   cd backend
   python -m pytest
   
   # Frontend tests (if available)
   cd ../frontend
   npm test
   ```

5. **Start Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] Self-review of your own code
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings generated
- [ ] Tests added for new features
- [ ] All tests pass locally
- [ ] Commits are well-formed and descriptive

### Creating the PR

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

4. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Submit!

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] All tests pass
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be recognized in release notes!

---

## Style Guidelines

### Python (Backend)

**Follow PEP 8 with these specifics:**

```python
# Imports: standard, third-party, local
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
import anthropic

from .services import arxiv_service

# Line length: 100 characters max
# Indentation: 4 spaces
# Strings: Double quotes for regular, single for dict keys

def search_papers(
    query: str,
    max_results: int = 5
) -> List[dict]:
    """
    Search arXiv for papers.
    
    Args:
        query: Search query string
        max_results: Maximum papers to return
        
    Returns:
        List of paper metadata dictionaries
    """
    # Implementation
    pass
```

**Tools:**
- Use `black` for formatting: `black backend/`
- Use `flake8` for linting: `flake8 backend/`
- Use `mypy` for type checking: `mypy backend/`

### TypeScript (Frontend)

**Follow Airbnb style guide with these specifics:**

```typescript
// Imports: React, third-party, local
import React, { useState } from 'react';
import axios from 'axios';

import { api } from '@/api/client';
import { Button } from '@/components/ui';

// Interfaces over types when possible
interface SearchProps {
  onSearch: (query: string) => void;
  maxResults?: number;
}

// Functional components with TypeScript
export const SearchBar: React.FC<SearchProps> = ({ 
  onSearch, 
  maxResults = 5 
}) => {
  const [query, setQuery] = useState('');
  
  // Handlers use arrow functions
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Implementation */}
    </form>
  );
};
```

**Tools:**
- Use `prettier` for formatting: `npm run format`
- Use `eslint` for linting: `npm run lint`
- Use `tsc` for type checking: `npm run typecheck`

### CSS/Tailwind

```tsx
// Use Tailwind utility classes
<div className="card-brutal bg-white p-4 shadow-brutal">
  <h2 className="font-display text-2xl font-black">
    Title
  </h2>
</div>

// Custom CSS only when necessary
// Keep in sync with neobrutalist design
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Maintenance tasks

### Examples

```bash
feat(search): add date range filter to arXiv search

Added date range selector to search interface allowing users
to filter papers by publication date.

Closes #123
```

```bash
fix(pdf): resolve text extraction error for certain PDFs

Fixed issue where PDFs with unusual encoding would fail to
extract. Added fallback encoding detection.

Fixes #456
```

```bash
docs(readme): update installation instructions

Updated Python version requirement to 3.10+ and clarified
virtual environment setup steps.
```

---

## Areas for Contribution

We'd especially love help with:

### 🐛 Bug Fixes
- Check [Issues](https://github.com/antonyga/scirag/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
- Fix known bugs
- Improve error handling

### ✨ Features
See our [Roadmap](README.md#-roadmap) for planned features:
- User authentication
- Conversation history
- Export functionality
- Multi-source support
- Dark mode

### 📖 Documentation
- Improve setup guides
- Add usage examples
- Create video tutorials
- Translate to other languages
- Fix typos and clarify explanations

### 🎨 Design
- UI/UX improvements
- Accessibility enhancements
- Mobile responsiveness
- Animation and transitions
- Design system refinements

### 🧪 Testing
- Write unit tests
- Add integration tests
- Improve test coverage
- Performance testing
- Cross-browser testing

### 🌍 Localization
- Translate UI to other languages
- Add i18n support
- RTL language support

### 🔧 Infrastructure
- Improve CI/CD
- Docker optimization
- Monitoring and logging
- Performance optimization
- Security enhancements

---

## Questions?

Feel free to:
- Open a [Discussion](https://github.com/antonyga/scirag/discussions)
- Ask in existing Issues
- Reach out directly: antonio@example.com

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the project

Thank you for making SciRAG better! 🙏

---

**Remember:** No contribution is too small! Even fixing a typo helps. ❤️