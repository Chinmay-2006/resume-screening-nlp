import streamlit as st
import pandas as pd
from extractor import extract_text
from similarity import compute_final_score
from preprocessing import clean_for_wordcloud
from resume_quality import check_completeness, check_readability
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk

@st.cache_resource
def download_nltk_data():
    resources = ["punkt", "punkt_tab", "stopwords", "wordnet",
                 "averaged_perceptron_tagger", "maxent_ne_chunker", "words"]
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

download_nltk_data()
st.set_page_config(page_title="Resume Screening System", layout="wide")

st.title("📄 NLP-Based Resume Screening System")
st.write("Upload a Job Description and multiple resumes to rank candidates based on skill match and content similarity.")

# --- Sidebar ---
with st.sidebar:
    st.header("ℹ️ How it works")
    st.write("""
    1. Upload a Job Description
    2. Upload one or more resumes
    3. Click Analyze
    4. View ranked candidates below
    """)

    st.divider()
    st.subheader("📐 How scores are calculated")

    with st.expander("Skill Match %"):
        st.write("""
        We compare a predefined list of technical skills against both 
        the Job Description and the resume text (using whole-word 
        matching, e.g. "java" won't match inside "javascript").
        
        **Formula:**
        `(Matched Skills ÷ Total Skills Required by JD) × 100`
        """)

    with st.expander("TF-IDF Similarity %"):
        st.write("""
        Measures **exact word overlap** between resume and JD using 
        TF-IDF vectors + Cosine Similarity. Only catches matches when 
        the same words are used in both documents.
        """)

    with st.expander("Semantic Similarity %"):
        st.write("""
        Uses spaCy word embeddings to measure **meaning-based** similarity — 
        catches related concepts even when different words are used 
        (e.g., "backend developer" ≈ "server-side engineer").
        """)

    with st.expander("Combined Final Score"):
        st.write("""
        **Formula:**
        `(Skill Match % × 0.6) + (Content Similarity % × 0.4)`
        
        where Content Similarity = average of TF-IDF and Semantic Similarity.
        
        **Exception:** If the Job Description doesn't mention any 
        specific technical skills, we rely fully on Content Similarity instead.
        """)

    with st.expander("Resume Completeness %"):
        st.write("""
        Checks whether standard resume sections are present: 
        Education, Skills, Experience/Projects, and Contact Info.
        """)

    with st.expander("Readability Score"):
        st.write("""
        Uses the Flesch Reading Ease formula to estimate how easy 
        the resume is to read, based on sentence length and word complexity.
        Higher score = easier to read.
        """)

# --- File Uploaders ---
col1, col2 = st.columns(2)

with col1:
    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])

with col2:
    resume_files = st.file_uploader(
        "Upload Resumes (you can select multiple)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

# --- Analyze Button ---
if st.button("🔍 Analyze"):
    if not jd_file or not resume_files:
        st.warning("Please upload both a Job Description and at least one resume.")
    else:
        with st.spinner("Analyzing resumes... this may take a few seconds"):
            jd_text = extract_text(jd_file)
            results = []

            for resume in resume_files:
                resume_text = extract_text(resume)
                result = compute_final_score(resume_text, jd_text)
                result["filename"] = resume.name
                result["resume_text"] = resume_text
                results.append(result)

            results.sort(key=lambda x: x["final_score"], reverse=True)

        st.success("Analysis complete!")

        if any(r.get("note") for r in results):
            st.info(results[0]["note"])

        st.subheader("📊 Ranked Results")

        # Summary table
        table_data = [
            {
                "Rank": i + 1,
                "Candidate": r["filename"],
                "Final Score (%)": r["final_score"],
                "Skill Match (%)": r["skill_match_pct"],
                "TF-IDF Similarity (%)": r["tfidf_score"],
                "Semantic Similarity (%)": r["semantic_score"]
            }
            for i, r in enumerate(results)
        ]
        df = pd.DataFrame(table_data)
        st.table(df)

        # Bar chart comparison
        st.subheader("📈 Score Comparison")
        chart_df = df.set_index("Candidate")[["Final Score (%)", "Skill Match (%)", "TF-IDF Similarity (%)", "Semantic Similarity (%)"]]
        st.bar_chart(chart_df)

        # Download as CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Results as CSV", csv, "resume_screening_results.csv", "text/csv")

        # Top candidate highlight
        top = results[0]
        st.success(f"🏆 Top Candidate: **{top['filename']}** with a Final Score of **{top['final_score']}%**")

        # Detailed per-candidate breakdown
        st.subheader("🔎 Candidate Details")
        for i, r in enumerate(results):
            label = f"#{i+1} — {r['filename']} (Final Score: {r['final_score']}%)"
            if i == 0:
                label = "🏆 " + label
            with st.expander(label):
                st.write(f"**Matched Skills:** {', '.join(r['matched_skills']) if r['matched_skills'] else 'None'}")
                st.write(f"**Missing Skills:** {', '.join(r['missing_skills']) if r['missing_skills'] else 'None'}")
                st.write(f"**TF-IDF Similarity:** {r['tfidf_score']}% | **Semantic Similarity:** {r['semantic_score']}%")

                # Resume completeness check
                completeness = check_completeness(r["resume_text"])
                st.write(f"**Resume Completeness:** {completeness['completeness_pct']}%")
                missing_sections = [sec for sec, present in completeness["sections"].items() if not present]
                if missing_sections:
                    st.write(f"⚠️ Missing sections: {', '.join(missing_sections)}")

                # Readability
                readability = check_readability(r["resume_text"])
                st.write(f"**Readability:** {readability['level']} (Flesch score: {readability['score']})")

                # Word cloud
                cleaned_for_cloud = clean_for_wordcloud(r["resume_text"])
                if cleaned_for_cloud.strip():
                    wc = WordCloud(
                        width=1000,
                        height=500,
                        background_color="white",
                        max_words=60,
                        collocations=False,
                        prefer_horizontal=0.9,
                        margin=10
                    ).generate(cleaned_for_cloud)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)