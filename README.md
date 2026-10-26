# Microsoft Foundry Starter

[![Microsoft Foundry](https://img.shields.io/badge/Microsoft_Foundry-0078D4?style=flat)](https://ai.azure.com/)

A tutorial project that uses Python to authenticate to Microsoft Foundry, connect to a project, and call an LLM deployment.

After completing the setup below, you will have a local Python script that sends a prompt to your deployed model and prints its response.

## The Scenario

This is the starting point for AI development on Azure: set up a Foundry project, deploy a model, and make your first request. The script uses your Azure CLI sign-in and asks the model to reply with `FOUNDRY_OK`.

## Before You Start

You need:

- **Python** installed locally. Python 3.12 was used to test this starter. Download it from [python.org ↗](https://www.python.org/downloads/). On Windows, enable the option to add Python to PATH if the installer offers it.
- **Git** to clone the repository. See the [Git downloads ↗](https://git-scm.com/downloads/) for your operating system.
- **An Azure account with an active subscription** and permission to create a Foundry project and deploy a model, or access to a project someone has prepared for you. If you are new to Azure, see the [Azure account signup ↗](https://azure.microsoft.com/en-us/free/).
- **Azure CLI** to sign in from your terminal. Install it using the instructions below.

The Python packages are listed in `requirements.txt` and will be installed together later. Azure CLI is a separate installation, not a Python requirement.

**Costs:** Each run sends a request to an Azure-hosted model. Model usage can incur charges. Review the deployment's pricing before using it.

### Install Azure CLI

**macOS**

If you do not have Homebrew, install it using the instructions at [brew.sh ↗](https://brew.sh/). Then run:

```bash
brew update
brew install azure-cli
```

See Microsoft's [macOS installation guide ↗](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos) if installation fails.

**Windows**

Open PowerShell and run:

```powershell
winget install --exact --id Microsoft.AzureCLI
```

Close and reopen your terminal after installation. If `winget` is unavailable, use the installer linked in Microsoft's [Windows installation guide ↗](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows).

**Linux**

Follow Microsoft's [Linux installation guide ↗](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux) for your distribution.

Check that Azure CLI is available:

```bash
az version
```

## Set Up Foundry

If you already have a suitable project and model deployment, skip to step 3.

### 1. Create a Project

Open [Microsoft Foundry ↗](https://ai.azure.com/) and sign in. Use the new Foundry experience; enable the **New Foundry** toggle if shown.

Select **Create new project** from the project selector. Give it a name, such as `starter-tutorial`. Under **Advanced options**, choose your subscription, resource group, and a supported region. A resource group is a folder-like container for your Azure resources. Create the project and wait for provisioning to finish.

### 2. Deploy a Model

Select **Build > Models > Deploy > Deploy a base model**. Search for `gpt-5-mini`, open the model, and select **Deploy > Default settings**. Note the deployment name and wait until the deployment is ready.

For screenshots and setup details, see Microsoft's [Foundry resource quickstart ↗](https://learn.microsoft.com/en-us/azure/foundry/tutorials/quickstart-create-foundry-resources).

The script needs a model that supports the Responses API. Availability depends on your region and quota; an existing compatible deployment can also be used. Check Microsoft's [Responses API guide ↗](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses) for supported models and regions.

### 3. Collect the Connection Details

Copy the **project endpoint** from your project's welcome screen. Also keep the model's **deployment name**. You will put both values in `.env` during local setup.

The project endpoint includes `/api/projects/` and your project name. Copy it exactly as displayed; do not substitute a model inference endpoint or an Azure OpenAI resource URL.

The deployment name is the name of your deployed instance, which may differ from the underlying model name. For example, a deployment of `gpt-5-mini` could be named `starter-model`.

### 4. Check Access

The account you use for `az login` needs permission to access the project and call the model. **Foundry User**, formerly **Azure AI User**, is the standard developer role for this access.

If an administrator prepared the project, ask them to confirm your access. In the Azure portal, they can assign Foundry User to your account through the Foundry resource's **Access control (IAM)** page. Resource creation and model deployment require additional management permissions. See Microsoft's [Foundry permissions guide ↗](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry).

## Run Locally

Run the following commands on your own computer, not in Azure Cloud Shell.

### 1. Clone the Repository

```bash
git clone https://github.com/emfrg/msfoundry-starter.git
cd msfoundry-starter
```

If you already have the repository locally, open a terminal in its root folder instead.

### 2. Create and Activate a Virtual Environment

A virtual environment keeps this project's Python packages separate from your other projects.

**macOS / Linux**

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

The Windows commands select Python 3.12. If you installed another compatible version, use that version instead.

Your terminal will usually show `(.venv)` when the environment is active. Use `python` for the remaining Python commands on both operating systems.

### 3. Install the Requirements

```bash
python -m pip install -r requirements.txt
```

Use the versions in this file rather than independently upgrading the SDKs. The project includes compatibility constraints between its dependencies.

### 4. Configure the Project

Create your local configuration file from the example.

**macOS / Linux**

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

Open `.env` in your editor and replace the placeholders with the values from Foundry:

```dotenv
PROJECT_ENDPOINT=https://<resource>.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT_NAME=<your-deployment>
```

The URL above illustrates the format. Use your actual copied endpoint, even if its hostname differs from this example. Remove the angle-bracket placeholders.

No API key is required for this local setup. `.env` is ignored by Git; do not publish it.

### 5. Sign In to Azure

```bash
az login
```

Complete the sign-in flow using the account that has access to your project. If prompted, choose the subscription containing your Foundry resource. See Microsoft's [Azure CLI sign-in guide ↗](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli-interactively).

Check the selected account and subscription:

```bash
az account show --output table
```

If you need a different subscription:

```bash
az account set --subscription "<your-subscription-name-or-id>"
```

### 6. Check the Foundry Connection

```bash
python main.py
```

This is the complete starter. It uses `AzureCliCredential` for authentication, connects with `AIProjectClient`, and calls the deployment through `get_openai_client().responses.create()`.

A successful run should look like this:

```text
Azure CLI authentication: OK
Foundry project connection: OK
Model deployment: OK
Response: FOUNDRY_OK
```

If it fails, see [Troubleshooting](#troubleshooting) below. When you return later, activate `.venv` again before running the script. You do not need to reinstall the requirements for each session.

## Try the Demo

Open `main.py` and find the request:

```python
response = openai_client.responses.create(
    model=model_deployment,
    input="Reply with only: FOUNDRY_OK",
)
```

Change the `input` text to a question, such as `What is Microsoft Foundry? Answer in one sentence.`, and run `python main.py` again. The model's reply appears after `Response:`. Each run sends one independent request.

## Project Files

| File | Purpose |
| --- | --- |
| `main.py` | Authenticates with Azure CLI, connects to Foundry, and calls the model deployment. |
| `requirements.txt` | Lists the Python dependencies and compatibility constraints. |
| `.env.example` | Provides the configuration fields to copy into your local `.env`. |
| `.gitignore` | Excludes local configuration, the virtual environment, Python cache files, and local reference clones from Git. |

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `az` is not recognized or found | Install Azure CLI and reopen your terminal. It is not installed by `requirements.txt`. |
| `python`, `python3`, or `py` is not found | Confirm Python is installed and available on PATH. Reopen the terminal after installation. |
| `ModuleNotFoundError` or an unexpected SDK error | Activate `.venv` and run `python -m pip install -r requirements.txt` using the same environment as the script. |
| `PROJECT_ENDPOINT` or `MODEL_DEPLOYMENT_NAME` is missing | Check that `.env` is in the repository root, is not named `.env.txt`, and contains both values. |
| Authentication fails or a request returns `401` | Run `az login` again with the account that can access the project. |
| A request returns `403` | Ask your administrator to check your Foundry role assignments. Signing in alone does not grant access. Allow time for new assignments to take effect. |
| A request returns `404` or the deployment cannot be found | Check the project endpoint and deployment name against the portal. The deployment must belong to the intended Foundry resource and be ready. |
| A request returns `429` | Check your deployment's quota and rate limits. Wait before retrying, or ask your administrator about capacity. |

### Azure Sign-In Does Not Open

Try device-code sign-in:

```bash
az login --use-device-code
```

Follow the URL and code printed in the terminal. Use the account with access to your project.

### PowerShell Blocks Virtual Environment Activation

On a personal machine, you can allow activation scripts for the current PowerShell session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

If your organization manages this setting, follow its policy rather than trying to bypass it.

## Demo Limitations

- This is a local learning project that makes one model request per run. It has no agent, tools, chat interface, or conversation history.
- The script checks for a nonempty response. The model's wording can vary, including when asked to reply with `FOUNDRY_OK`.
- Stopping the script does not remove the Azure resources you set up. If you created a dedicated tutorial resource group, remove it when no longer needed, after checking that it contains no resources you still use.
