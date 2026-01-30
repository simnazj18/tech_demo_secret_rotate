import os
import sys
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import HttpResponseError

def verify_azure_connection():
    print("--- Verifying Azure Connection ---")
    
    # 1. Check for Key Vault URL
    vault_url = os.getenv("AZURE_KEYVAULT_URL")
    if not vault_url:
        print("ERROR: AZURE_KEYVAULT_URL environment variable is not set.")
        print("Please export it: export AZURE_KEYVAULT_URL='https://<your-vault>.vault.azure.net/'")
        return False

    print(f"Target Key Vault: {vault_url}")

    # 2. Try to get credentials (supports AZ CLI, Env Vars, Managed Identity)
    try:
        print("Attempting to acquire credentials (via DefaultAzureCredential)...")
        credential = DefaultAzureCredential()
        # Trigger a token request to verify auth immediately
        token = credential.get_token("https://vault.azure.net/.default")
        print("SUCCESS: Authenticated successfully.")
    except Exception as e:
        print(f"ERROR: Authentication failed. \nDetails: {str(e)}")
        print("Tip: Run 'az login' if running locally.")
        return False

    # 3. Test Key Vault Access
    try:
        print(f"Connecting to Key Vault client...")
        client = SecretClient(vault_url=vault_url, credential=credential)
        
        print("Listing secrets (top 5)...")
        secrets = client.list_properties_of_secrets()
        count = 0
        for secret in secrets:
            print(f" - Found secret: {secret.name} (Enabled: {secret.enabled})")
            count += 1
            if count >= 5: 
                break
        
        if count == 0:
            print("SUCCESS: Connected to Key Vault (No secrets found or empty).")
        else:
            print(f"SUCCESS: Connected to Key Vault and listed {count} secrets.")
            
    except HttpResponseError as e:
        print(f"ERROR: Access to Key Vault failed.")
        print(f"Status Code: {e.status_code}")
        print(f"Message: {e.message}")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        return False

    return True

if __name__ == "__main__":
    if verify_azure_connection():
        print("\n[OK] Azure connection verified. Ready to proceed with backend.")
    else:
        print("\n[FAIL] Azure connection verification failed. Please fix issues before proceeding.")
        sys.exit(1)
