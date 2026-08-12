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
            --panel: rgba(10, 16, 32, 0.88);
        }

        .stApp {
            background:
                radial-gradient(ellipse 70% 55% at 15% -5%, rgba(99,102,241,0.24), transparent 55%),
                radial-gradient(ellipse 55% 45% at 95% 5%, rgba(34,211,238,0.16), transparent 50%),
                radial-gradient(ellipse 40% 35% at 50% 100%, rgba(244,114,182,0.12), transparent 55%),
                linear-gradient(180deg, #02040a 0%, #060a14 50%, #02040a 100%);
            font-family: "Space Grotesk", sans-serif;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(99,102,241,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99,102,241,0.035) 1px, transparent 1px);
            background-size: 44px 44px;
            mask-image: radial-gradient(ellipse at center, black 25%, transparent 78%);
            pointer-events: none;
            z-index: 0;
        }

        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            max-width: 1480px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(5,8,18,0.99), rgba(3,6,14,0.99)) !important;
            border-right: 1px solid rgba(99,102,241,0.28) !important;
            box-shadow: 10px 0 40px rgba(0,0,0,0.4);
        }

        [data-testid="stSidebar"] h3 {
            background: linear-gradient(90deg, #fff, #c7d2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* ── Hero ── */
        .hero-shell {
            position: relative;
            overflow: hidden;
            border-radius: 26px;
            margin-bottom: 1rem;
            border: 1px solid rgba(99,102,241,0.38);
            background: linear-gradient(135deg, rgba(99,102,241,0.16), rgba(34,211,238,0.07)), var(--panel);
            box-shadow: 0 0 0 1px rgba(255,255,255,0.05) inset, 0 28px 56px rgba(0,0,0,0.4);
        }

        .hero-glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(70px);
            pointer-events: none;
        }

        .hero-glow-1 { width: 320px; height: 320px; top: -140px; right: -60px; background: rgba(34,211,238,0.2); animation: float 9s ease-in-out infinite; }
        .hero-glow-2 { width: 240px; height: 240px; bottom: -90px; left: 8%; background: rgba(167,139,250,0.18); animation: float 11s ease-in-out infinite reverse; }
        .hero-glow-3 { width: 180px; height: 180px; top: 40%; right: 30%; background: rgba(244,114,182,0.1); animation: float 13s ease-in-out infinite; }

        @keyframes float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(14px) scale(1.03); }
        }

        .hero-inner { position: relative; padding: 1.75rem 2rem; z-index: 1; }

        .hero-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }

        .hero-brand { display: flex; align-items: center; gap: 0.6rem; }

        .hero-logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px; height: 32px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--indigo), var(--cyan));
            color: white;
            font-size: 0.9rem;
            box-shadow: 0 0 20px rgba(99,102,241,0.5);
        }

        .hero-eyebrow {
            color: var(--cyan);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero-chips { display: flex; gap: 0.5rem; flex-wrap: wrap; }

        .hero-chip {
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 600;
        }

        .chip-engine {
            border: 1px solid rgba(167,139,250,0.4);
            background: rgba(167,139,250,0.12);
            color: #ddd6fe;
        }

        .chip-model {
            border: 1px solid rgba(34,211,238,0.35);
            background: rgba(34,211,238,0.1);
            color: var(--cyan);
            font-family: "JetBrains Mono", monospace;
        }

        .hero-title {
            margin: 0 0 0.75rem;
            font-size: clamp(2.1rem, 4.5vw, 3rem);
            font-weight: 700;
            line-height: 1.08;
            color: #ffffff;
        }

        .hero-accent {
            background: linear-gradient(135deg, #e0e7ff 0%, #22d3ee 60%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            margin: 0 0 1.1rem;
            max-width: 680px;
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.65;
        }

        .hero-tags { display: flex; gap: 0.45rem; flex-wrap: wrap; }

        .hero-tag {
            padding: 0.28rem 0.7rem;
            border-radius: 8px;
            border: 1px solid rgba(148,163,184,0.18);
            background: rgba(8,12,24,0.6);
            color: #cbd5e1;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.04em;
        }

        /* ── Stats ── */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 1100px) { .stat-grid { grid-template-columns: repeat(3, 1fr); } }
        @media (max-width: 640px) { .stat-grid { grid-template-columns: repeat(2, 1fr); } }

        .stat-card {
            position: relative;
            overflow: hidden;
            padding: 1.05rem 1.15rem;
            border-radius: 18px;
            border: 1px solid rgba(148,163,184,0.14);
            background: var(--panel);
            transition: transform 0.22s, box-shadow 0.22s, border-color 0.22s;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(99,102,241,0.5);
            box-shadow: 0 16px 36px rgba(99,102,241,0.18);
        }

        .stat-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--indigo), var(--cyan));
            opacity: 0.85;
        }

        .stat-icon { width: 8px; height: 8px; border-radius: 50%; margin-bottom: 0.55rem; box-shadow: 0 0 16px currentColor; }
        .stat-icon.files { background: #60a5fa; color: #60a5fa; }
        .stat-icon.chunks { background: var(--violet); color: var(--violet); }
        .stat-icon.depth { background: var(--cyan); color: var(--cyan); }
        .stat-icon.status { background: #fbbf24; color: #fbbf24; }
        .stat-icon.queries { background: var(--pink); color: var(--pink); }

        .stat-label { color: var(--muted); font-size: 0.76rem; font-weight: 500; margin-bottom: 0.25rem; }
        .stat-value { color: var(--text); font-size: 1.75rem; font-weight: 700; line-height: 1.1; }
        .stat-value.ready { color: var(--emerald); }
        .stat-value.pending { color: #fbbf24; }

        /* ── Panels ── */
        .panel-shell {
            border-radius: 20px;
            border: 1px solid rgba(148,163,184,0.14);
            background: var(--panel);
            padding: 1rem 1.15rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 14px 32px rgba(0,0,0,0.22);
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.85rem;
            flex-wrap: wrap;
        }

        .panel-title {
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .panel-badge {
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            border: 1px solid rgba(52,211,153,0.3);
            background: rgba(52,211,153,0.08);
            color: var(--emerald);
            font-size: 0.68rem;
            font-weight: 600;
        }

        .actions-hint {
            color: var(--muted);
            font-size: 0.82rem;
            margin: -0.5rem 0 0.75rem;
        }

        /* ── Pipeline ── */
        .pipeline-flow {
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            align-items: stretch;
        }

        .pipe-step-wrap { display: flex; align-items: center; gap: 0.35rem; }

        .pipe-step {
            min-width: 100px;
            padding: 0.7rem 0.75rem;
            border-radius: 14px;
            border: 1px solid rgba(148,163,184,0.14);
            background: rgba(8,12,24,0.65);
            transition: all 0.25s;
        }

        .pipe-step.complete { border-color: rgba(52,211,153,0.38); background: rgba(52,211,153,0.09); }
        .pipe-step.live {
            border-color: rgba(34,211,238,0.55);
            background: rgba(34,211,238,0.11);
            box-shadow: 0 0 28px rgba(34,211,238,0.22);
            animation: glow 2.2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 18px rgba(34,211,238,0.15); }
            50% { box-shadow: 0 0 32px rgba(34,211,238,0.38); }
        }

        .pipe-num { font-family: "JetBrains Mono", monospace; font-size: 0.66rem; color: var(--cyan); font-weight: 700; margin-bottom: 0.2rem; }
        .pipe-label { color: #e2e8f0; font-size: 0.8rem; font-weight: 600; }
        .pipe-desc { color: var(--muted); font-size: 0.66rem; margin-top: 0.15rem; }
        .pipe-line { width: 12px; height: 2px; background: linear-gradient(90deg, rgba(99,102,241,0.5), rgba(34,211,238,0.5)); border-radius: 2px; }

        /* ── Insights ── */
        .insight-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.55rem; }

        .insight-item {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
            padding: 0.7rem 0.8rem;
            border-radius: 12px;
            border: 1px solid rgba(148,163,184,0.1);
            background: rgba(8,12,24,0.55);
            transition: border-color 0.2s;
        }

        .insight-item:hover { border-color: rgba(99,102,241,0.35); }
        .insight-item span { color: var(--muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; }
        .insight-item strong { color: #e2e8f0; font-family: "JetBrains Mono", monospace; font-size: 0.78rem; }

        /* ── Chat ── */
        .chat-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding-bottom: 0.85rem;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid rgba(148,163,184,0.12);
        }

        .chat-title { color: var(--text); font-size: 1.12rem; font-weight: 600; }
        .chat-sub { color: var(--muted); font-size: 0.8rem; margin-top: 0.15rem; }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.85rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 600;
            white-space: nowrap;
        }

        .status-pill.online { border: 1px solid rgba(52,211,153,0.42); background: rgba(52,211,153,0.1); color: var(--emerald); }
        .status-pill.offline { border: 1px solid rgba(251,191,36,0.42); background: rgba(251,191,36,0.1); color: #fbbf24; }

        .status-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 10px currentColor;
            animation: pulse 2s infinite;
        }

        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.45; } }

        /* ── Welcome ── */
        .welcome-shell {
            text-align: center;
            padding: 2.25rem 1.75rem;
            border-radius: 20px;
            border: 1px dashed rgba(99,102,241,0.42);
            background: linear-gradient(180deg, rgba(99,102,241,0.09), rgba(99,102,241,0.03));
            margin: 0.5rem 0 1rem;
        }

        .welcome-shell.partial {
            border-style: dashed;
            border-color: rgba(251,191,36,0.4);
            background: linear-gradient(180deg, rgba(251,191,36,0.08), rgba(251,191,36,0.02));
        }

        .welcome-shell.ready {
            border-style: solid;
            border-color: rgba(52,211,153,0.38);
            background: linear-gradient(180deg, rgba(52,211,153,0.09), rgba(52,211,153,0.02));
        }

        .welcome-icon-ring {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 56px; height: 56px;
            border-radius: 50%;
            border: 1px solid rgba(99,102,241,0.4);
            background: rgba(99,102,241,0.1);
            margin-bottom: 0.75rem;
        }

        .welcome-icon-ring.ready {
            border-color: rgba(52,211,153,0.4);
            background: rgba(52,211,153,0.1);
        }

        .welcome-icon { font-size: 1.4rem; color: var(--cyan); }
        .welcome-shell.ready .welcome-icon { color: var(--emerald); }

        .welcome-shell h3 { color: var(--text); margin: 0 0 0.55rem; font-size: 1.15rem; }
        .welcome-shell p { color: var(--muted); margin: 0; font-size: 0.9rem; line-height: 1.6; }

        .welcome-tip {
            margin-top: 1rem !important;
            font-size: 0.82rem !important;
            color: #64748b !important;
        }

        .welcome-flow {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.45rem;
            margin-top: 1.1rem;
            flex-wrap: wrap;
        }

        .flow-step {
            padding: 0.38rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(99,102,241,0.32);
            background: rgba(99,102,241,0.1);
            color: #c7d2fe;
            font-size: 0.76rem;
            font-weight: 600;
        }

        .flow-arrow { color: var(--muted); font-size: 0.85rem; }

        /* ── Sidebar progress ── */
        .sidebar-progress {
            border: 1px solid rgba(99,102,241,0.28);
            border-radius: 16px;
            padding: 0.9rem;
            margin-bottom: 0.85rem;
            background: linear-gradient(135deg, rgba(99,102,241,0.11), rgba(34,211,238,0.05));
        }

        .sidebar-progress-label { display: flex; justify-content: space-between; color: #cbd5e1; font-size: 0.8rem; margin-bottom: 0.45rem; }
        .sidebar-progress-track { height: 8px; border-radius: 999px; background: rgba(148,163,184,0.15); overflow: hidden; }
        .sidebar-progress-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--indigo), var(--cyan)); box-shadow: 0 0 16px rgba(34,211,238,0.55); transition: width 0.4s ease; }
        .sidebar-progress-caption { margin-top: 0.42rem; color: var(--muted); font-size: 0.74rem; }

        /* ── File library ── */
        .file-chip {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.55rem 0.75rem;
            border-radius: 12px;
            border: 1px solid rgba(148,163,184,0.14);
            background: rgba(8,12,24,0.55);
            margin-bottom: 0.35rem;
            transition: border-color 0.2s;
        }

        .file-chip:hover { border-color: rgba(99,102,241,0.35); }

        .file-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 8px var(--cyan); flex-shrink: 0; }
        .file-name { color: #e2e8f0; font-size: 0.78rem; font-family: "JetBrains Mono", monospace; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .file-meta { color: var(--muted); font-size: 0.68rem; white-space: nowrap; }

        /* ── Footer ── */
        .app-footer {
            margin-top: 1.5rem;
            padding: 1rem 0 0.5rem;
            border-top: 1px solid rgba(148,163,184,0.1);
        }

        .footer-inner {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.6rem;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.78rem;
        }

        .footer-brand {
            color: #c7d2fe;
            font-weight: 600;
            background: linear-gradient(90deg, #c7d2fe, var(--cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .footer-divider { opacity: 0.4; }

        /* ── Streamlit overrides ── */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid rgba(99,102,241,0.24) !important;
            background: rgba(10,16,32,0.65) !important;
            border-radius: 20px !important;
            box-shadow: 0 14px 32px rgba(0,0,0,0.22) !important;
        }

        [data-testid="stChatMessage"] {
            border-radius: 16px !important;
            border: 1px solid rgba(148,163,184,0.12) !important;
            background: rgba(12,18,36,0.58) !important;
            margin-bottom: 0.7rem !important;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            border-color: rgba(99,102,241,0.32) !important;
            background: rgba(99,102,241,0.09) !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            border-color: rgba(34,211,238,0.28) !important;
            background: rgba(34,211,238,0.07) !important;
        }

        [data-testid="stChatInput"] {
            border-radius: 16px !important;
            border: 1px solid rgba(99,102,241,0.42) !important;
            background: rgba(6,10,22,0.94) !important;
            box-shadow: 0 0 36px rgba(99,102,241,0.16) !important;
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(34,211,238,0.55) !important;
            box-shadow: 0 0 40px rgba(34,211,238,0.2) !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1, #22d3ee) !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 26px rgba(99,102,241,0.38) !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
        }

        .stButton > button[kind="primary"]:hover:not(:disabled) {
            transform: translateY(-2px) !important;
            box-shadow: 0 14px 32px rgba(99,102,241,0.48) !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
        }

        .stButton > button:hover:not(:disabled) { transform: translateY(-1px) !important; }

        [data-testid="stFileUploader"] section {
            border-radius: 14px !important;
            border: 1px dashed rgba(99,102,241,0.42) !important;
            background: rgba(99,102,241,0.07) !important;
            transition: border-color 0.2s, background 0.2s !important;
        }

        [data-testid="stFileUploader"] section:hover {
            border-color: rgba(34,211,238,0.5) !important;
            background: rgba(34,211,238,0.06) !important;
        }

        [data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 1px solid rgba(148,163,184,0.14) !important;
            background: rgba(8,12,24,0.52) !important;
        }

        div[data-testid="stProgressBar"] > div {
            background: linear-gradient(90deg, #6366f1, #22d3ee) !important;
        }

        [data-testid="stStatusWidget"] {
            border-radius: 14px !important;
            border: 1px solid rgba(99,102,241,0.3) !important;
        }

        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )
