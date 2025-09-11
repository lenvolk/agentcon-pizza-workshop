#!/bin/bash

# Default role (can be overridden by first argument)
role=${1:-"Azure AI User"}

# Get subscription ID
subscriptionId=$(az account show --query id -o tsv)

# Get current signed-in user principal name
assignee=$(az ad signed-in-user show --query userPrincipalName -o tsv)

# Get the only resource group name in this subscription
resourceGroup=$(az group list --query "[0].name" -o tsv)

# Construct the scope
scope="/subscriptions/$subscriptionId/resourceGroups/$resourceGroup"

# Run the Azure CLI command
echo "Using subscription: $subscriptionId"
echo "Using resource group: $resourceGroup"
echo "Assigning role '$role' to current user: $assignee"
az role assignment create \
  --role "$role" \
  --assignee "$assignee" \
  --scope "$scope"