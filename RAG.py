# RAG.py
import random
import pandas as pd
from typing import List, Dict, Any, Tuple
import streamlit as st
import matplotlib.pyplot as plt

class CareerAdviceRAG:
    def __init__(self, pinecone_api_key: str, google_api_key: str):
        self.PINECONE_API_KEY = pinecone_api_key
        self.GOOGLE_API_KEY = google_api_key
        self.saved_answers: List[Dict[str, Any]] = []
        self.conversation_history: List[Dict[str, str]] = []

    # -------------------------
    # Core functions
    # -------------------------
    def generate_summary(self, query: str) -> str:
        if not query.strip():
            return ""
        return f"🔹 Insight Summary for '{query}': Focus on continuous learning, networking, and practical experience 🌿."

    def fetch_podcast_relevance(self, query: str) -> Tuple[List[Dict[str, str]], pd.DataFrame]:
        podcasts = [
            {"title": "Career Chat", "description": "Insights from top professionals.", "image_url": "https://via.placeholder.com/200"},
            {"title": "Tech Talks", "description": "Latest trends in tech careers.", "image_url": "https://via.placeholder.com/200"},
            {"title": "Job Journey", "description": "Advice for career growth.", "image_url": "https://via.placeholder.com/200"},
        ]
        concepts = ["Networking", "Learning", "Experience"]
        freq = [random.randint(1, 10) for _ in concepts]
        df = pd.DataFrame({"concept": concepts, "frequency": freq})
        return podcasts, df

    def plot_concept_frequency(self, df: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(df['concept'], df['frequency'], color=['#A3C9A8','#C2B280','#8F9779'])  # greens and browns
        ax.set_xlabel("Concepts")
        ax.set_ylabel("Frequency")
        ax.set_title("Concept Frequency Across Podcasts", fontsize=16, color="#556b2f")
        for i, v in enumerate(df['frequency']):
            ax.text(i, v + 0.3, str(v), ha='center', fontweight='bold', color="#4b6330")
        st.pyplot(fig, use_container_width=True)

    def render_podcast_cards(self, podcasts: List[Dict[str, str]]):
        cols = st.columns(3)
        for col, pod in zip(cols, podcasts):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.image(pod["image_url"], use_container_width=True)
                st.markdown(f'<div class="pod-title">{pod["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="muted">{pod["description"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    def save_answer(self, query: str, summary: str):
        self.saved_answers.append({"query": query, "summary": summary})
        st.success("Answer saved! ✅")

    def display_saved_library(self):
        if self.saved_answers:
            with st.expander("📚 Saved Insights"):
                for ans in self.saved_answers:
                    st.markdown(f"**Query:** {ans['query']}")
                    st.write(f"**Summary:** {ans['summary']}")
        else:
            st.info("No saved insights yet 🌿")
