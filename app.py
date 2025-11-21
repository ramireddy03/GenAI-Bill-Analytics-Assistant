import streamlit as st
import os
from google import genai
from google.genai import types
import json
import pandas as pd
import io

# --- 1. CONFIGURATION AND INITIALIZATION ---

# Set Streamlit page configuration
st.set_page_config(page_title="💰 GenAI Bill Analytics Assistant", layout="wide")
st.title("💰 GenAI Bill Analytics Assistant")
st.markdown("Upload a bill image to extract structured data and query the information.")

# Initialize the Gemini Client using the secret key defined in .streamlit/secrets.toml
try:
    # Uses the key defined as GEMINI_API_KEY in the secrets.toml file
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("Error: 'GEMINI_API_KEY' not found in Streamlit secrets. "
             "Please check your .streamlit/secrets.toml file.")
    st.stop()
except Exception as e:
    st.error(f"Error initializing Gemini client: {e}")
    st.stop()

# Define the structured output schema for the bill data (Requirement 2 & 5)
BILL_SCHEMA = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string", "description": "The unique invoice or bill number."},
        "invoice_date": {"type": "string", "description": "The date the bill was issued (e.g., DD/MM/YYYY)."},
        "seller_name": {"type": "string", "description": "The name of the company or seller who issued the bill."},
        "customer_name": {"type": "string", "description": "The name of the customer the bill is addressed to (Bill To)."},
        "grand_total": {"type": "number", "description": "The final total amount paid."},
        "currency": {"type": "string", "description": "The currency of the grand total (e.g., INR, USD)."},
        "items": {
            "type": "array",
            "description": "A list of all individual products or services purchased.",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Product or service description/title."},
                    "quantity": {"type": "integer", "description": "Number of units purchased."},
                    "unit_price": {"type": "number", "description": "Price per unit before any discount/tax."},
                    "total_amount": {"type": "number", "description": "Final total amount for this item."}
                },
                "required": ["description", "quantity", "total_amount"]
            }
        }
    },
    "required": ["invoice_number", "invoice_date", "seller_name", "grand_total", "items"]
}

# Initialize session state for persistent data (chat history and parsed bill)
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Please upload a bill image to begin analysis."}]
if "parsed_data" not in st.session_state:
    st.session_state["parsed_data"] = None


# --- 2. CORE FUNCTIONS ---

@st.cache_data(show_spinner=False)
def parse_bill_with_gemini(uploaded_file, schema):
    """Uses Gemini to perform structured data extraction from an image."""
    try:
        # Read the file content and convert to a Part object for Gemini
        image_bytes = uploaded_file.read()
        image = types.Part.from_bytes(
            data=image_bytes,
            mime_type=uploaded_file.type
        )
        
        prompt = (
            "You are an expert bill parser. Analyze the uploaded bill image and extract "
            "all the required information. Strictly adhere to the provided JSON schema."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            )
        )
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error during bill parsing: {e}")
        return None

def chit_chat_and_query(extracted_data, user_query):
    """Handles conversational interactions and bill-specific queries (Requirement 1 & 4)."""
    
    # Context for the model
    bill_context = json.dumps(extracted_data, indent=2)
    
    # System Instruction grounds the model's response to the extracted data
    system_instruction = (
        "You are an AI Bill Analyst. Your main goal is to answer questions about the provided JSON bill data, "
        "and also engage in friendly chit-chat. When asked about the bill, use *only* the data below. "
        "If the question is conversational, respond normally."
        f"\n\n--- BILL DATA START ---\n{bill_context}\n--- BILL DATA END---\n\n"
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[user_query],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return response.text
    except Exception as e:
        return f"An error occurred while generating the response: {e}"


# --- 3. STREAMLIT UI LAYOUT AND LOGIC ---

# --- Sidebar: File Upload Section ---
uploaded_file = st.sidebar.file_uploader("Upload Bill Image", type=["jpg", "jpeg", "png"])

if uploaded_file and (st.session_state["parsed_data"] is None or uploaded_file.file_id != st.session_state.get("file_id")):
    st.sidebar.info("Analyzing bill, please wait...")
    
    # Reset state for new file
    st.session_state["parsed_data"] = None 
    st.session_state["file_id"] = uploaded_file.file_id 
    
    # Call the parsing function
    with st.spinner("Extracting structured data from image..."):
        parsed_json = parse_bill_with_gemini(uploaded_file, BILL_SCHEMA)
    
    if parsed_json:
        st.session_state["parsed_data"] = parsed_json
        st.session_state["messages"].append({"role": "assistant", "content": f"✅ Bill from **{parsed_json.get('seller_name', 'Unknown Seller')}** successfully parsed! You can now query the data or export it."})
        st.sidebar.success("Bill successfully analyzed!")
    else:
        st.sidebar.error("Failed to parse bill. Please try a different image.")
        st.session_state["file_id"] = None

# --- Main Content Area ---
col1, col2 = st.columns([1, 1])

# Column 1: Display Extracted Data & Export (Requirement 3)
with col1:
    st.header("Extracted Structured Data")
    if st.session_state["parsed_data"]:
        data = st.session_state["parsed_data"]
        
        # Display key fields
        st.subheader("Key Information")
        st.json({k: data[k] for k in data if k != 'items'}, expanded=True)
        
        # Display Items in a table
        if data.get('items'):
            st.subheader("Line Items")
            df = pd.DataFrame(data['items'])
            # Format numbers
            for col in ['unit_price', 'total_amount']:
                 if col in df.columns:
                     df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
            
            st.dataframe(df, use_container_width=True)
        
        # Data Export
        st.subheader("Data Export")
        json_string = json.dumps(data, indent=2)
        st.download_button(
            label="Download Data as JSON",
            data=json_string,
            file_name=f"{data.get('invoice_number', 'extracted')}_bill_data.json",
            mime="application/json",
            help="Click to save the extracted structured data."
        )
    else:
        st.info("Upload a bill image in the sidebar to view the extracted structured data.")

# Column 2: Chit-Chat & Information Querying
with col2:
    st.header("Ask Questions about the Bill")
    
    # Display previous messages
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question (e.g., 'What is the grand total?', 'What did I buy?', 'Say hello'):"):
        
        # Add user message to history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        with st.spinner("Thinking..."):
            if st.session_state["parsed_data"]:
                response = chit_chat_and_query(st.session_state["parsed_data"], prompt)
            else:
                # Basic chit-chat if no bill is uploaded
                response = chit_chat_and_query({}, prompt)
                
        # Add assistant response to history
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.rerun() # Refresh the chat window