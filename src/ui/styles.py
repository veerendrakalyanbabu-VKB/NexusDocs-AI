"""Global futuristic theme styles for the Streamlit app."""

from __future__ import annotations

import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --cyan: #22d3ee;
            --violet: #a78bfa;
            --indigo: #6366f1;
            --emerald: #34d399;
            --pink: #f472b6;
            --text: #f8fafc;
            --muted: #94a3b8;
            --panel: rgba(10, 16, 32, 0.82);
        }

        .stApp {
            background:
                radial-gradient(ellipse 70% 55% at 15% -5%, rgba(99,102,241,0.22), transparent 55%),
                radial-gradient(ellipse 55% 45% at 95% 5%, rgba(34,211,238,0.14), transparent 50%),
                radial-gradient(ellipse 40% 35% at 50% 100%, rgba(244,114,182,0.10), transparent 55%),
                linear-gradient(180deg, #03050d 0%, #060a14 50%, #03050d 100%);
            font-family: "Space Grotesk", sans-serif;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
            background-size: 40px 40px;
            mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
            pointer-events: none;
            z-index: 0;
        }

        .block-container {
            padding-top: 0.75rem;
            padding-bottom: 1.25rem;
            max-width: 1440px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(6,10,22,0.98), rgba(4,7,16,0.99)) !important;
            border-right: 1px solid rgba(99,102,241,0.25) !important;
            box-shadow: 8px 0 32px rgba(0,0,0,0.35);
        }

        [data-testid="stSidebar"] h3 {
            background: linear-gradient(90deg, #fff, #c7d2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-shell {
            position: relative;
            overflow: hidden;
            border-radius: 24px;
            margin-bottom: 1rem;
            border: 1px solid rgba(99,102,241,0.35);
            background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(34,211,238,0.06)), var(--panel);
            box-shadow: 0 0 0 1px rgba(255,255,255,0.04) inset, 0 24px 48px rgba(0,0,0,0.35);
        }

        .hero-glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            pointer-events: none;
        }

        .hero-glow-1 {
            width: 280px; height: 280px;
            top: -120px; right: -40px;
            background: rgba(34,211,238,0.18);
            animation: float 8s ease-in-out infinite;
        }

        .hero-glow-2 {
            width: 200px; height: 200px;
            bottom: -80px; left: 10%;
            background: rgba(167,139,250,0.15);
            animation: float 10s ease-in-out infinite reverse;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(12px); }
        }

        .hero-inner { position: relative; padding: 1.5rem 1.75rem; z-index: 1; }

        .hero-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 0.85rem;
        }

        .hero-eyebrow {
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            border: 1px solid rgba(34,211,238,0.4);
            background: rgba(34,211,238,0.1);
            color: var(--cyan);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .hero-chip {
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(167,139,250,0.35);
            background: rgba(167,139,250,0.1);
            color: #ddd6fe;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .hero-title {
            margin: 0 0 0.6rem;
            font-size: clamp(2rem, 4vw, 2.75rem);
            font-weight: 700;
            line-height: 1.1;
            background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 35%, #22d3ee 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            margin: 0;
            max-width: 720px;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.6;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 1000px) {
            .stat-grid { grid-template-columns: repeat(3, 1fr); }
        }

        .stat-card {
            position: relative;
            overflow: hidden;
            padding: 1rem 1.1rem;
            border-radius: 18px;
            border: 1px solid rgba(148,163,184,0.14);
            background: var(--panel);
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-3px);
            border-color: rgba(99,102,241,0.45);
            box-shadow: 0 14px 32px rgba(99,102,241,0.15);
        }

        .stat-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--indigo), var(--cyan));
            opacity: 0.8;
        }

        .stat-icon {
            width: 8px; height: 8px;
            border-radius: 50%;
            margin-bottom: 0.5rem;
            box-shadow: 0 0 14px currentColor;
        }

        .stat-icon.files { background: #60a5fa; color: #60a5fa; }
        .stat-icon.chunks { background: var(--violet); color: var(--violet); }
        .stat-icon.depth { background: var(--cyan); color: var(--cyan); }
        .stat-icon.status { background: #fbbf24; color: #fbbf24; }
        .stat-icon.queries { background: var(--pink); color: var(--pink); }

        .stat-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 500;
            margin-bottom: 0.2rem;
        }

        .stat-value {
            color: var(--text);
            font-size: 1.7rem;
            font-weight: 700;
            line-height: 1.1;
        }

        .stat-value.ready { color: var(--emerald); }
        .stat-value.pending { color: #fbbf24; }

        .panel-shell {
            border-radius: 20px;
            border: 1px solid rgba(148,163,184,0.14);
            background: var(--panel);
            padding: 1rem 1.1rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 12px 28px rgba(0,0,0,0.2);
        }

        .panel-title {
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.85rem;
        }

        .pipeline-flow {
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            align-items: stretch;
        }

        .pipe-step-wrap {
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .pipe-step {
            min-width: 108px;
            padding: 0.7rem 0.75rem;
            border-radius: 14px;
            border: 1px solid rgba(148,163,184,0.14);
            background: rgba(8,12,24,0.65);
            transition: all 0.25s;
        }

        .pipe-step.complete {
            border-color: rgba(52,211,153,0.35);
            background: rgba(52,211,153,0.08);
        }

        .pipe-step.live {
            border-color: rgba(34,211,238,0.5);
            background: rgba(34,211,238,0.1);
            box-shadow: 0 0 24px rgba(34,211,238,0.2);
            animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 16px rgba(34,211,238,0.15); }
            50% { box-shadow: 0 0 28px rgba(34,211,238,0.35); }
        }

        .pipe-num {
            font-family: "JetBrains Mono", monospace;
            font-size: 0.68rem;
            color: var(--cyan);
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .pipe-label {
            color: #e2e8f0;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .pipe-desc {
            color: var(--muted);
            font-size: 0.68rem;
            margin-top: 0.15rem;
        }

        .pipe-line {
            width: 14px;
            height: 2px;
            background: linear-gradient(90deg, rgba(99,102,241,0.5), rgba(34,211,238,0.5));
            border-radius: 2px;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.55rem;
        }

        .insight-item {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
            padding: 0.65rem 0.75rem;
            border-radius: 12px;
            border: 1px solid rgba(148,163,184,0.1);
            background: rgba(8,12,24,0.5);
        }

        .insight-item span {
            color: var(--muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .insight-item strong {
            color: #e2e8f0;
            font-family: "JetBrains Mono", monospace;
            font-size: 0.8rem;
        }

        .chat-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding-bottom: 0.85rem;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid rgba(148,163,184,0.12);
        }

        .chat-title {
            color: var(--text);
            font-size: 1.1rem;
            font-weight: 600;
        }

        .chat-sub {
            color: var(--muted);
            font-size: 0.8rem;
            margin-top: 0.15rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 600;
            white-space: nowrap;
        }

        .status-pill.online {
            border: 1px solid rgba(52,211,153,0.4);
            background: rgba(52,211,153,0.1);
            color: var(--emerald);
        }

        .status-pill.offline {
            border: 1px solid rgba(251,191,36,0.4);
            background: rgba(251,191,36,0.1);
            color: #fbbf24;
        }

        .status-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 10px currentColor;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .welcome-shell {
            text-align: center;
            padding: 2rem 1.5rem;
            border-radius: 18px;
            border: 1px dashed rgba(99,102,241,0.4);
            background: linear-gradient(180deg, rgba(99,102,241,0.08), rgba(99,102,241,0.03));
            margin: 0.5rem 0 1rem;
        }

        .welcome-shell.ready {
            border-style: solid;
            border-color: rgba(52,211,153,0.35);
            background: linear-gradient(180deg, rgba(52,211,153,0.08), rgba(52,211,153,0.02));
        }

        .welcome-icon {
            font-size: 1.6rem;
            color: var(--cyan);
            margin-bottom: 0.5rem;
        }

        .welcome-shell h3 {
            color: var(--text);
            margin: 0 0 0.5rem;
            font-size: 1.1rem;
        }

        .welcome-shell p {
            color: var(--muted);
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .welcome-flow {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }

        .flow-step {
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            border: 1px solid rgba(99,102,241,0.3);
            background: rgba(99,102,241,0.1);
            color: #c7d2fe;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .flow-arrow { color: var(--muted); }

        .sidebar-progress {
            border: 1px solid rgba(99,102,241,0.25);
            border-radius: 14px;
            padding: 0.85rem;
            margin-bottom: 0.85rem;
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(34,211,238,0.05));
        }

        .sidebar-progress-label {
            display: flex;
            justify-content: space-between;
            color: #cbd5e1;
            font-size: 0.8rem;
            margin-bottom: 0.45rem;
        }

        .sidebar-progress-track {
            height: 8px;
            border-radius: 999px;
            background: rgba(148,163,184,0.15);
            overflow: hidden;
        }

        .sidebar-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--indigo), var(--cyan));
            box-shadow: 0 0 14px rgba(34,211,238,0.5);
        }

        .sidebar-progress-caption {
            margin-top: 0.4rem;
            color: var(--muted);
            font-size: 0.74rem;
        }

        .file-chip {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.7rem;
            border-radius: 10px;
            border: 1px solid rgba(148,163,184,0.14);
            background: rgba(8,12,24,0.55);
            color: #cbd5e1;
            font-size: 0.78rem;
            margin-bottom: 0.4rem;
            font-family: "JetBrains Mono", monospace;
        }

        .file-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--cyan);
            box-shadow: 0 0 8px var(--cyan);
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid rgba(99,102,241,0.22) !important;
            background: rgba(10,16,32,0.6) !important;
            border-radius: 18px !important;
            box-shadow: 0 12px 28px rgba(0,0,0,0.2) !important;
        }

        [data-testid="stChatMessage"] {
            border-radius: 16px !important;
            border: 1px solid rgba(148,163,184,0.12) !important;
            background: rgba(12,18,36,0.55) !important;
            margin-bottom: 0.65rem !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            border-color: rgba(99,102,241,0.3) !important;
            background: rgba(99,102,241,0.08) !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            border-color: rgba(34,211,238,0.25) !important;
            background: rgba(34,211,238,0.06) !important;
        }

        [data-testid="stChatInput"] {
            border-radius: 16px !important;
            border: 1px solid rgba(99,102,241,0.4) !important;
            background: rgba(6,10,22,0.92) !important;
            box-shadow: 0 0 32px rgba(99,102,241,0.15) !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1, #22d3ee) !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 24px rgba(99,102,241,0.35) !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
        }

        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 12px 28px rgba(99,102,241,0.45) !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            transition: transform 0.15s !important;
        }

        .stButton > button:hover:not(:disabled) {
            transform: translateY(-1px) !important;
        }

        [data-testid="stFileUploader"] section {
            border-radius: 14px !important;
            border: 1px dashed rgba(99,102,241,0.4) !important;
            background: rgba(99,102,241,0.06) !important;
        }

        [data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 1px solid rgba(148,163,184,0.14) !important;
            background: rgba(8,12,24,0.5) !important;
        }

        div[data-testid="stProgressBar"] > div {
            background: linear-gradient(90deg, #6366f1, #22d3ee) !important;
        }

        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )
