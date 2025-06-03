import streamlit as st
import polars as pl
from query_engine import ComplaintIngestor
from nlp_summary import summarize_narratives
from report_export import generate_report

st.title("Consumer Complaint Explorer")

columns = [
    "Complaint ID", "Product", "Sub-product", "Issue",
    "Company", "State", "Date received", "Consumer complaint narrative"
]
ingestor = ComplaintIngestor("data/consumer_complaints.csv")
df = ingestor.load_selected_columns(columns)

st.subheader("📊 Data Overview")
st.dataframe(df.head(50))

if st.button("Generate Report"):
    products, companies = ingestor.generate_insights(df)
    heatmap_path = "output/heatmap.png"
    ingestor.plot_heatmap(df, heatmap_path)
    generate_report(products, companies, heatmap_path)
    with open("output/report.pdf", "rb") as f:
        st.download_button("Download PDF Report", f, file_name="summary_report.pdf")

st.subheader("🧠 Narrative Summary (First 10)")
chunks = ingestor.chunk_narratives(df[:10])
summaries = summarize_narratives(chunks)
for s in summaries:
    st.write(f"- {s}")
