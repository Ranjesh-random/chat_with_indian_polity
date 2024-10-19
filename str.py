import streamlit as st
from app import rag_chain  # Import rag_chain directly from app.py

# Streamlit app setup
st.set_page_config(page_title="CHAT WITH INDIAN POLITY", page_icon="📖", layout="centered")
st.title("📖 Chat with Indian Polity")

# Use columns for a cleaner layout
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<h2 style='font-size: 35px;'>Enter Your Question:</h2>", unsafe_allow_html=True)

# Center the page content
st.markdown(
    """
    <style>
    .centered-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# User input field
user_query = st.text_input("Enter your question:", placeholder="Ask about the content of Indian polity...")

# Process the user's query
if user_query:
    with st.spinner("Generating answer..."):  # Show spinner while the response is generated
        try:
            response = rag_chain.invoke(user_query)
            if response:
                st.success(f"**Answer**: {response}")
                
                # Feedback and comment section below the answer
                with st.container():  # This keeps everything in the main body of the app, below the answer
                    st.write("### Feedback")
                    
                    # Like and Dislike buttons in a row
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("👍 Like"):
                            st.success("Thank you for your feedback!")
                    with col2:
                        if st.button("👎 Dislike"):
                            st.warning("We're sorry to hear that. Please let us know how we can improve.")

                    # Comment section
                    comment = st.text_area("Leave a comment about the answer:")
                    if st.button("Submit Comment"):
                        if comment:
                            st.success("Thank you for your comment!")
                        else:
                            st.warning("Please enter a comment before submitting.")
            else:
                st.warning("Sorry, no relevant information found.")
        except Exception as e:
            st.error(f"Error processing the question: {e}")

# Align everything to the center
st.markdown(
    """
    <style>
    .stButton>button {
        display: block;
        margin: 0 auto;
    }
    .stTextArea>label {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
