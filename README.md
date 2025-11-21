GenAI Bill Analytics Assistant

A Streamlit-based application that extracts structured data from bill/invoice images using Google Gemini, and allows users to query the bill through a conversational chat interface.

🚀 Overview

This application solves the problem of manually reading and entering information from invoices.
It allows users to:

✔️ Upload a bill image (JPG/PNG)
✔️ Automatically extract structured fields like invoice number, seller, items, total, etc.
✔️ View extracted information in JSON & table format
✔️ Download the structured data
✔️ Ask natural language questions about the bill
✔️ Engage in chit-chat (hybrid conversational assistant)

The solution is powered by Gemini 2.5 Flash, with a strict JSON schema to guarantee consistent extraction.

🧠 Why This Approach?
1️⃣ Use of LLM (Gemini) for Vision + Extraction

Gemini models are extremely good at reading complex documents (unstructured data) and converting them into structured formats.

Instead of writing manual OCR logic, rule-based text parsing, or regex pipelines (which fail for different bill formats), an LLM:

Understands layout + content

Extracts fields robustly

Works without training

Supports multi-format invoices

2️⃣ Structured JSON Schema Enforcement

Without a schema, LLMs may produce inconsistent JSON.
By giving a strict response_schema, we ensure:

Correct data types

Required fields

Extracted list of items

Predictable output structure

This is essential for downstream analytics / export.

3️⃣ Using Streamlit for UI

Streamlit provides:

Fast development

File uploader component

Chat interface

DataFrames for displaying line-items

Download button support

It makes the app interactively usable within minutes.

4️⃣ Chat-based Querying

After extraction, users can ask questions such as:

"What is the grand total?"

"Who is the seller?"

"List all purchased items."

This is achieved by embedding the extracted JSON data inside a system instruction, ensuring the model answers only from bill data, while still supporting chit-chat.

5️⃣ Session State Management

Session-state tracks:

Chat history

Parsed bill data

File ID (so a new upload triggers re-parsing)

This ensures smooth user experience without reloading everything.

🛠️ Features
📤 1. Upload Bill Image

Upload JPG/PNG invoices from the sidebar.

🧾 2. Automatic Structured Extraction

Fields extracted include:

Invoice number

Invoice date

Seller & customer

Currency

Grand total

List of purchased items (desc, qty, price, amount)

📑 3. Display Structured Output

Key values shown in JSON

Items shown in a DataFrame

Auto-formatting of numerical fields

###⬇️ 4. Export to JSON
A single click downloads the extracted structured data.

💬 5. Smart Chat Interface

Ask anything about the bill or casually chat.

🧩 Architecture & Flow
User Uploads Image
        ↓
Streamlit sends image → Gemini API
        ↓
Gemini parses image using JSON schema
        ↓
Output stored in session_state
        ↓
Displayed to the user (JSON + Table)
        ↓
User asks questions about the bill
        ↓
System instruction embeds JSON context
        ↓
Gemini answers using bill data

📦 Tech Stack
Component	Purpose
Streamlit	UI & interaction
Google Gemini 2.5 Flash	Vision + structured extraction + chat
Pandas	Tabular display of line-items
JSON Schema	Enforcing consistent LLM outputs
📁 Project Setup
1. Install dependencies
pip install streamlit google-genai pandas

2. Add your API key

Create a file:

.streamlit/secrets.toml


Inside it:

GEMINI_API_KEY = "your_api_key_here"

3. Run the app
streamlit run app.py

📜 Summary of the Approach (Simple Explanation)

How it works:

You upload a bill → the app sends it to Gemini.

Gemini reads the bill and extracts clean structured info following a strict schema.

The app shows the extracted data and lets you download it.

You can chat with the AI to ask questions about the bill.

Why this approach:

LLMs can understand diverse bill layouts better than OCR + rules.

JSON schema ensures consistent, high-quality extraction.

Streamlit enables rapid, interactive UI development.

Conversational interface improves usability & insights.
