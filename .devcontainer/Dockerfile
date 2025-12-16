# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.10

# Ensure basic utilities exist (varies by base image)
RUN if command -v apt-get >/dev/null 2>&1; then \
        apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && \
        rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null 2>&1; then \
        apk add --no-cache curl ca-certificates bash; \
    fi

# Install Azure CLI
RUN if command -v apt-get >/dev/null 2>&1; then \
        curl -sL https://aka.ms/InstallAzureCLIDeb | bash; \
    elif command -v apk >/dev/null 2>&1; then \
        apk add --no-cache azure-cli; \
    else \
        echo "Unsupported distro for Azure CLI install" && exit 1; \
    fi

# Install uv (provides `uv` and `uvx`)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --install-dir /usr/local/bin

# Install .NET SDK (some MCP servers/tools depend on it)
RUN curl -LsSf https://dot.net/v1/dotnet-install.sh -o /tmp/dotnet-install.sh \
    && bash /tmp/dotnet-install.sh --channel 8.0 --install-dir /usr/local/dotnet --no-path \
    && ln -sf /usr/local/dotnet/dotnet /usr/local/bin/dotnet

# Install Node.js + npm (provides `npx` for MCP servers like Context7)
RUN if command -v apt-get >/dev/null 2>&1; then \
        curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
        apt-get update && apt-get install -y nodejs && \
        rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null 2>&1; then \
        apk add --no-cache nodejs npm; \
    else \
        echo "Unsupported distro for Node.js install" && exit 1; \
    fi

# Verify installs
RUN az version && node --version && npm --version && npx --version && uvx --version && dotnet --version
