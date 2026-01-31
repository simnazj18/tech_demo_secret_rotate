# GitHub Actions Setup Guide

To enable automated deployment of your `tech_demo` application to the AKS cluster `demo_project`, you need to configure the following secrets in your GitHub repository.

## 1. Configure Secrets
Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.

Add the following secrets:

| Secret Name | Value | Description |
| :--- | :--- | :--- |
| `AZURE_CREDENTIALS` | *(Output of `az ad sp create-for-rbac`)* | JSON output for Azure authentication. |
| `ACR_USERNAME` | `secretrotate2026` | Login username for ACR. |
| `ACR_PASSWORD` | `5QTwa3A1aKghY8gi3y7N3FhXLwPSPKyUjHuWiL4Zv6DVxS3jbCZRJQQJ99CAACYeBjFEqg7NAAACAZZCRDUQp` | Login password for ACR. |
| `AZURE_KEYVAULT_URL` | `https://kv-techdemo-1769683213.vault.azure.net/` | URL of your Key Vault. |
| `AZURE_CLIENT_ID` | *(Your Service Principal App ID)* | Client ID used by the app to access Key Vault. |
| `AZURE_CLIENT_SECRET` | *(Your Service Principal Password)* | Client Secret used by the app. |
| `AZURE_TENANT_ID` | `1dcc587a-e945-4997-ba86-712dcdfabb36` | Your Azure Tenant ID. |

> [!TIP]
> To generate `AZURE_CREDENTIALS`, run:
> ```bash
> az ad sp create-for-rbac --name "github-actions-ops" --role contributor --scopes /subscriptions/ff93113c-05e0-45e8-9fcd-9df5c1022559/resourceGroups/rg-secrets-demo --sdk-auth
> ```
> Use the `clientId` and `clientSecret` from the JSON output for `AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET`.

## 2. Commit and push
The deployment pipeline file has been created at `.github/workflows/deploy.yml`. 
Commit and push this file to your repository to trigger the first build.

```bash
git add .github/workflows/deploy.yml charts/secrets-dashboard/values.yaml
git commit -m "Setup deployment pipeline for AKS"
git push origin main
```

## 3. Verify Deployment
After the Action completes:
1.  Connect to your cluster:
    ```bash
    az aks get-credentials --resource-group rg-secrets-demo --name demo_project
    ```
2.  Get the external IP:
    ```bash
    kubectl get service secrets-dash-secrets-dashboard
    ```
3.  Open the External IP in your browser.
