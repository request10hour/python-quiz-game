# Python Quiz Game - Project Guidelines

## Code Style
- Use Python 3.x with type hints (PEP 484).
- Follow PEP 8 style guidelines.
- Keep functions and classes modular and focused on a single responsibility.
- Coding Level: Limit the complexity to what is expected of a senior undergraduate computer science student. Do not over-engineer.
- Scope: When a feature is requested, implement only the essential functionalities briefly and stop there.
- UI/Output Style: Keep CLI outputs extremely minimal and plain. Do NOT use emojis, decorative ASCII borders (e.g., `======`), or unnecessary formatting. Use simple, flat text strings for menus and messages.

## Architecture
- Since this is a Python quiz game, keep the quiz data (questions, answers) separate from the core game engine logic (e.g., loading from a config or JSON file).
- The main entry point should be a `main.py` script.

## Build and Test
- Use standard library modules where possible to minimize external dependencies.
- Standard dependency management: define any required packages in a `requirements.txt` (or via Poetry/Pipenv if preferred).
- Use `pytest` for testing. Place all tests in a dedicated `tests/` directory at the root.

## Conventions
- Provide clear, descriptive docstrings for modules, classes, and non-trivial functions.
- Avoid hardcoding configuration values; use constants or configuration files.

- Exception Handling: Do NOT implement exception or error handling automatically. If you anticipate edge cases or invalid inputs (e.g., alphabets instead of numbers, unexpected number of arguments), ask the user first to discuss possible scenarios and wait for their confirmation before writing any exception handling code.