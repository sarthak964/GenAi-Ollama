import streamlit as st
import ollama

# --- App Configuration ---
st.set_page_config(page_title="Multi-Model Assistant", page_icon="⚡")

st.title("⚡ Fast Multi-Model Assistant")
st.markdown("Enter your question below. The AI will draft, review, and refine the answer behind the scenes.")


# --- 1. OPTIMIZATION: Model Warm-up Function ---
@st.cache_resource
def warmup_models():
    # Make sure these match the models you have installed in `ollama list`
    models = ['llama3.2:1b', 'qwen3:1.7b', 'gpt-oss:20b-cloud']
    status_text = st.empty()

    for model in models:
        status_text.text(f"🔥 Warming up {model}...")
        try:
            ollama.chat(
                model=model,
                messages=[{'role': 'user', 'content': 'hi'}],
                keep_alive='60m'
            )
        except Exception as e:
            st.error(f"Failed to load {model}: {e}")

    status_text.empty()
    return True


# Trigger warm-up
with st.spinner("Initializing AI Models... (This happens only once)"):
    warmup_models()

# --- Session State ---
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'draft' not in st.session_state:
    st.session_state.draft = ""
if 'review' not in st.session_state:
    st.session_state.review = ""
if 'final_ans' not in st.session_state:
    st.session_state.final_ans = ""

# --- UI Layout ---
with st.container():
    user_question = st.text_input("Enter your question:", key="main_input")

    # Reset if user types a new question
    if user_question and user_question != st.session_state.user_input:
        st.session_state.user_input = user_question
        st.session_state.processed = False  # Reset processed flag
        st.session_state.draft = ""
        st.session_state.review = ""
        st.session_state.final_ans = ""

    if st.button("Generate Answer"):
        if not user_question:
            st.warning("Please enter a question first.")
        else:
            # --- EXECUTION BLOCK (Runs all steps in background) ---
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Draft
                status_text.text("🤔 Model 1 (Llama) is drafting an initial answer...")
                response1 = ollama.chat(
                    model='llama3.2:1b',
                    messages=[{'role': 'user', 'content': f"Answer: {user_question}"}],
                    keep_alive='60m'
                )
                st.session_state.draft = response1['message']['content']
                progress_bar.progress(33)

                # Step 2: Review
                status_text.text("🧐 Model 2 (Qwen) is critiquing the draft...")
                prompt2 = f"Review this answer for errors:\nQ: {user_question}\nA: {st.session_state.draft}"
                response2 = ollama.chat(
                    model='qwen3:1.7b',
                    messages=[{'role': 'system', 'content': "You are a harsh reviewer."},
                              {'role': 'user', 'content': prompt2}],
                    keep_alive='60m'
                )
                st.session_state.review = response2['message']['content']
                progress_bar.progress(66)

                # Step 3: Final Polish
                status_text.text("✍️ Model 3 (gpt-oss-cloud') is writing the final answer...")
                prompt3 = f"Write a perfect answer based on this review:\nQ: {user_question}\nReview: {st.session_state.review}\nDraft: {st.session_state.draft}"
                response3 = ollama.chat(
                    model='gpt-oss:20b-cloud',
                    messages=[{'role': 'system', 'content': "You are an expert teacher."},
                              {'role': 'user', 'content': prompt3}],
                    keep_alive='60m'
                )
                st.session_state.final_ans = response3['message']['content']
                progress_bar.progress(100)

                # Mark as done
                st.session_state.processed = True
                status_text.empty()
                progress_bar.empty()

            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Result Display ---
if st.session_state.processed:
    st.divider()

    # 1. Show the Final Answer FIRST (Clean View)
    st.subheader("✅ Final Answer")
    st.markdown(st.session_state.final_ans)

    st.divider()

    # 2. "View Details" Expander (Hidden by default)
    with st.expander("🕵️ View Behind-the-Scenes (Draft & Review)"):
        st.markdown("### 📝 Step 1: Initial Draft (Llama 3.2)")
        st.info(st.session_state.draft)

        st.markdown("### 🔍 Step 2: Critical Review (Qwen)")
        st.warning(st.session_state.review)