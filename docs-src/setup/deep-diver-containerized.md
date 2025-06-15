# Deep Diver Setup: Containerized

For developers who want to run the code with minimal local dependencies using containers.

## Prerequisites

- **Development experience** with basic command line and containerization
- **Container runtime** (Docker, Podman, Colima, etc.) installed and running
- **Git** installed

## Before the Workshop

### 1. Clone and navigate to the repository

```shell
git clone https://github.com/hosmanadam/rag-beyond-the-basics.git
cd rag-beyond-the-basics
```

### 2. Prepare environment file

```shell
cp .env.example .env
```

### 3. Test the setup

```shell
docker-compose up
```

The container should build, but **fail** with an error about missing environment variables - this is correct behavior
unless you've added your own API keys. You'll add the workshop API keys later.

### 4. Stop the container

```shell
docker-compose down
```

### 5. Optional: Set up your own LangSmith account

If you want to debug your own traces instead of using shared workshop access:

1. Sign up for a free account at [https://smith.langchain.com](https://smith.langchain.com)
2. Get your API key from the account settings
3. Add `LANGCHAIN_API_KEY` to your `.env` file

## During the Workshop

### 1. Get latest code

```shell
git pull
```

### 2. Add API keys (provided during workshop)

Edit `.env` file with the API keys we provide.

### 3. Start the application

```shell
docker-compose up
```

### 4. Access the application

The application will start and print a URL in the console. Click the link to access the Chainlit interface.

## Debugging and Observability

You'll participate in debugging exercises using LangSmith:

- **Shared access**: We'll provide credentials to view workshop traces
- **Your own traces**: If you set up your own account above, you'll see your own traces

LangSmith access: [https://smith.langchain.com](https://smith.langchain.com)

## After the Workshop

### Cleanup

```shell
# Stop and remove containers
docker-compose down

# Remove containers and image
export IMAGE="rag-beyond-the-basics-chainlit-gui"
docker rm -f $(docker ps -a -q --filter "ancestor=$IMAGE") || echo "No containers are using $IMAGE"
docker rmi -f $IMAGE

# Delete the entire repository (removes all dependencies)
cd ..
rm -rf rag-beyond-the-basics
```

Ready to dive deep! 🐋
