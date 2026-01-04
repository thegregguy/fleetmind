# Contributing to FleetMind

Thank you for your interest in contributing to FleetMind! This document provides guidelines and information for contributors.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Verify the bug with the latest version
3. Try to reproduce with demo mode first

Include in your bug report:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Relevant logs or screenshots

### Suggesting Features

When suggesting a feature:
1. Check if it's already been suggested
2. Clearly describe the problem it solves
3. Explain the proposed solution
4. Consider implementation complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the coding standards
4. **Test your changes** thoroughly
5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: description of what you did"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** with a clear description

## Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/thegregguy/fleetmind.git
cd fleetmind
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure for Development
```bash
cp .env.example .env
# Set DEMO_MODE=true for development
echo "DEMO_MODE=true" > .env
```

### 4. Run Tests
```bash
python test_fleetmind.py
```

### 5. Run the Application
```bash
streamlit run app.py
```

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes

### Documentation
- Update README.md for user-facing changes
- Add docstrings for all public functions
- Include type hints where appropriate
- Update CHANGELOG.md (when we add one)

### Imports
Order imports as:
1. Standard library
2. Third-party packages
3. Local modules

Example:
```python
import os
from typing import Dict, List

import streamlit as st
import pandas as pd

from gps_utils import GPSUtils
from sheets_manager import GoogleSheetsManager
```

### Function Documentation
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

## Project Structure

```
fleetmind/
├── app.py                  # Main Streamlit application
├── gps_utils.py           # GPS utilities and distance calculation
├── sheets_manager.py      # Google Sheets API integration
├── ping_manager.py        # Trip logging logic
├── smart_gas_manager.py   # Variance reconciliation logic
├── demo_mode.py           # In-memory storage for testing
├── test_fleetmind.py      # Test suite
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore patterns
├── README.md             # Main documentation
├── QUICKSTART.md         # Quick start guide
├── SETUP_GUIDE.md        # Google Sheets setup
└── DATA_FLOW_EXAMPLE.md  # Example data flow
```

## Testing

### Running Tests
```bash
python test_fleetmind.py
```

### Writing Tests
- Add tests for all new features
- Test edge cases and error conditions
- Use demo mode for unit tests
- Test with actual Google Sheets for integration tests

### Test Coverage
Aim for:
- Core logic: 100% coverage
- UI components: Basic smoke tests
- Integration: Key workflows

## Areas for Contribution

### High Priority
- [ ] Mobile GPS integration
- [ ] Bluetooth hardware integration for hands-free Ping
- [ ] Export functionality (PDF, Excel)
- [ ] Multi-vehicle support improvements
- [ ] Route visualization on maps

### Medium Priority
- [ ] Tax deduction calculator
- [ ] Expense categories and tags
- [ ] Weekly/monthly reports
- [ ] Backup and restore functionality
- [ ] Dark mode UI

### Low Priority (Nice to Have)
- [ ] Multiple driver support
- [ ] Integration with accounting software
- [ ] Voice command support
- [ ] Automatic trip detection
- [ ] Weather data correlation

### Documentation
- [ ] Video tutorials
- [ ] More usage examples
- [ ] Internationalization (i18n)
- [ ] API documentation
- [ ] Deployment guides (AWS, GCP, Heroku)

## Performance Guidelines

### Google Sheets API
- Batch updates when possible
- Cache data locally when appropriate
- Respect API rate limits
- Use exponential backoff for retries

### Streamlit UI
- Use `@st.cache_data` for expensive computations
- Minimize unnecessary reruns
- Keep UI responsive
- Test with large datasets

## Security Guidelines

### Credentials
- Never commit credentials to git
- Use environment variables for secrets
- Document credential setup clearly
- Implement proper error handling for missing credentials

### Data Privacy
- Don't log sensitive information
- Implement proper access controls
- Consider GDPR compliance for EU users
- Add data export functionality

### Dependencies
- Keep dependencies up to date
- Review security advisories
- Use virtual environments
- Pin dependency versions in requirements.txt

## Release Process

1. **Update Version**: Update version number in appropriate files
2. **Update CHANGELOG**: Document all changes
3. **Test Thoroughly**: Run full test suite
4. **Tag Release**: Create git tag with version number
5. **Deploy**: Deploy to production (if applicable)
6. **Announce**: Announce release to users

## Getting Help

- **Documentation**: Start with README.md and other docs
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive issues

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (when we add one)
- Credited in release notes
- Acknowledged in the README

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Questions?

Feel free to open an issue with the "question" label if you need clarification on anything!

---

**Thank you for making FleetMind better! 🚗✨**
