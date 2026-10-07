# Contributing to Video Understanding & Temporal Reasoning

Thank you for your interest in contributing! We welcome bug reports, feature suggestions, and pull requests.

## Development Workflow

1. **Fork the Repository** and clone your fork locally:
   ```bash
   git clone https://github.com/your-username/video-temporal-reasoning.git
   cd video-temporal-reasoning
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Run Tests**:
   Ensure all automated tests pass:
   ```bash
   python -m unittest tests/test_temporal_reasoning.py
   ```

5. **Commit & Push**:
   ```bash
   git commit -m "feat: add support for custom restricted polygon zones"
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**:
   Explain the rationale, design decisions, and provide relevant test results.
