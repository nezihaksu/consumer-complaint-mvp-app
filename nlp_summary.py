def summarize_narratives(chunks: list[dict]) -> list[str]:
    # Placeholder mock summarization function
    summaries = []
    for chunk in chunks:
        text = chunk["text"]
        summary = text[:200] + ("..." if len(text) > 200 else "")
        summaries.append(summary)
    return summaries
