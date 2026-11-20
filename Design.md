# SecRAG --- Design

## Purpose

SecRAG is a cited security-knowledge assistant for questions about
vulnerabilities, weaknesses, attack techniques and web-application
risks. It retrieves evidence from public security sources, generates
answers grounded in that evidence, validates citations and refuses when
evidence is insufficient.

## Scope and data sources

The initial corpus is deliberately focused to fit local hardware
constraints. Raw files remain unchanged under `data/raw/`. Each source
directory has its own `metadata.json` for provenance.

  ----------------------------------------------------------------------------------------
  Source                  Dataset / scope         Current raw file(s)
  ----------------------- ----------------------- ----------------------------------------
  CISA                    Known Exploited         `known_exploited_vulnerabilities.json`
                          Vulnerabilities (KEV)   

  NVD                     Annual CVE feeds for    `nvdcve-2.0-2024.json`,
                          2024, 2025 and 2026;    `nvdcve-2.0-2025.json`,
                          filter by publication   `nvdcve-2.0-2026.json`
                          date during             
                          normalization           

  MITRE CWE               Comprehensive weakness  `2000.xml`
                          catalogue               

  MITRE ATT&CK            Enterprise ATT&CK, STIX `enterprise-attack-20.1.json`
                          2.1                     

  OWASP                   OWASP Top 10:2025       `OWASP Top Ten 2025.pdf`; HTML
                                                  reference: https://owasp.org/Top10/2025/
  ----------------------------------------------------------------------------------------

Record the exact source URL, version, download date, format and
filenames in each `metadata.json`. The NVD annual feeds include records
outside the intended two-year window; apply the publication-date filter
during Day 3 normalization. Preserve the original downloaded files
unchanged.

## Common document schema

Normalize source records into JSONL documents with this common schema:

`id`, `title`, `text`, `source`, `date`, `severity`

Retain useful source-specific identifiers, relationships, section
information and source URLs as metadata where available. Preserve
traceability to the original source.

## Architecture

**Offline indexing:** collect raw sources → parse and normalize →
validate records → chunk (one CVE per chunk; split longer documents by
section) → attach metadata → generate local embeddings with
`bge-small-en-v1.5` → store vectors in embedded Chroma; create a keyword
index with `rank_bm25`.

**Online answering:** user query → input/scope checks → extract
CVE/CWE/ATT&CK identifiers → BM25 and vector retrieval → Reciprocal Rank
Fusion (RRF) → local cross-encoder reranking (final top 5) → prompt the
LLM with retrieved content explicitly marked as untrusted data →
generate cited answer → validate citations against retrieved chunk IDs
and refuse when evidence is missing or insufficient.

## Technology choices

Python 3.x and the existing `secragenv`; hosted LLM behind the existing
`generate(prompt) -> str` interface; local `bge-small-en-v1.5`
embeddings; embedded Chroma; `rank_bm25`; a small local cross-encoder;
FastAPI; Streamlit; Docker; GitHub Actions CI. Keep provider-specific
code behind the existing LLM interface. The agreed baseline architecture
is frozen; do not add layers or technologies without discussing a
genuine blocker first.

## Evaluation and security

Create `eval/questions.jsonl` with at least 50 questions covering
exact-ID, conceptual, multi-hop and out-of-scope queries. Establish
ground-truth source IDs before examining system outputs. Measure
retrieval with hit-rate@k and MRR. Evaluate generated answers using
faithfulness, citation-valid percentage, injection-defense rate and
correct-refusal percentage on one frozen final LLM. Record model,
settings and date with every result. Test prompt injection in retrieved
content and treat retrieved text as untrusted data.

## Constraints and decisions

Target hardware: 8 GB RAM, GTX 1650 (4 GB VRAM), limited SSD. Keep the
NVD subset focused; run embeddings and reranking locally and use a
hosted LLM. Do not commit raw datasets, `.env`, cache files or virtual
environments. The secure code-review extension is outside the initial
20-day build.

  -----------------------------------------------------------------------
  Date                    Decision                Reason
  ----------------------- ----------------------- -----------------------
  2026-11-20              Keep raw datasets in    Keep source provenance
                          per-source folders with alongside the original
                          a separate              data.
                          `metadata.json` in      
                          each.                   

  2026-11-20              Collect NVD annual JSON Limit the corpus to the
                          feeds for 2024--2026    intended recent window
                          and filter by           without downloading all
                          publication date during historical NVD records.
                          normalization.          

  2026-11-20              Use Enterprise ATT&CK   Preserve structured
                          STIX 2.1 JSON and CWE   ATT&CK
                          XML.                    objects/relationships
                                                  and the CWE XML
                                                  content.
  -----------------------------------------------------------------------
