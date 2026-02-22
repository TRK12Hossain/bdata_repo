# Bangladesh Content Platform — GCS Orchestration MVP v3.1
## Work Breakdown Structure (Hybrid Cloud Edition)

**Document Version:** 3.1  
**Execution Environment:** Google Cloud Platform (Cloud Run Jobs)  
**Storage Environment:** Google Cloud Storage (GCS)  
**Configuration Source:** GitHub (Version Controlled)  
**Security Model:** Workload Identity Federation (OIDC)

---

## 🔄 Architecture Overview: The Hybrid Flow

This version splits the platform into two distinct zones: **GitHub** (where you think and write) and **GCP** (where the AI executes and stores data).



| Component | Location | Role |
| :--- | :--- | :--- |
| **The "Brain"** | **GitHub Repo** | Version control for brand DNA (configs) and agent instructions (prompts). |
| **The "Body"** | **Cloud Run Jobs** | Serverless compute engine that runs the Gemini CLI and scripts. |
| **The "Memory"** | **GCS Buckets** | Stores the research JSONs, draft Markdown files, and generated PNG charts. |
| **The "Heartbeat"**| **Cloud Scheduler** | Triggers the pipeline daily at 9:00 AM Bangladesh time. |
| **The "Bridge"** | **GitHub Actions** | Syncs your GitHub configs to GCS every time you push a change. |

---

## PHASE 0 — Security & Foundations (3 hours)

### 0.1 GCP Project & Storage
* **0.1.1** Access your existing GCP project (no new project creation required).
* **0.1.2** Enable necessary APIs: Cloud Run, Cloud Scheduler, Artifact Registry, Secret Manager, and Cloud Storage.
* **0.1.3** Create a **GCS Bucket**: `gs://bd-content-data`.
* **0.1.4** Create folder structure within the bucket: `/config`, `/prompts`, `/pipeline`, `/published`.

### 0.2 Workload Identity Federation (Zero-Key Security)
* **0.2.1** Set up a Workload Identity Pool in GCP to allow GitHub Actions to authenticate without Service Account JSON keys.
* **0.2.2** Create a Service Account `github-sync-sa` with the `Storage Object Admin` role limited to your bucket.
* **0.2.3** Configure GitHub Secrets: `GCP_PROJECT_ID`, `GCP_WORKLOAD_IDENTITY_PROVIDER`, and `GCP_SERVICE_ACCOUNT`.

### 0.3 Secrets & Environment
* **0.3.1** Store `GEMINI_API_KEY`, `INSTAGRAM_TOKEN`, and `SLACK_BOT_TOKEN` in **GCP Secret Manager**.
* **0.3.2** Grant the Cloud Run Service Account permission to access these specific secrets.

---

## PHASE 1 — Config & Version Control (4 hours)
*Stored and edited in GitHub; synced to GCS for the AI to read.*

### 1.1 Brand DNA (GitHub)
* **1.1.1** Write `config/writing_style_profile.md`: Tone, bilingual ratio, and training examples for the agents.
* **1.1.2** Write `config/visual_identity.md`: Hex colors, font rules, and Matplotlib constraints.
* **1.1.3** Write `config/editorial_preferences.md`: Original lens criteria (local vs. international) and banned topics.

### 1.2 The Sync Bridge (GitHub Actions)
* **1.2.1** Create `.github/workflows/sync-config.yml`.
* **1.2.2** Set trigger to: `on: push: branches: [main]`.
* **1.2.3** Add step to mirror GitHub `/config` and `/prompts` folders to `gs://bd-content-data/` via the `google-github-actions/upload-cloud-storage` action.

---

## PHASE 2 — Agent Prompt Engineering (3 hours)
*Your instructions to the AI employee, managed via Git.*

### 2.1 The Instruction Set
* **2.1.1** `prompts/01_research.md`: Web browsing protocols for BBS and World Bank data extraction.
* **2.1.2** `prompts/02_write.md`: Instructions for data-driven storytelling for a mass audience.
* **2.1.3** `prompts/03_factcheck.md`: "Skeptical verifier" persona instructions using `config/fact_check_protocols.md`.
* **2.1.4** `prompts/05_visual.md`: Prompt for generating Python code that produces on-brand charts.

---

## PHASE 3 — The Engine: Cloud Run Job (5 hours)
*Replacing local execution with a serverless, custom container.*



### 3.1 Dockerization
* **3.1.1** Create a `Dockerfile`:
    * Base: `python:3.11-slim`.
    * Install: `google-cloud-sdk`, `nodejs`, `npm`.
    * Install Gemini CLI: `npm install -g @google/gemini-cli`.
* **3.1.2** Create a script `engine.py` to:
    * Download current configs/prompts from GCS using the Cloud Storage Python SDK.
    * Run Gemini CLI stages in sequence.
    * Write all outputs (`research.md`, `draft.md`, `chart.png`) directly back to GCS.
* **3.1.3** Build and push image to **GCP Artifact Registry**.

### 3.2 Helper Scripts (GCP-Optimized)
* **3.2.1** Generate `scripts/gcs_utils.py`: Logic for uploading/downloading from buckets.
* **3.2.2** Generate `scripts/slack_notifier.py`: Logic to send GCS "Signed URLs" to Slack for human review.

---

## PHASE 4 — Orchestration & Review (2 hours)

### 4.1 Cloud Scheduler (The Daily Trigger)
* **4.1.1** Create Cloud Scheduler job: `pipeline-daily-cron`.
* **4.1.2** Set Schedule: `0 3 * * 1-5` (Mon-Fri 9:00 AM Bangladesh time).
* **4.1.3** Target: Cloud Run Job (Phase 3).

### 4.2 Human-in-the-Loop Review
* **4.2.1** Set up Slack to receive the package (Caption + Chart + Quality Scores).
* **4.2.2** Approval mechanism: Use Option A (GitHub Action manual trigger link) in the Slack message to authorize the final `publish_instagram.py` script.

---

## PHASE 5 — Testing & Launch (4 hours)

### 5.1 End-to-End Validation
* **5.1.1** Commit a change to `writing_style_profile.md` $\rightarrow$ Confirm GitHub Actions mirrors it to GCS.
* **5.1.2** Manually trigger the Cloud Run Job in the GCP Console.
* **5.1.3** Verify that outputs appear in `gs://bd-content-data/pipeline/` and a Slack notification is sent.
* **5.1.4** Run 1 "Dry Run" through to publication; then go live 🎉.

---

## 📊 Summary of Costs & Resources

| Service | Monthly Cost | Why? |
| :--- | :--- | :--- |
| **Cloud Run Jobs** | **$0.00** | Free tier covers infrequent (~20 min) daily runs. |
| **Cloud Storage** | **$0.00** | 5GB standard storage free tier; MD and PNG files are minimal. |
| **Cloud Scheduler** | **$0.00** | First 3 jobs per month are free. |
| **GitHub Actions** | **$0.00** | Mirroring configs takes seconds; well within the 2,000 min/month free limit. |
| **Gemini API** | **$0.00** | Provided via Enterprise work account. |
| **TOTAL** | **$0.00/mo** | **Fully capitalized on free-tier services.** |

---

Would you like me to generate the **Dockerfile** configuration or the **sync-config.yml** GitHub Action code to start Phase 1?