# RAG: Beyond The Basics

Welcome to the workshop repo!

## 🛠️ 1. Initial setup

To get the most out of this meetup, set up this repo to run on your laptop and follow along with the code. Sometimes
you'll be asked to hunt for bugs and find solutions on your own, and the best way to do this is if it's all at your
fingertips.

**If you are a developer**, it's all standard procedure: clone the repo, update tools, install dependencies. You might
even start by running the check commands and skim the text only if something fails.  
**If you are not a developer**, this could be a significant challenge—but if you're technically inclined and open to
Googling to troubleshoot issues, you can do it. Each section includes commands, explanations, and checks so
you won't feel lost. This setup will also be useful for anyone interested in Python coding beyond this workshop.

We'll start with system-level tools, then move on to project-specific setup. **Please go step-by-step, and don’t skip
any steps**—a complete setup will ensure you get the maximum benefit from the workshop.

### 🐚 1.1 Unix shell

A POSIX-compliant shell, like **Bash** or **Zsh** is needed to execute the commands listed below, including those that
run the application. **PowerShell** will not work.

Such shells come factory-installed on Mac and Linux. On Windows, there are some options to choose from:

- [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) (complete Unix environment)
- [Git Bash](https://git-scm.com/downloads/win) (quicker, simpler setup, part of the Git for Windows installation).

When you're done, run this in your new shell for an initial check on your shell installation. Look for an "OK" at the
end. If there is no "OK", or it fails with some ugly error, then you're not using the right shell:

```shell
( [ -n "$BASH_VERSION" ] || [ -n "$ZSH_VERSION" ] || command -v uname >/dev/null 2>&1 ) && echo "OK, you seem to have a compatible shell"
```

### 🌿 1.2 Git

We'll use version control to step through different parts of the development process, and Git is the tool for
this. You don't need to learn Git because we'll use some helper commands, but you need to set it up as follows.

1. **Install**: If you're on Windows and installed Git Bash above, you already have this. Otherwise, installation
   instructions for all operating systems are on [this page](https://git-scm.com/downloads).
2. **Clone the repo**: If you haven't yet, then please do this now. If it's your first time, you can find general
   instructions [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
   Important: don't use the ZIP download option, you must use the `git clone` command.
3. **Set as working directory**: All commands in this README need to be run with this folder (repo root) as the working
   directory. If you open this repo in an IDE (see below), then this will be the default behavior. You can run this to
   check (it should say "OK"):
   ```shell
   ([ -d ".git" ] && git config --get remote.origin.url | grep -q "rag-beyond-the-basics" && echo "OK: You're at the repo root") || (echo >&2 "NOK: You're somewhere else" && exit 1)
   ```
4. Now you can run this to double-check your shell installation (it should say "OK"):
   ```shell
   chmod +x scripts/check_shell.sh && ./scripts/check_shell.sh
   ```
   (If this fails because you use some other esoteric shell, but you know what you're doing, no problem, just have
   something POSIX-compliant.)
5. And this to check your Git installation (it should say "OK"):
   ```shell
   chmod +x scripts/check_git.sh && ./scripts/check_git.sh
   ```

### 🐍 1.3 Python

The app is written in Python, so this needs to be installed on your machine. Already installed on Macs, but that's for
the system itself: it's better to have a separate installation of the version that's tested to work with this
app: please install version **3.12.7** from [this page](https://www.python.org/downloads/release/python-3127/).

Here is what to expect:

- Will **not** work (too old): `3.11.10` ❌
- Will **probably** work: `3.12.0` ❔
- Will **definitely** work: `3.12.7` ✅
- Will **not** work (too new): `3.13.0` ❌

Please check your installation:

```shell
chmod +x scripts/check_python.sh && ./scripts/check_python.sh
```

**Note:** The following scripts use the **python** executable. If your installation only included **python3** in your
PATH, or you prefer to use **python3.12**, feel free to modify the scripts, just make sure they use the right version.

We also need to ensure that **pip**, the Python package manager, is up-to-date.  
Please check:

```shell
chmod +x scripts/check_pip.sh && ./scripts/check_pip.sh
```

And if needed, run:

```shell
python -m pip install --upgrade pip
```

### 🖥 1.4 IDE / Code editor

Needed to easily navigate the repo and run the app in debug mode, which can really help you understand what's happening.
If you just want to run the app, you can do it in the terminal as well. Some good choices
are: [PyCharm](https://www.jetbrains.com/pycharm/), [VS Code](https://code.visualstudio.com/).

If you're on Windows, make sure the IDE is configured to use the POSIX shell you've installed, or the commands won't
work. Here are guides
for [PyCharm](https://www.jetbrains.com/help/pycharm/settings-tools-terminal.html#application-settings)
and [VS Code](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git#_git-bash-on-windows).

### 📦 1.5 Python dependencies

Here we install libraries for things like calling OpenAI, creating a vector database, etc. This will download about
500MB of stuff. We will create a virtual environment that will live in this repo only. Later, you can delete all
dependencies by deleting this folder, if you don't want them anymore. **Pick the first option you like**:

1. If your IDE offers to set up the Poetry environment/interpreter using [pyproject.toml](./pyproject.toml), that will
   probably work.
2. Or, if you use Poetry, you can also:
   ```shell
   poetry lock && poetry install && [[ -n "$VIRTUAL_ENV" && "$VIRTUAL_ENV" == "$(pwd)/.venv" ]] || poetry shell
   ```
3. Or, if you have another preferred way of setting up the virtual environment, and you know what you're doing, feel
   free.
4. Otherwise, you should:
   ```shell
   python -m venv .venv && source .venv/bin/activate && python -m pip install -e .
   ```

After this, the virtual environment should be active and your terminal prompts should start with `(.venv)` or
`(rag-beyond-the-basics-py3.12)` or similar. All further commands must be executed with the shell in this state. Run
this to check (it should say "OK"):

```shell
chmod +x scripts/check_venv.sh && ./scripts/check_venv.sh
```

**Only if** the virtual environment is not active, this is how to reactivate:

1. If you used Poetry:
   ```shell
   poetry shell
   ```
2. Otherwise:
   ```shell
   source .venv/bin/activate
   ```

You may need to do this every time you close and reopen the shell.

### 📈 1.6 LangSmith

This will turbocharge your insights. We'll use it to debug into the RAG chain during the workshop, because this is
difficult to do locally. LangSmith is a paid LLM observability platform, but it has a volume-based free tier that you
are never going to exceed until you do something serious. You can technically skip this and still run the RAG script,
but it is definitely worth trying out.

1. Create a free account at https://smith.langchain.com/.
2. Note down your API key in a safe place, you'll need it during the workshop.

### 🎯 1.7 Final tests

1. Double-check all of the above (it should say "OK" or better five times):
   ```shell
   chmod +x scripts/check_tools.sh && ./scripts/check_tools.sh
   ```
2. Finally, if the following script prints something nice to the console, then you did everything right:
   ```shell
   chmod +x .venv/bin/ws && ws hello
   ```

**Only if** the `ws` command gives you permission errors:

1. If you used Poetry, try this instead:
   ```shell
   poetry run ws hello
   ```

## 📅 2. During the workshop

**You can read these ahead of time, but don't do them, they won't work!**

### 📍 2.1 Get back to where you were

Only if you did **not** set up an IDE project that handles this automatically, then, in the terminal...

1. Let's make sure your shell is still in the right place (it should say "OK"):
   ```shell
   ([ -d ".git" ] && git config --get remote.origin.url | grep -q "rag-beyond-the-basics" && echo "OK: You're at the repo root") || (echo >&2 "NOK: You're somewhere else" && exit 1)
   ```
2. And everything still works (it should say "OK" or better five times):
   ```shell
   chmod +x scripts/check_tools.sh && ./scripts/check_tools.sh
   ```
3. **Only if** the check said that the virtual environment is not active, this is how to reactivate:
    1. If you used Poetry:
       ```shell
       poetry shell
       ```
    2. Otherwise:
       ```shell
       source .venv/bin/activate
       ```

### 🌿 2.2 Git

Get the latest version of the repo (with tags):

```shell
git pull --tags
```

### 🔐 2.3 Environment variables

Config and various secrets (i.e. API keys) will be stored in a hidden file at [.env](./.env).

1. Create the file using the template by running this (it should say "OK"):
   ```shell
   (cp -n .env.example .env && echo "OK: Successfully created .env file") || echo >&2 "NOK: Couldn't create .env, maybe you already have it?"
   ```
2. Get your LangSmith API key and add it to `LANGCHAIN_API_KEY` in [.env](./.env).
3. Add other API keys marked with `TODO` (they will be provided at the workshop).

### 📦 2.4 Python dependencies

Let's update our dependencies.

1. If you use Poetry:
   ```shell
   poetry lock && poetry install
   ```
2. Otherwise:
   ```shell
   python -m pip freeze > temp_requirements.txt && python -m pip uninstall -r temp_requirements.txt -y && rm temp_requirements.txt && python -m pip install -e .
   ```

### 🐚 2.5 Workshop CLI

We will use some easy-to-type helper commands to run things and do time-traveling in the repo.  
You don't need to run these now, they are here for when you need them.

#### For execution

- Run the RAG script:
  ```shell
  ws run
  ```

- Run evaluations specific to the current version:
  ```shell
  ws evals
  ```

- Run all evaluations (you should rarely run this):
  ```shell
  ws evals --all
  ```

#### For navigation

- Print your current active version:
  ```shell
  ws where
  ```

- Step to the next version:
  ```shell
  ws next
  ```

- Step to the previous version:
  ```shell
  ws prev
  ```

- Go to the version you specify:
  ```shell
  ws goto VERSION
  ```

- Clean up any changes you made to the repo:
  ```shell
  git reset --hard
  ```

#### Troubleshooting

**Only if** the `ws` command gives you permission errors:

1. If you used Poetry, try prepending the commands with poetry run, for example:
   ```shell
   poetry run ws hello
   ```

### 2.6 Have fun!
