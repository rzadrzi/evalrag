# EvalRAG: Evaluation-Aware Retrieval-Augmented Generation System

EvalRAG is a **production-oriented Retrieval-Augmented Generation (RAG) system** with a built-in **evaluation framework**.  
It not only answers questions using your domain documents, but also **measures** how good those answers are in terms of:

- **Answer correctness**
- **Faithfulness to the retrieved context (hallucination detection)**
- **Context relevance (retrieval quality)**
- **System metrics** such as latency and cost

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the stack](#running-the-stack)
- [Usage](#usage)
  - [1. Ingest documents](#1-ingest-documents)
  - [2. Ask a question (RAG)](#2-ask-a-question-rag)
  - [3. Run offline evaluation](#3-run-offline-evaluation)
  - [4. View the dashboard](#4-view-the-dashboard)
- [Evaluation Details](#evaluation-details)
  - [Answer correctness](#answer-correctness)
  - [Faithfulness](#faithfulness)
  - [Context relevance](#context-relevance)
  - [System metrics](#system-metrics)
- [Data Formats](#data-formats)
  - [Documents](#documents)
  - [Evaluation dataset](#evaluation-dataset)
  - [Evaluation results](#evaluation-results)
- [Extending EvalRAG](#extending-evalrag)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

EvalRAG is designed for teams who want to move from *“We built a RAG demo”* to  
*“We know how well our RAG system actually performs.”*

Typical use cases:

- Internal knowledge bases (policies, regulations, manuals)
- Financial / legal / medical document QA
- Any domain where **hallucinations are unacceptable** and decisions require trust

EvalRAG provides:

- A **RAG API** (`/api/ask`) to answer user questions
- A **document ingestion pipeline** to index your corpus
- An **evaluation engine** that:
  - Runs a test set through your RAG pipeline
  - Uses an LLM-as-a-judge to rate answers and contexts
  - Stores metrics and results for analysis
- A **dashboard** to visualize quality, hallucination rate, and performance

---

## Key Features

- **RAG pipeline**
  - Chunk-based document ingestion
  - Vector search using a vector database
  - Configurable prompt templates
- **Evaluation-aware design**
  - Offline evaluation on curated test sets
  - LLM-as-a-judge scoring for:
    - Answer correctness
    - Faithfulness to context
    - Context relevance
- **Observability**
  - Logging of queries, contexts, answers, tokens, and latency
  - Dashboard with charts and tables
- **Configurable**
  - Pluggable embeddings and LLM providers
  - YAML-based configuration for prompts and thresholds
- **API-first**
  - REST API for ingestion, querying, and evaluation
  - Ready to be integrated into existing products or UIs

---

## Architecture

High-level architecture:

```text
                  +-----------------------+
                  |    Evaluation UI      |
                  |  (Dashboard / Charts) |
                  +-----------+-----------+
                              |
                              v
+-----------------------------+------------------------------+
|                        Backend API                         |
|                         (FastAPI)                          |
|                                                            |
|  +----------------+    +----------------+   +------------+ |
|  |  RAG Service   |    |  Eval Engine   |   |  Ingestion | |
|  | /api/ask       |    | /api/eval/run  |   | /api/docs  | |
|  +--------+-------+    +--------+-------+   +------+-----+ |
|           |                     |                  |       |
+-----------+---------------------+------------------+-------+
            |                     |                  |
            v                     v                  v
   +----------------+    +----------------+   +--------------+
   |  Vector Store  |    |  Relational DB |   | Object Store |
   | (e.g. Qdrant)  |    |  (e.g. Postgres)|  |  (optional)  |
   +----------------+    +----------------+   +--------------+

