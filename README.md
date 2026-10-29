# NexusMind

NexusMind is a local-first autonomous research agent built for the Nebius x NVIDIA Global AI Hackathon. It allows users to run structured, multi-step research on complex questions while keeping their private notes and documents strictly on their local machine.

The application uses NVIDIA Nemotron models hosted on Nebius Token Factory for planning, document analysis, and report synthesis.

---

## Features

- **Local-First Privacy**: Uploaded reference files (`.txt`, `.md`, `.csv`, `.json`) are parsed directly in memory during the session and are never saved to an external database.
- **Autonomous Multi-Step Execution**: Instead of a single-turn prompt, the agent breaks the problem down into distinct phases:
  1. Task planning and question decomposition
  2. Local evidence analysis and cross-referencing
  3. Structured research report synthesis
- **Nebius Token Factory Integration**: Connects to Nebius OpenAI-compatible endpoints to run `nvidia/Llama-3.1-Nemotron-70B-Instruct-HF` and other Nemotron variants with high throughput.
- **Offline / Demo Mode**: Runs an interactive demonstration mode if an API key is not configured, allowing reviewers to test the workflow immediately.
- **Export**: One-click download of the generated report in Markdown.

---

## Setup & Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/Adityaaop/NexusMind.git
cd NexusMind
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key (Optional)
You can provide your Nebius API Key in any of the following ways:
- In the Streamlit sidebar input field when running the app.
- In a `.env` file (`NEBIUS_API_KEY=your_key_here`).
- In `.streamlit/secrets.toml`.

If left blank, the app will run in Demo Mode.

### 4. Start the app
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser. You can upload the included `sample_notes.txt` and pick a preset research goal to test the workflow right away.

---

## Project Structure

```text
NexusMind_Hackathon_Project/
├── app.py               # Streamlit application and agent workflow
├── requirements.txt     # Python dependencies
├── sample_notes.txt     # Sample test notes for local document ingestion
├── .env.example         # Example environment file
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
└── LICENSE              # MIT License
```

---

## Tech Stack

- **Frontend & App Framework**: Streamlit
- **Language**: Python 3.10+
- **Inference Infrastructure**: Nebius Token Factory (`https://api.studio.nebius.ai/v1/`)
- **Reasoning Models**: `nvidia/Llama-3.1-Nemotron-70B-Instruct-HF`, `nvidia/nemotron-4-340b-instruct`

---

## Hackathon Submission

- **Event**: Nebius x NVIDIA Global AI Hackathon
- **Track**: Best Apps and Agents / Personal AI
- **Author**: Aditya

---

## License

MIT License. See [LICENSE](LICENSE) for details.
