# Azure DevOps Pipeline Setup Guide

This guide explains how to configure the `azure-pipelines.yaml` file you just created to enable automated secret rotation.

## 1. Prerequisites
*   **Azure DevOps Project**: You need an active project.
*   **Service Connection**:
    1.  Go to **Project Settings** -> **Service connections**.
    2.  Create a new **Azure Resource Manager** connection.
    3.  Select **Workload Identity federation** (recommended) or Secret.
    4.  Name it `AzureConnection` (matches the variable in the yaml).
    5.  **Important**: This connection needs `Key Vault Secrets User` on your KV and `Azure Kubernetes Service Cluster User Role` on your AKS.

## 2. Import the Pipeline
1.  Go to **Pipelines** -> **New Pipeline**.
2.  Select **GitHub** (or where your code is).
3.  Select **Existing Azure Pipelines YAML file**.
4.  Point to `azure-pipelines.yaml`.

## 3. How it Works (The Logic)
This pipeline is designed to be a **"Worker"**. It is generic. It takes parameters so it can rotate *any* secret.

*   **Step 1: Fetch**: It logs into Azure and asks Key Vault for the *latest* value of `SQLPassword`.
*   **Step 2: Update**: It runs `kubectl apply` to update the secret object `sql-secrets` in the cluster.
*   **Step 3: Restart**: It runs `kubectl rollout restart`. This is the "Zero Downtime" feature. Kubernetes will spin up a NEW pod with the NEW password. Once it verifies the new pod is healthy, it terminates the old one.

## 4. Setting up the App Deployment Pipeline (CI/CD)
To automate the deployment of the Dashboard itself:
1.  Create another **New Pipeline**.
2.  Select `azure-pipelines-app.yaml`.
3.  Name it: `secrets-dashboard-ci-cd`.

### Triggers
*   **Automatic**: This pipeline runs every time you push code to the `main` branch.
*   **Action**: It builds a new Docker image with a unique tag (`BuildId`), pushes it to ACR, and upgrades the Helm release in your cluster.

## 5. How to Trigger the Rotation Pipeline (The Automation)
In Phase 3, you will use an **Azure Logic App** or **Azure Function** to trigger the *Rotation Pipeline* via API whenever a secret changes.

**API Call Example (what the Logic App will do):**
```json
POST https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipelineId}/runs?api-version=6.0-preview.1
{
    "templateParameters": {
        "SecretName": "SQLPassword",
        "K8sSecretName": "sql-secrets",
        "K8sKey": "password",
        "DeploymentName": "sql-server"
    }
}
```
