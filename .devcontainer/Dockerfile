# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.10

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Node.js (using NodeSource for latest LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash && \
    apt-get install -y nodejs

# Verify installs
RUN az version && node --version && npm --version
