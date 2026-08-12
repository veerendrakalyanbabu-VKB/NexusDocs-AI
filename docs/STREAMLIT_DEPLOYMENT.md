# Deploy Project 2 to Streamlit Community Cloud

Free hosting for your NexusDocs AI portfolio demo.

## One-click deploy

1. Open this link (logs you into Streamlit with GitHub):

   **[Deploy on Streamlit Cloud](https://share.streamlit.io/deploy?repository=veerendrakalyanbabu-VKB/AI-Document-QA-Assistant&branch=main&mainModule=app.py)**

2. Set an **App URL** (example: `nexusdocs-ai` → `https://nexusdocs-ai.streamlit.app`)

3. Under **Advanced settings → Secrets**, paste:

   ```toml
   OPENAI_API_KEY = "sk-your-openai-key"
   OPENAI_MODEL = "gpt-4o-mini"
   ```

   > OpenAI is recommended on Streamlit Cloud. The local FLAN-T5 model is too heavy for the free tier.

4. Click **Deploy** and wait 5–10 minutes for the first build.

5. Copy your live URL and add it to the README **Live Demo** badge.

## After deployment

Your live app will look like:

```text
https://YOUR-APP-NAME.streamlit.app
```

Update `README.md`:

```markdown
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://YOUR-APP-NAME.streamlit.app)
```

## Demo flow for visitors

1. Click **Demo** in the sidebar
2. Click **Build knowledge base**
3. Ask: *"Which file formats are supported?"*
4. Expand **Sources** to show citations

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails / out of memory | Add `OPENAI_API_KEY` in Secrets (avoids loading FLAN-T5) |
| App crashes on first question | Wait for embedding model download, then retry |
| Upload fails | Keep files under 200 MB |

## Local vs cloud

| | Local | Streamlit Cloud |
|---|-------|-----------------|
| LLM | FLAN-T5 or OpenAI | OpenAI (recommended) |
| Storage | `data/` folder | Ephemeral (re-index each session) |
| Cost | Free | Free |

For persistent cloud storage, use a separate GCP project (Portfolio Project #3).
