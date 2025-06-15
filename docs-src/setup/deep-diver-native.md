# Deep Diver Setup: Native

For experienced developers who want full control and the ability to browse, run, debug, and tweak the code.

## Prerequisites

- **Development experience** with basic command line and version control
- **Python 3.12.x** installed and accessible via `python` command
- **Git** installed
- **Your preferred development environment** (IDE, editor, shell, etc.)

## Setup

### 1. Clone and navigate to the repository

```shell
git clone https://github.com/hosmanadam/rag-beyond-the-basics.git
cd rag-beyond-the-basics
```

### 2. Verify Python version

```shell
python --version
```

Should show `Python 3.12.x`. If you only have `python3`, feel free to use that throughout.

### 3. Set up Python dependencies

Choose your preferred approach:

**Option A: Using Poetry (if you have it)**

```shell
poetry install && poetry shell
```

**Option B: Using venv**

```shell
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m pip install -e .
```

### 4. Prepare environment variables

```shell
cp .env.example .env
```

### 5. Verify setup

```shell
ws hello
```

This should print a welcome message and confirm all dependencies are working.

### 6. Optional: Set up your own LangSmith account

If you want to debug your own traces instead of using shared workshop access:

1. Sign up for a free account at [https://smith.langchain.com](https://smith.langchain.com)
2. Get your API key from the account settings
3. Add `LANGCHAIN_API_KEY` to your `.env` file

## During the Workshop

### 1. Get latest code

```shell
git pull
```

### 2. Activate your environment (if not using an IDE that handles this)

**Poetry**: `poetry shell`  
**venv**: `source .venv/bin/activate`

### 3. Update dependencies

`poetry install` or `python -m pip install -e .`

### 4. Add API keys to `.env` file (provided during workshop)

### 5. Run the application

```shell
ws gui
```

This opens the Chainlit interface in your browser.

## Debugging and Observability

You'll participate in debugging exercises using LangSmith:

- **Shared access**: We'll provide credentials to view workshop traces
- **Your own traces**: If you set up your own account above, you'll see your own traces

LangSmith access: [https://smith.langchain.com](https://smith.langchain.com)

## Troubleshooting

- **Python version issues**: We need 3.12.x specifically for compatibility with all dependencies
- **Virtual environment not active**: Make sure your terminal prompt shows `(.venv)` or similar
- **Permission errors with `ws` command**: Try `poetry run ws hello` instead (if using Poetry)
- **Import errors**: Run `python -m pip install -e .` again

## After the Workshop

### Cleanup

If you no longer need this environment:

```shell
# Delete the entire repository (removes all dependencies)
cd ..
rm -rf rag-beyond-the-basics
```

This removes everything - the code, virtual environment, and all dependencies.

Ready to dive deep! 🤿
