# GenAI Bill Analytics Assistant

A Streamlit-based application that extracts **structured data** from
bill/invoice images using **Google Gemini**, and allows users to **query
the bill** through a conversational chat interface.

------------------------------------------------------------------------

## Overview

This application solves the problem of manually reading and entering
information from invoices. It enables users to:

-   Upload a bill image (JPG/PNG)
-   Automatically extract structured fields like invoice number, seller,
    items, and grand total
-   View extracted information in JSON and table format
-   Download the structured data
-   Ask natural language questions about the bill
-   Engage in friendly chit-chat

------------------------------------------------------------------------

##  Why This Approach?

### 1. LLM (Gemini) for Vision + Extraction

Traditional OCR + rule-based parsing fails across different invoice
formats. Gemini understands layout, patterns, and semantics, making
extraction **robust, accurate, and universal**.

### 2. Enforced JSON Schema

To avoid inconsistent or invalid outputs, a strict `response_schema` is
used. This ensures predictable extraction with correct data types and
required fields.

### 3. Streamlit for UI

Streamlit provides an easy-to-use interface enabling fast development
of: - File upload - Chat interface - Dataframe rendering - JSON export

### 4. Chat-based Querying

Users can ask: - "What is the total?" - "List all purchased
items."

A custom **system instruction** ensures answers come **only from
extracted JSON data**, while still supporting chit-chat.

------------------------------------------------------------------------

##  Features

### 📤 Upload Bill Image

Supports JPG/PNG images.

### 🧾 Structured Data Extraction

Extracted fields: - Invoice number - Invoice date - Seller name -
Customer name - Currency - Grand total - Items (description, quantity,
unit price, amount)

### 📑 Display Output

-   JSON format
-   Table view for items
-   Auto-format numerical fields

### ⬇️ Export to JSON

One-click download.

### 💬 AI Chat

Ask questions about the bill or general conversations.

------------------------------------------------------------------------

## 🔧 Setup

### 1. Install Dependencies

``` bash
pip install streamlit google-genai pandas
```

### 2. Add API Key

Create `.streamlit/secrets.toml`:

    GEMINI_API_KEY = "your_api_key"

### 3. Run App

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## 📜 Summary

**How it Works** 1. User uploads invoice → Gemini extracts structured
data 2. Data validated via JSON schema 3. UI displays structured output
4. User can query details via chat

**Why This Approach** - LLMs are superior to OCR for varied invoice
formats - JSON schema maintains consistency - Streamlit enables rapid UI
development - Chat interface improves usability
