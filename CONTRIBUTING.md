# Contributing to KashaLang

Thank you for your interest in contributing to KashaLang! 🌍 We welcome contributions from developers of all skill levels and backgrounds.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Areas for Contribution](#areas-for-contribution)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to:

- **Respect**: Treat everyone with respect and dignity
- **Inclusivity**: Welcome contributors from all backgrounds
- **Collaboration**: Work together to build something amazing
- **Learning**: Help others learn and grow

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Set up** your development environment
4. **Create** a branch for your changes

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/kashalang.git
cd kashalang
git checkout -b feature/your-feature-name
```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please:

1. Check if the bug has already been reported
2. Try to reproduce the bug with the latest version
3. Collect information about the bug (OS, Python version, error messages)

When filing a bug report, include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Code example that triggers the bug
- Error messages and stack traces

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Provide a clear use case
3. Explain why the feature would be useful
4. Include example code if applicable

### Contributing Code

1. **Find an issue** to work on or create a new one
2. **Comment** on the issue to let others know you're working on it
3. **Write** your code following our coding standards
4. **Test** your changes thoroughly
5. **Document** your changes
6. **Submit** a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kashalang.git
cd kashalang

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests to verify setup
pytest tests/
```

## Coding Standards

### Python Code

We follow PEP 8 with some modifications:

- **Line length**: 100 characters max
- **Indentation**: 4 spaces
- **Imports**: Group stdlib, third-party, and local imports
- **Docstrings**: Use Google-style docstrings

```python
def example_function(param1: int, param2: str) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    return True
```

### KashaLang Code

For examples and standard library:

- Use African-inspired keywords where appropriate
- Include comments in both English and African languages
- Keep functions focused and small
- Use descriptive variable names

```kasha
# Calculate factorial
# Kuba factorial
fata factorial(n)
    niba n <= 1
        subiza 1
    subiza n * factorial(n - 1)
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for high test coverage

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=core --cov=cli

# Run specific test file
pytest tests/test_lexer.py
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for your changes
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Submit pull request** with clear description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add Swahili language support

- Added Swahili keywords (sema, weka, kama)
- Updated lexer to recognize Swahili tokens
- Added tests for Swahili syntax

Closes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

## Areas for Contribution

### 🌍 Language & Culture

- Add support for more African languages
- Create culturally relevant examples
- Translate documentation

### 💻 Core Development

- Improve interpreter performance
- Add new language features
- Fix bugs and edge cases

### 📚 Documentation

- Write tutorials and guides
- Improve API documentation
- Create video content

### 📦 Packages

- Build useful libraries
- Create web frameworks
- Add database connectors

### 🧪 Testing

- Write test cases
- Improve test coverage
- Add integration tests

### 🎨 Design

- Create logos and branding
- Design website
- Make promotional materials

## Recognition

Contributors will be:
- Listed in our CONTRIBUTORS.md file
- Mentioned in release notes
- Invited to our Discord community

## Questions?

- 💬 Join our [Discord](https://discord.gg/kashalang)
- 📧 Email us at [hello@kashalang.dev](mailto:hello@kashalang.dev)
- 🐦 Tweet us [@kashalang](https://twitter.com/kashalang)

---

Thank you for contributing to KashaLang! Together, we're building the future of African tech. 🌍
