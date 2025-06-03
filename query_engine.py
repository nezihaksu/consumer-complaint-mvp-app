import duckdb
import polars as pl
from pathlib import Path
import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

nltk.download('punkt_tab')

class ComplaintIngestor:
    def __init__(self, filepath: str, table_name: str = "complaints"):
        self.filepath = Path(filepath)
        self.table_name = table_name
        self.con = duckdb.connect()

    def load_selected_columns(self, columns: list[str]) -> pl.DataFrame:
        query = f"""
            SELECT {', '.join([f'"{col}"' for col in columns])}
            FROM read_csv_auto('{self.filepath.as_posix()}', AUTO_DETECT=TRUE)
            WHERE "Consumer complaint narrative" IS NOT NULL
        """
        df = self.con.execute(query).df()
        return pl.from_pandas(df)

    def chunk_narratives(self, df: pl.DataFrame, max_sentences: int = 5, overlap: int = 1) -> list[dict]:
        chunks = []
        for row in df.iter_rows(named=True):
            narrative = row.get("Consumer complaint narrative", "")
            if not isinstance(narrative, str):
                continue
            sentences = sent_tokenize(narrative)
            i = 0
            while i < len(sentences):
                chunk_sents = sentences[i:i + max_sentences]
                chunk_text = " ".join(chunk_sents)
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "Complaint ID": row.get("Complaint ID"),
                        "Product": row.get("Product"),
                        "Company": row.get("Company"),
                        "State": row.get("State"),
                        "Date received": row.get("Date received")
                    }
                })
                i += max_sentences - overlap
        return chunks

    def generate_insights(self, df: pl.DataFrame):
        df_pd = df.to_pandas()
        most_common_products = df_pd['Product'].value_counts().head(10)
        most_common_companies = df_pd['Company'].value_counts().head(10)
        return most_common_products, most_common_companies

    def plot_heatmap(self, df: pl.DataFrame, output_path: str):
        df_pd = df.to_pandas()
        pivot = pd.pivot_table(df_pd, index='Product', columns='State', values='Complaint ID', aggfunc='count', fill_value=0)
        plt.figure(figsize=(16, 8))
        sns.heatmap(pivot, cmap="YlGnBu")
        plt.title("Complaints Heatmap by Product and State")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
