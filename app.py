import os
import time
import requests
import streamlit as st

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def get_api_key():
    if os.getenv("NEBIUS_API_KEY"):
        return os.getenv("NEBIUS_API_KEY")
    try:
        if hasattr(st, "secrets") and "NEBIUS_API_KEY" in st.secrets:
            return st.secrets["NEBIUS_API_KEY"]
    except Exception:
        pass
    return ""

st.set_page_config(
    page_title="NexusMind",
    page_icon="🧠",
    layout="wide"
)

# Sidebar setup
st.sidebar.title("NexusMind")
st.sidebar.caption("Local-first research with Nebius + NVIDIA Nemotron")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(
    "Nebius API Key",
    value=get_api_key(),
    type="password",
    help="Enter your Nebius Token Factory API key. Leave blank to run in offline demo mode."
)

api_endpoint = st.sidebar.selectbox(
    "Endpoint",
    [
        "https://api.studio.nebius.ai/v1/chat/completions",
        "https://api.tokenfactory.nebius.com/v1/chat/completions"
    ]
)

model = st.sidebar.selectbox(
    "Model",
    [
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
        "nvidia/nemotron-4-340b-instruct",
        "nvidia/nemotron-mini-4b-instruct"
    ]
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.6, 0.05)

st.sidebar.markdown("---")
st.sidebar.caption("Files uploaded in this session are processed in memory and never saved to a database.")

def call_model(prompt, system_prompt="You are a helpful research assistant.", model_name=model, temp=temperature, key=api_key, url=api_endpoint):
    # If no API key is provided, generate a sensible offline response based on the prompt
    if not key or not key.strip() or "your_" in key.lower():
        time.sleep(1.0)
        if "plan" in prompt.lower() or "break down" in prompt.lower():
            return (
                "1. **Core Problem Definition**: Identify the main thesis, background context, and key questions to answer.\n"
                "2. **Evidence Analysis**: Review available documents, literature, and data points for supporting and counter-arguments.\n"
                "3. **Synthesis & Takeaways**: Summarize findings, outline practical implications, and draw conclusions."
            )
        else:
            return (
                f"### Research Report: {prompt[:80].strip()}...\n\n"
                f"*(Generated in Demo Mode using {model_name})*\n\n"
                "#### Overview\n"
                f"This research topic focuses on: \"{prompt[:120].strip()}...\". "
                "The analysis evaluated key objectives, trade-offs, and practical implementations.\n\n"
                "#### Key Findings\n"
                "- **System Design**: Splitting research tasks into discrete planning, analysis, and synthesis phases provides much more structured outputs than single-turn queries.\n"
                "- **Privacy & Local Context**: Processing source documents locally before querying an LLM preserves privacy and keeps token usage focused on relevant context.\n"
                "- **Model Performance**: Running NVIDIA Nemotron via Nebius serverless endpoints offers strong instruction adherence for technical and analytical writing.\n\n"
                "#### Trade-offs & Considerations\n"
                "- Larger models (70B/340B) excel at nuanced reasoning but take slightly longer per generation than 4B/8B variants.\n"
                "- Quality of the synthesis is heavily guided by how clean and targeted the input notes are.\n\n"
                "#### Recommendations\n"
                "1. Use a fast model for text cleanup and outline drafting, then Nemotron-70B for the final synthesized report.\n"
                "2. Keep research notes organized in Markdown or text files for optimal local parsing.\n\n"
                "*(To run live queries against Nebius, enter your API key in the sidebar.)*"
            )

    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temp,
        "max_tokens": 2048
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError:
        return f"Nebius API error ({r.status_code}): {r.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"

# Main layout
top_left, top_right = st.columns([4, 1])
with top_left:
    st.title("NexusMind")
    st.write("Local-first autonomous research agent powered by NVIDIA Nemotron on Nebius Token Factory.")
with top_right:
    if api_key:
        st.success("API Connected")
    else:
        st.info("Demo Mode")

st.write("---")

st.subheader("1. Reference Files (Optional)")
uploaded_files = st.file_uploader(
    "Upload research notes or papers (.txt, .md, .csv, .json) — or try 'sample_notes.txt':",
    type=["txt", "md", "csv", "json"],
    accept_multiple_files=True
)

file_context = ""
if uploaded_files:
    texts = []
    for f in uploaded_files:
        try:
            content = f.read().decode("utf-8", errors="ignore")
            texts.append(f"Source file: {f.name}\n{content[:2500]}")
        except Exception as err:
            texts.append(f"Error reading {f.name}: {err}")
    file_context = "\n\n".join(texts)
    st.caption(f"Loaded {len(uploaded_files)} file(s) into memory.")

st.subheader("2. Research Goal")

preset_options = [
    "Write your own query...",
    "Compare using open-weight NVIDIA Nemotron models on Nebius Token Factory vs closed APIs for autonomous agents.",
    "Evaluate latency and cost trade-offs between local inference on Apple Silicon vs Nebius cloud endpoints for 70B models."
]
selected_preset = st.selectbox("Sample topic presets:", preset_options)
preset_text = "" if selected_preset == "Write your own query..." else selected_preset

goal = st.text_area(
    "What topic or question are you researching?",
    value=preset_text,
    placeholder="e.g. Compare using open-weight NVIDIA Nemotron models on Nebius Token Factory vs closed APIs for agent workflows.",
    height=100
)

if st.button("Start Research", type="primary"):
    if not goal.strip():
        st.warning("Please enter a research goal first.")
    else:
        start = time.time()
        with st.status("Running research agent...", expanded=True) as status:
            st.write("Step 1: Planning investigation steps...")
            plan_prompt = f"Break down this research goal into 3 clear investigative steps:\n\nGoal: {goal}"
            plan = call_model(plan_prompt, system_prompt="You are a research planning assistant. Provide a concise, clear 3-step outline.")
            st.markdown(plan)

            st.write("Step 2: Analyzing reference context...")
            time.sleep(0.8)
            if file_context:
                st.write(f"Analyzed {len(uploaded_files)} uploaded document(s).")
            else:
                st.write("No files uploaded; proceeding with general research knowledge.")

            st.write("Step 3: Synthesizing final report...")
            synthesis_prompt = f"""Research Goal:
{goal}

Outline:
{plan}

Uploaded Notes:
{file_context if file_context else "None provided."}

Please write a clear, well-structured research report covering:
1. Executive Summary
2. Key Findings & Analysis
3. Trade-offs and Risks
4. Practical Recommendations
5. Conclusion
"""
            report = call_model(synthesis_prompt, system_prompt="You are an objective research analyst. Write a clean, thorough report in markdown.")
            
            elapsed = time.time() - start
            status.update(label=f"Completed in {elapsed:.1f}s", state="complete", expanded=False)

        st.markdown("---")
        st.subheader("Research Report")
        st.markdown(report)

        st.download_button(
            label="Download Report (.md)",
            data=report,
            file_name="research_report.md",
            mime="text/markdown"
        )
