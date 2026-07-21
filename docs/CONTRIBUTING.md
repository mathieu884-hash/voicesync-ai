# Contributing to VoiceSync AI

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the VoiceSync AI project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community. Please read and adhere to our Code of Conduct.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/voicesync-ai.git
   cd voicesync-ai
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Set up your environment**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

4. **Start development servers**
   ```bash
   docker-compose up -d
   ```

## Development Workflow

### Commit Messages

We follow Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Changes to build process or dependencies

**Examples:**
```
feat(dubbing): add voice cloning capability
fix(api): resolve job status query timeout
docs: update API documentation
```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use Black for formatting

```bash
cd backend
black app/
isort app/
```

**TypeScript/React:**
- Use ESLint and Prettier
- Type all props and state
- Use functional components with hooks

```bash
cd frontend
npm run lint:fix
npm run format
```

### Testing

**Backend:**
```bash
cd backend
pytest  # Run all tests
pytest tests/test_dubbing.py  # Run specific test file
pytest -v --cov=app  # Run with coverage
```

**Frontend:**
```bash
cd frontend
npm test  # Run tests
npm test -- --coverage  # With coverage report
```

### Before Submitting a PR

1. **Update documentation** if you're adding new features
2. **Add tests** for your changes
3. **Run linting and formatting**
   ```bash
   make lint
   make format
   ```
4. **Update CHANGELOG.md** with your changes
5. **Ensure all tests pass**
   ```bash
   make test
   ```

## Pull Request Process

1. **Create a descriptive PR title** following the Conventional Commits format
2. **Reference related issues** using `#issue_number`
3. **Provide a clear description** of changes
4. **Ensure CI/CD checks pass**
5. **Request reviews** from maintainers
6. **Address feedback** and make necessary changes
7. **Squash commits** if requested

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123
Related to #456

## Testing
Describe the tests you ran and how to reproduce

## Screenshots (if applicable)

## Checklist
- [ ] I have tested my changes locally
- [ ] I have updated the documentation
- [ ] I have added tests for my changes
- [ ] All tests pass
- [ ] My code follows the style guidelines
```

## Project Structure

```
voicesync-ai/
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── services/             # Microservices
├── ml_models/            # ML model configs
├── docs/                 # Documentation
├── .github/workflows/    # CI/CD pipelines
└── docker-compose.yml    # Local development setup
```

## Areas to Contribute

### High Priority
- 🎬 Video processing optimization
- 🗣️ New language support
- 🎙️ Voice actor integration
- 📱 Mobile app support

### Medium Priority
- 📊 Analytics and reporting
- 🔐 Enhanced security features
- 🌍 Internationalization (i18n)
- ⚡ Performance optimization

### Documentation
- API documentation
- User guides
- Architecture documentation
- Setup guides

## Getting Help

- 📖 Read the [documentation](docs/)
- 💬 Join our [Discord community](https://discord.gg/voicesync)
- 📝 Open an [issue](https://github.com/mathieu884-hash/voicesync-ai/issues)
- 📧 Email: support@voicesync-ai.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

We recognize all contributors! Your name will be added to:
- README.md
- CONTRIBUTORS.md
- GitHub contributors page

---

Thank you for contributing to VoiceSync AI! 🙌
