from __future__ import annotations

import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Resolve the .env file relative to this file, not the terminal's current folder.
BASE_DIR = Path(__file__).resolve().parent


def require_environment_variable(name: str) -> str:
    """Return a required environment variable or raise a setup error."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name}. Add it to {BASE_DIR / '.env'}.")
    return value


def main() -> None:
    """Verify dependencies, Azure CLI authentication, and model access."""
    # Load environment variables from .env file.
    load_dotenv(BASE_DIR / ".env")
    project_endpoint = require_environment_variable("PROJECT_ENDPOINT")
    model_deployment = require_environment_variable("MODEL_DEPLOYMENT_NAME")

    # Use the developer's Azure login to authenticate with the Foundry project.
    with AzureCliCredential() as credential:
        # Request a Foundry access token to verify the Azure CLI sign-in.
        credential.get_token("https://ai.azure.com/.default")
        print("Azure CLI authentication: OK")

        # Connect to the Foundry project that hosts the model deployment.
        with AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        ) as project_client:
            # Use the project's OpenAI client to call the Responses API.
            with project_client.get_openai_client() as openai_client:
                # NOTE: model is the deployment name you chose in Foundry.
                response = openai_client.responses.create(
                    model=model_deployment,
                    input="Reply with only: FOUNDRY_OK", # or something else
                )

    if not response.output_text:
        raise RuntimeError("The model deployment returned an empty response.")

    print("Foundry project connection: OK")
    print("Model deployment: OK")
    print(f"Response: {response.output_text}")


if __name__ == "__main__":
    main()
