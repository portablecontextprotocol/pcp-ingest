# Episode Rewrite Plan

## Goal

- Extract structured snippets from documents using the LLM (via `snippet_extractor.py`).
- Convert each snippet into a `RawEpisode` for ingestion into the graph database.
- Chain these steps in `app.py` for a clean, minimal, and modular workflow.

---

## Task Checklist

### 1. Snippet Extraction ([snippet_extractor.py])

- [x] Ensure `format_document(content, config)` returns a list of `Snippet` objects.

### 2. Episode Generation ([episode_generation.py])

- [x] Implement `generate_episodes_from_snippets(snippets)` to convert a list of `Snippet` objects to `RawEpisode` objects.
- [x] Map fields:
  - `name` ← `snippet.title`
  - `content` ← `snippet.description` (+ code, language, mentions, etc. as needed)
  - `source_description` ← `snippet.source` or formatted string
  - `source` ← `EpisodeType.json`
  - `reference_time` ← `datetime.now(timezone.utc)`

### 3. Chaining in [app.py]

- [x] Refactor to:
  - [x] Call `format_document` to extract snippets from each document
  - [x] Call `generate_episodes_from_snippets` to convert snippets to episodes
  - [x] Ingest each `RawEpisode` into the graph

### 4. Minimal Code Changes

- [ ] Confirm no unnecessary changes in `snippet_extractor.py`
- [ ] Refactor `episode_generation.py` to accept snippets and output episodes
- [ ] Refactor `app.py` to orchestrate the new workflow

### 5. Extensibility

- [ ] Ensure modularity for easy swapping of extraction/mapping logic

### 6. Example Pseudocode

- [x] (This plan includes pseudocode for reference)

### 7. Testing

- [ ] Add unit test: Given a sample snippet, does it produce the expected RawEpisode?
- [ ] Add integration test: Given a document, does it end up in the graph as expected?

---

## Example Pseudocode

```python
# app.py
snippets = await format_document(content, config)
episodes = generate_episodes_from_snippets(snippets)
for episode in episodes:
    await graphiti.add_episode(...)
```

---

**Mark each checkbox as you complete the corresponding step!**
