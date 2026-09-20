# Sheets-to-AI-Workflow Pipeline

An automated, open-source asynchronous backend pipeline built with **FastAPI** and **Google Workspace**. It ingests live customer entries from Google Forms/Sheets, dynamically generates tailored context using the **Gemini API**, and instantly dispatches professional email responses.

## 📂 Project Architecture

```text
LoopAI.3.1.2/
├── app/
│   ├── ai/          # Gemini API processing modules
│   ├── api/         # FastAPI web server routes
│   ├── email/       # Email formatting and delivery logic
│   └── gspreed/     # Google Sheets connection handlers
├── config/          # Logging and system configurations
└── .gitignore       # Protection for keys and system caches
```

## 🛠️ Local Installation & Credentials Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd sheets-to-ai-workflow-automated-system
   ```

2. **Google Cloud Service Account Setup:**
   To connect this application to your Google Sheets and Forms, you must generate a private service account key:
   * Go to the [Google Cloud Console](https://google.com).
   * Create a new project or select an existing one.
   * Navigate to **IAM & Admin > Service Accounts** and click **Create Service Account**.
   * Grant the service account the **Editor** role for your project.
   * Go to the **Keys** tab of your new service account, click **Add Key > Create New Key**, and choose **JSON**.
   * Download the JSON file, rename it exactly to `google_credentials.json`, and place it inside a folder named `credentials/` in your project root directory.

3. **Share Your Google Sheet:**
   Open your target Google Sheet in your web browser, click **Share**, and add the `client_email` address found inside your downloaded JSON file (`loopai-sheet-service@...`) as an **Editor**.

4. **Configure Environment Variables:**
   Create a `.env` file inside your project root and add your remaining secrets:
   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_app_password_here
   ```

5. **Launch the Server:**
   ```bash
   uvicorn app.api.loopserver:app --reload
   ```
