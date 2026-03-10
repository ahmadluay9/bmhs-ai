# gcloud cli
## 1. instalasi gcloud
- a. Windows
```bash
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

& $env:Temp\GoogleCloudSDKInstaller.exe    
```

- b. ubuntu
```bash
# 1. Import the Google Cloud public key.
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
```

```bash
# 2. Add the gcloud CLI distribution URI as a package source.
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
```

```bash
sudo apt-get update && sudo apt-get install google-cloud-cli
```

## 2. Inisiasi gcloud
```bash
gcloud init
```

## 3. Authorizes the Google Cloud CLI to access Google Cloud resources using your user credentials. 
```bash
gcloud auth login
```

## 4. Acquire user credentials for Application Default Credentials (ADC)
```bash
gcloud auth application-default login
```

## 5. authorize the gcloud CLI to use the credentials of a service account via a local key file for authentication.
```bash
gcloud auth activate-service-account [SERVICE_ACCOUNT_EMAIL] --key-file=[KEY_FILE]
```

## 6. List account
```bash
gcloud auth list
```

## 7. List the properties in your active gcloud CLI configuration
```bash
gcloud config list
```
---

# UV
## 1. Installasi UV
- a. Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- b. macOS dan Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Insiasi UV
```bash
# buat direktori folder baru
mkdir FOLDER_NAME

# ubah direktori
cd FOLDER_NAME

# inisiasi uv
uv init
```

## 3. Membuat virtual environment

```bash
uv venv
```
- apabila ingin spesifik versi python tertentu
```bash
uv venv --python 3.XX
```
- aktivasi venv
```bash
.venv\Scripts\activate
```

## 4. Instalasi python package
```bash
uv add python_package_1 python_package_2
```
---
# MCP Toolbox
[Dokumentasi](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
## 1. Installasi MCP
- a. Windows
```bash
$VERSION = "0.28.0"
curl.exe -o toolbox.exe "https://storage.googleapis.com/genai-toolbox/v$VERSION/windows/amd64/toolbox.exe"
```
- b. Linux

```bash
export VERSION=0.28.0
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v$VERSION/linux/amd64/toolbox
chmod +x toolbox
```
## 2. Buat file `tools.yaml`

```bash
nano tools.yaml
```
Kemudian paste script di bawah ini
```yaml
sources:
  my-bigquery-source:
    kind: bigquery
    project: ${GOOGLE_CLOUD_PROJECT}
    location: ${REGION}

tools:
  tool_name:
    kind: bigquery-sql
    source: my-bigquery-source
    description: "Tool Description"
    parameters:
      - parameter_name : parameter name
        type: parameter type (string, integer, etc.)
        description: "Parameter Description."
    statement: |
      SELECT * 
      FROM `project_id.dataset_name.table_name`;

toolsets:
   toolset_name:
     - tool_name
```
Kemudian tekan `CTRL+O` (untuk menyimpan) dan `CTRL+X` untuk keluar dari editor.
## 3. Running MCP Server di Local Computer
```bash
./toolbox --tools-file "tools.yaml"
```
---
# Cloud Run Deployment
## 1. Environment Setup
- a. Powershell
```bash
$env:GOOGLE_CLOUD_PROJECT = "Your Project Name"
# Geographic area where Gemini model requests are processed, e.g (us-central1, asia-southeast2)
$env:REGION = "Your Project Location"
$env:IMAGE = "us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest"
$env:SERVICE_ACCOUNT_NAME = "Your Service Account Name"
$env:APP_SECRET_NAME = "Your Application Secret Name"
$env:CLOUD_RUN_SERVICE_NAME = "Your Cloud Run Service Name"
```
- b. Linux
```bash
export GOOGLE_CLOUD_PROJECT = "Your Project Name"
export REGION="Your Project Location"
export IMAGE="us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest"
export SERVICE_ACCOUNT_NAME="YOUR_SERVICE_ACCOUNT_NAME"
export APP_SECRET_NAME = "YOUR_APP_SECRET_NAME"
export CLOUD_RUN_SERVICE_NAME = "Your Cloud Run Service Name"
```

## 2. Enable APIs
- a. Powershell
```bash
gcloud services enable run.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com `
    iam.googleapis.com `
    secretmanager.googleapis.com
```
- b. Linux
```bash
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    iam.googleapis.com \
    secretmanager.googleapis.com
```

## 3. Buat Service Account dan Permission
- a. Powershell
```bash
# Create the service account
gcloud iam service-accounts create $env:SERVICE_ACCOUNT_NAME `
    --display-name="Display Name"

# Grant Secret Accessor role
gcloud projects add-iam-policy-binding $env:GOOGLE_CLOUD_PROJECT `
    --member="serviceAccount:$env:SERVICE_ACCOUNT_NAME@$($env:GOOGLE_CLOUD_PROJECT).iam.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"

# Grant Bigquery jobuser role
gcloud projects add-iam-policy-binding $env:GOOGLE_CLOUD_PROJECT `
    --member="serviceAccount:$env:SERVICE_ACCOUNT_NAME@$($env:GOOGLE_CLOUD_PROJECT).iam.gserviceaccount.com" `
    --role="roles/bigquery.jobUser"

# Grant Bigquery dataViewer Role
gcloud projects add-iam-policy-binding $env:GOOGLE_CLOUD_PROJECT `
    --member="serviceAccount:$env:SERVICE_ACCOUNT_NAME@$($env:GOOGLE_CLOUD_PROJECT).iam.gserviceaccount.com" `
    --role="roles/bigquery.dataViewer"
```

- b. Linux
```bash
# Create the service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="Display Name"

# Grant Secret Accessor role
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Grant Bigquery jobuser role
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

# Grant Bigquery dataViewer Role
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

## 4. Simpan `tools.yaml` file ke secret manager
- a. Powershell
```bash
gcloud secrets create $env:APP_SECRET_NAME --data-file="tools.yaml"
```

- b. Linux
```bash
gcloud secrets create $APP_SECRET_NAME --data-file="tools.yaml"
```

## 5. Deploy ke Cloud Run
- a. Powershell
```bash
gcloud run deploy $env:CLOUD_RUN_SERVICE_NAME `
    --image $env:IMAGE `
    --service-account "$env:SERVICE_ACCOUNT_NAME@$($env:GOOGLE_CLOUD_PROJECT).iam.gserviceaccount.com" `
    --region $env:REGION `
    --set-secrets "/app/tools.yaml=$env:APP_SECRET_NAME:latest" `
    --args="--tools-file=/app/tools.yaml,--address=0.0.0.0,--port=8080"
```

- b. Linux
```bash
gcloud run deploy $CLOUD_RUN_SERVICE_NAME \
    --image $IMAGE \
    --service-account "${SERVICE_ACCOUNT_NAME}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --region $REGION \
    --set-secrets "/app/tools.yaml=${APP_SECRET_NAME}:latest" \
    --args="--tools-file=/app/tools.yaml,--address=0.0.0.0,--port=8080"
```

# ADK
## 1. Buat agen project baru
```bash
adk create APP_NAME
```

atau bisa jalankan command berikut
* a. Powershell
```bash
adk create APP_NAME `
    --model gemini-2.5-flash `
    --project $env:GOOGLE_CLOUD_PROJECT `
    --region $env:GOOGLE_CLOUD_LOCATION
```
* b. Linux
```bash
adk create APP_NAME \
    --model gemini-2.5-flash \
    --project $GOOGLE_CLOUD_PROJECT \
    --region $GOOGLE_CLOUD_LOCATION
```
## 2. Jalankan Web UI ADK
```bash
adk web
```

# A2A
## 1. Cara menjalankan A2A di local environment
```bash
uv run uvicorn agent_directory.agent:a2a_app --host 127.0.0.1 --port 8001
```

## 2. Buka URL ini untuk melihat agent card
```
http://127.0.0.1:8001/.well-known/agent-card.json
```

atau 
```
http://localhost:8001/.well-known/agent-card.json
```

## 3. Deploy A2A ke Cloud Run
### 1. Environment Setup
- a. Powershell
```bash
$env:GOOGLE_CLOUD_PROJECT = "Your Project Name"
# Geographic area where Gemini model requests are processed, e.g (us-central1, asia-southeast2)
$env:GOOGLE_CLOUD_LOCATION = "Your Vertex AI location"
$env:GOOGLE_GENAI_USE_VERTEXAI = "Default value is '1'"
$env:REGION = "Your Project Location"
$env:IMAGE = "us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest"
$env:SERVICE_ACCOUNT_NAME = "Your Service Account Name"
$env:APP_SECRET_NAME = "Your Application Secret Name"
$env:CLOUD_RUN_SERVICE_NAME = "Your Cloud Run Service Name"
$env:TOOLBOX_URL = "Cloud Run URL for MCP Toolbox"
```
- b. Linux
```bash
export GOOGLE_CLOUD_PROJECT = "Your Project Name"
export GOOGLE_CLOUD_LOCATION = "Your Vertex AI location"
export GOOGLE_GENAI_USE_VERTEXAI = "Default value is '1'"
export REGION="Your Project Location"
export IMAGE="us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest"
export SERVICE_ACCOUNT_NAME="YOUR_SERVICE_ACCOUNT_NAME"
export APP_SECRET_NAME = "YOUR_APP_SECRET_NAME"
export CLOUD_RUN_SERVICE_NAME = "Your Cloud Run Service Name"
export TOOLBOX_URL = "Cloud Run URL for MCP Toolbox"
```