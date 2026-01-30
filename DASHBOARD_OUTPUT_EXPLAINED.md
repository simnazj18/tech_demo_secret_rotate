# Dashboard Output Explained

Use this guide to explain the final result (the Dashboard Page) to your reviewers. Break it down section by section.

## 1. Top Status Cards (The High-Level View)
*   **"ACTIVE SECRETS (K8S): 2"**:
    *   *Meaning*: The system scanned the cluster and found **2 instances** where a Pod is loading a secret.
    *   *Context*: Specifically, our `sql-server` pod is loading both a username and a password.
*   **"MANAGED IN AKV: 3"**:
    *   *Meaning*: It connected to Azure Key Vault and found **3 master secrets** stored there (`SQLUsername`, `SQLPassword`, `DatabasePassword`).
*   **"DRIFT STATUS: Synced"**:
    *   *Meaning*: This is the most important indicator. It means "Every secret used in Kubernetes matches a valid secret in Azure." If someone changed a password in Azure but didn't update the Cluster, this would turn **Red**.

## 2. "Detected Secrets Usage" Table (The "Magic")
This table proves the **AI/Logic** of the system.
*   **Service / Pod (`sql-server`)**: Identifies *who* is using the secret.
*   **Check Mechanism (`EnvVar`)**: Shows *how* the secret is injected (Environment Variable in this case).
*   **K8s Secret Name (`sql-secrets`)**: This is the local resource name in the cluster.
*   **AKV Secret Value (`******`)**:
    *   *Security Feature*: We intentionally mask the value so it is never shown in plaintext during a demo or audit.
*   **AKV Correlation (`Synced with: SQLPassword`)**: 
    *   *Key Feature*: Notice the difference! The K8s secret is named `sql-secrets`, but the system correctly identified that *one specific key* matches the Azure secret `SQLPassword`.
    *   *Why it matters*: This proves **Value-Based Matching**. The system didn't just guess by name; it verified the actual credentials match.
*   **Status (`Synced`)**: Visual confirmation that the workload is safe.

## 3. "Vault Inventory" Table (The Source of Truth)
This shows what is actually inside the Azure Key Vault.
*   **Secret Name**: Lists the authoritative secrets (`DatabasePassword`, `SQLPassword`, `SQLUsername`).
*   **Status (`Enabled`)**: Confirms these secrets are active and valid in Azure.

## Summary Checklist for Demo
1.  Point to **"Drift Status"** to show overall health.
2.  Point to **"AKV Correlation"** to show the intelligent matching logic.
3.  Point to the **Masked Values (`******`)** to highlight security compliance.
