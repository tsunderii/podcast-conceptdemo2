# UI.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from typing import List, Dict, Any, Tuple
from RAG import CareerAdviceRAG  # assuming your RAG backend is still the same

def run_ui():
    # -------------------------
    # Page config + CSS
    # -------------------------
    st.set_page_config(page_title="💼 Career Explorer", layout="wide")
    st.markdown(
        """
        <style>
        body {background-color: #ffffff; color: #1f2937; font-family: 'Helvetica', sans-serif;}
        .card { background: #f3f4f6; padding: 12px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 10px;}
        .pod-title { font-weight:600; color: #065f46; margin-bottom:6px; }
        .muted { color:#4b5563; font-size:14px; }
        .header { font-size:28px; font-weight:700; color:#065f46; margin-bottom:20px;}
        .stButton>button {background-color:#10b981; color:white; border-radius:8px; padding:8px 16px;}
        .stButton>button:hover {background-color:#059669; color:white;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # Initialize RAG system if not already
    # -------------------------
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = CareerAdviceRAG(
            st.secrets["PINECONE_API_KEY"],
            st.secrets["GOOGLE_API_KEY"]
        )

    # -------------------------
    # Session state defaults
    # -------------------------
    st.session_state.setdefault("saved_answers", [])
    st.session_state.setdefault("recent_queries", [])

    # -------------------------
    # Helper functions
    # -------------------------
    def generate_summary(query: str) -> str:
        if not query.strip():
            return ""
        return f"✨ Summary for '{query}': Focus on continuous learning, networking, and practical experience."

    def fetch_podcast_relevance(query: str) -> Tuple[List[Dict[str, str]], pd.DataFrame]:
        podcasts = [
            {"title": "Career Chat", "description": "Insights from top professionals.", "image_url": "https://via.placeholder.com/150"},
            {"title": "Tech Talks", "description": "Latest trends in tech careers.", "image_url": "https://via.placeholder.com/150"},
            {"title": "Job Journey", "description": "Advice for career growth.", "image_url": "https://via.placeholder.com/150"},
        ]
        concepts = ["Networking", "Learning", "Experience"]
        freq = [random.randint(1, 10) for _ in concepts]
        df = pd.DataFrame({"Concept": concepts, "Frequency": freq})
        return podcasts, df

    def plot_concept_frequency(df: pd.DataFrame):
        fig, ax = plt.subplots()
        ax.bar(df['Concept'], df['Frequency'], color='#a7f3d0')
        ax.set_xlabel("Concepts")
        ax.set_ylabel("Frequency")
        ax.set_title("Concept Frequency Across Podcasts")
        for i, v in enumerate(df['Frequency']):
            ax.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
        st.pyplot(fig)

    def render_podcast_cards(podcasts: List[Dict[str, str]]):
        cols = st.columns(3)
        for col, pod in zip(cols, podcasts):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.image(pod["image_url"], use_container_width=True)
                st.markdown(f'<div class="pod-title">{pod["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="muted">{pod["description"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    def save_answer(query: str, summary: str):
        st.session_state.saved_answers.append({"query": query, "summary": summary})
        st.success("✅ Answer saved!")

    def display_saved_library():
        if st.session_state.saved_answers:
            with st.expander("📚 Saved Answers"):
                for ans in st.session_state.saved_answers:
                    st.markdown(f"**Query:** {ans['query']}")
                    st.write(f"**Summary:** {ans['summary']}")
        else:
            st.info("No saved answers yet.")

    # -------------------------
    # Main page
    # -------------------------
    st.markdown('<div class="header">💼 Career Proof-of-Work Explorer</div>', unsafe_allow_html=True)
    st.write("Ask a career-related question below and discover insights, concept frequencies, and top podcasts.")

    query = st.text_input("✏️ Enter your career question here:")

    if st.button("🔍 Run Analysis"):
        if not query.strip():
            st.error("Please enter a valid question.")
        else:
            st.session_state.recent_queries.append(query)

            # Generate summary
            summary = generate_summary(query)
            st.subheader("🔹 Summarized Answer")
            st.write(summary)

            # Fetch podcasts & concept frequency
            podcasts, df = fetch_podcast_relevance(query)

            # Display graph
            st.subheader("📊 Concept Frequency Graph")
            plot_concept_frequency(df)

            # Display podcasts
            st.subheader("🎧 Top Podcasts")
            render_podcast_cards(podcasts)

            # Save button
            if st.button("💾 Save This Answer"):
                save_answer(query, summary)

    # Display saved library
    display_saved_library()
