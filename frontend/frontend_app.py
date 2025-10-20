# --- Imports ---
import streamlit as st
import pandas as pd
import altair as alt
import requests
from io import BytesIO

# --- Configuration ---
# This is the URL where your FastAPI backend will be running.
BACKEND_API_URL = "http://127.0.0.1:8000/api/v1/parse"

# --- Page Configuration ---
st.set_page_config(
    page_title="IntelliStatement Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
# Ensures the app remembers state between user interactions.
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'upload'
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# --- Main App Layout ---
st.title("📄 IntelliStatement: The Intelligent Bank Statement Analyzer")
st.markdown("---")

# =================================================================================================
# STEP 1: UPLOAD VIEW
# =================================================================================================
if st.session_state.current_step == 'upload':
    st.header("Step 1: Upload Your Bank Statement")
    
    # File uploader widget.
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, PNG, JPG)", 
        type=['pdf', 'png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )

    if uploaded_file:
        # When a file is uploaded, show the "Analyze" button.
        if st.button(f"Analyze '{uploaded_file.name}'", type="primary", use_container_width=True):
            st.session_state.current_step = 'processing'
            # Store file in memory to pass to the processing step.
            st.session_state.uploaded_file_bytes = uploaded_file.getvalue()
            st.session_state.uploaded_file_name = uploaded_file.name
            st.rerun()

# =================================================================================================
# STEP 2: PROCESSING VIEW
# =================================================================================================
elif st.session_state.current_step == 'processing':
    st.header("Analyzing Document...")
    with st.spinner("Please wait... The AI is processing your document. This may take a moment."):
        try:
            # Prepare the file for the API request.
            files = {'file': (st.session_state.uploaded_file_name, st.session_state.uploaded_file_bytes)}
            
            # Make the POST request to the FastAPI backend.
            response = requests.post(BACKEND_API_URL, files=files, timeout=120) # 2-minute timeout
            
            # Check if the request was successful.
            if response.status_code == 200:
                extracted_data = response.json()
                st.session_state.extracted_data = extracted_data
                
                # Create and store the DataFrame in session state for easy use.
                st.session_state.df = pd.DataFrame(extracted_data.get('transactions', []))
                
                st.session_state.current_step = 'display'
                st.rerun()
            else:
                # Handle backend errors.
                st.error(f"Error from backend: {response.status_code} - {response.text}")
                st.session_state.current_step = 'upload'

        except requests.exceptions.RequestException as e:
            # Handle network or connection errors.
            st.error(f"Could not connect to the backend service. Please ensure it is running. Error: {e}")
            st.session_state.current_step = 'upload'

# =================================================================================================
# STEP 3: DATA DISPLAY AND INTERACTION VIEW
# =================================================================================================
elif st.session_state.current_step == 'display':
    
    # Retrieve data from session state.
    data = st.session_state.extracted_data
    summary = data.get('summary', {})
    df = st.session_state.df

    st.header("Step 2: Review and Interact with Your Data")

    # --- Account Details Display ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Account Holder", value=data.get('account_holder', 'N/A'))
    with col2:
        st.metric(label="Account Number", value=data.get('account_number', 'N/A'))
    st.info(f"🧾 Statement Period: **{data.get('period_start', 'N/A')}** to **{data.get('period_end', 'N/A')}**")
    
    st.markdown("---")

    # --- Automatic Data Integrity Verification ---
    st.subheader("✅ Data Integrity Verification")
    if summary.get('is_consistent', False):
        st.success(f"Verification Successful! The transactions correctly add up. Calculated End Balance: ${summary.get('calculated_balance', 0):,.2f}")
    else:
        st.warning("Verification Mismatch. The calculated balance does not match the statement's ending balance. Please review the transactions for potential OCR errors.")

    st.markdown("---")

    # --- Tabbed Layout for Organization ---
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Transactions", "📤 Export"])

    with tab1:
        # --- Financial Dashboard Tab ---
        st.subheader("Financial Dashboard")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        summary_col1.metric("Beginning Balance", f"${data.get('beginning_balance', 0):,.2f}")
        summary_col2.metric("Total Deposits (Credits)", f"${summary.get('total_credits', 0):,.2f}")
        summary_col3.metric("Total Withdrawals (Debits)", f"${summary.get('total_debits', 0):,.2f}")
        summary_col4.metric("Ending Balance", f"${data.get('ending_balance', 0):,.2f}")

        # --- Income vs. Expenses Bar Chart ---
        st.subheader("Income vs. Expenses")
        chart_data = pd.DataFrame({
            "Category": ["Total Credits", "Total Debits"],
            "Amount": [summary.get('total_credits', 0), summary.get('total_debits', 0)],
            "Color": ["#4CAF50", "#F44336"] # Green for credits, Red for debits
        })
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', title=None),
            y=alt.Y('Amount', title='Amount ($)', axis=alt.Axis(format='$,.0f')),
            color=alt.Color('Color', scale=None)
        )
        st.altair_chart(chart, use_container_width=True)

    with tab2:
        # --- Interactive Transactions Tab ---
        st.subheader("Explore Transactions")
        
        filter_col1, filter_col2 = st.columns([3, 1])
        with filter_col1:
            search_query = st.text_input("Search Description", placeholder="e.g., Amazon, Morrisons Petrol...")
        with filter_col2:
            transaction_type = st.selectbox("Filter by Type", ["All", "Debits", "Credits"])

        # Apply filters to the dataframe.
        filtered_df = df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df['description'].str.contains(search_query, case=False, na=False)]
        if transaction_type == "Debits":
            filtered_df = filtered_df[filtered_df['debit'] > 0]
        elif transaction_type == "Credits":
            filtered_df = filtered_df[filtered_df['credit'] > 0]
        
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        st.write(f"Showing {len(filtered_df)} of {len(df)} total transactions.")

    with tab3:
        # --- Data Export Tab ---
        st.subheader("Export Your Data")
        st.write("The exported file will contain the transactions currently displayed in the 'Transactions' tab (including any filters you've applied).")
        
        export_df = filtered_df.copy()

        export_col1, export_col2 = st.columns(2)
        with export_col1:
            csv_buffer = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export as CSV", data=csv_buffer, file_name='statement_export.csv',
                mime='text/csv', use_container_width=True
            )
        with export_col2:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False, sheet_name='Transactions')
            st.download_button(
                label="📗 Export as Excel", data=excel_buffer.getvalue(), file_name='statement_export.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', use_container_width=True
            )

    st.markdown("---")
    
    # --- Reset Button ---
    if st.button("Upload Another Statement"):
        # Reset session state for a new upload.
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()