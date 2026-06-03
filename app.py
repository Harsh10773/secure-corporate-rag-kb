import streamlit as st
import os
from rag_backend import query_rag, process_new_pdf

# Configure the page aesthetics
st.set_page_config(page_title="Corporate AI Assistant", page_icon="💼", layout="centered")

st.title("Secure Corporate Knowledge Base")
st.markdown(
    "Ask questions about internal policies, HR manuals, or legal documents. **All data remains strictly on-premise.**")

# --- Sidebar for File Upload ---
with st.sidebar:
    st.header("📄 Document Management")
    st.markdown("Upload a new PDF to replace the current knowledge base.")

    uploaded_file = st.file_uploader("Upload a PDF policy", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Indexing document... This may take a moment."):
                # 1. Save the uploaded file to the local data directory
                file_path = os.path.join("data", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 2. Process the new PDF and rebuild the database
                chunk_count = process_new_pdf(uploaded_file.name)

                # 3. Notify the user and clear old chat history
                st.success(f"Success! Indexed {chunk_count} chunks from {uploaded_file.name}.")
                st.session_state.messages = []

# --- Chat Interface ---
# Initialize the chat history in the browser's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages when the app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Wait for user input at the bottom of the screen
if user_query := st.chat_input("E.g., What is the policy on maternity leave?"):

    # 1. Display the user's question
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Show a loading spinner while the local AI thinks
    with st.chat_message("assistant"):
        with st.spinner("Searching proprietary documents..."):

            # 3. Call your RAG backend function
            answer, pages = query_rag(user_query)

            # 4. Format and display the final answer
            if pages:
                formatted_response = f"{answer}\n\n*Sources: Page(s) {pages}*"
            else:
                formatted_response = answer

            st.markdown(formatted_response)

            # 5. Save the AI's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": formatted_response})