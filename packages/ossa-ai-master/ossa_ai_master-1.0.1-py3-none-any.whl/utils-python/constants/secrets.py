from infisical import InfisicalClient
from typing import Any, Optional, Literal
from google.cloud import secretmanager
from dotenv import load_dotenv

load_dotenv()

def create_infisical_client(token: str) -> InfisicalClient:
    return InfisicalClient(token=token)

def get_infisical_secret(
    client: InfisicalClient,
    name: str,
    path: str,
    environment: Literal["development", "staging", "production", "testing"],
    type: Optional[Literal["personal", "shared"]] = "personal"
) -> Any:
    error_message = f"Secret with name '{name}' and type '{type}' could not be found at path '{path}' in environment '{environment}'"
    try:
        secret = client.get_secret(
            secret_name=name,
            path=path,
            environment=environment,
            type=type
        )

        if secret.secret_value is None:
            raise ValueError(error_message)
        
        return secret.secret_value
    except Exception:
        raise ValueError(error_message)

def get_google_secret(secret_path):
    """
    Access the secret stored in Google Secret Manager. 
    Uses application default credentials.
    For local development make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the service account key file.
    """
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_path + "/versions/latest")
    return response.payload.data.decode('UTF-8')