# Contributing to Finsight

Thank you for your interest in contributing to Finsight! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Finsight.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Install development dependencies: `pip install -e .[dev]`

## Development Workflow

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for your changes
4. Run tests: `pytest`
5. Ensure code coverage: `pytest --cov=finsight`
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for at least 80% code coverage
- Use mocks for external API calls

## Adding New Connectors

To add a new financial institution connector:

1. Create a new file in `finsight/connectors/` (e.g., `new_connector.py`)
2. Extend the `BaseConnector` class
3. Implement all abstract methods
4. Add the connector to `ConnectorFactory` in `factory.py`
5. Write comprehensive unit tests in `tests/connectors/`
6. Update documentation with usage examples

Example structure:

```python
from finsight.connectors.base import BaseConnector, AuthType, ConnectorResponse

class NewConnector(BaseConnector):
    @property
    def provider_name(self) -> str:
        return "new_provider"
    
    @property
    def auth_type(self) -> AuthType:
        return AuthType.API_KEY
    
    def _validate_credentials(self) -> None:
        # Validate required credentials
        pass
    
    def authenticate(self) -> ConnectorResponse:
        # Implement authentication
        pass
    
    # Implement other required methods...
```

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure CI checks pass
- Be responsive to review feedback

## Code Review Process

1. At least one maintainer review is required
2. All CI checks must pass
3. Code coverage should not decrease
4. Documentation must be updated if needed

## Reporting Issues

- Use the GitHub issue tracker
- Provide clear reproduction steps
- Include error messages and logs
- Specify your environment (OS, Python version, etc.)

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
