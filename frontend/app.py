import os

import requests
import streamlit as st


API_URL = os.getenv(
    "STUDYVAULT_API_URL",
    "http://127.0.0.1:8000",
)

# API Helpers
def get_conversations():
    try:
        response = requests.get(
            f"{API_URL}/conversations",
            timeout=10,
        )
        response.raise_for_status()

        return response.json().get(
            "conversations",
            [],
        )

    except requests.exceptions.RequestException:
        return []


def get_messages(conversation_id):
    try:
        response = requests.get(
            f"{API_URL}/conversations/"
            f"{conversation_id}/messages",
            timeout=10,
        )
        response.raise_for_status()

        return response.json().get(
            "messages",
            [],
        )

    except requests.exceptions.RequestException:
        return []


def get_documents():
    try:
        response = requests.get(
            f"{API_URL}/documents",
            timeout=10,
        )
        response.raise_for_status()

        return response.json().get(
            "documents",
            [],
        )

    except requests.exceptions.RequestException:
        return []


def upload_document(uploaded_file):
    try:
        response = requests.post(
            f"{API_URL}/documents/upload",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            },
            timeout=180,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get(
                "detail",
                "Document upload failed.",
            )
        except ValueError:
            detail = "Document upload failed."

        st.error(f"❌ {detail}")

        return None

    except requests.exceptions.RequestException as exc:
        st.error(
            "❌ Could not connect to the StudyVault API."
        )
        st.caption(str(exc))

        return None


def delete_document(document_id):
    try:
        response = requests.delete(
            f"{API_URL}/documents/{document_id}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get(
                "detail",
                "Document deletion failed.",
            )
        except ValueError:
            detail = "Document deletion failed."

        st.error(f"❌ {detail}")

        return None

    except requests.exceptions.RequestException as exc:
        st.error(
            "❌ Could not connect to the StudyVault API."
        )
        st.caption(str(exc))

        return None


def rename_conversation(
    conversation_id,
    title,
):
    try:
        response = requests.patch(
            f"{API_URL}/conversations/"
            f"{conversation_id}",
            json={
                "title": title,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get(
                "detail",
                "Conversation rename failed.",
            )
        except ValueError:
            detail = "Conversation rename failed."

        st.error(f"❌ {detail}")

        return None

    except requests.exceptions.RequestException as exc:
        st.error(
            "❌ Could not connect to the StudyVault API."
        )
        st.caption(str(exc))

        return None


def remove_conversation(
    conversation_id,
):
    try:
        response = requests.delete(
            f"{API_URL}/conversations/"
            f"{conversation_id}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get(
                "detail",
                "Conversation deletion failed.",
            )
        except ValueError:
            detail = "Conversation deletion failed."

        st.error(f"❌ {detail}")

        return None

    except requests.exceptions.RequestException as exc:
        st.error(
            "❌ Could not connect to the StudyVault API."
        )
        st.caption(str(exc))

        return None


def ask_question(question):
    payload = {
        "question": question,
        "top_k": 5,
        "conversation_id": st.session_state.conversation_id,
        "study_mode": st.session_state.study_mode,
    }

    response = requests.post(
        f"{API_URL}/ask",
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# Streamlit Configuration
st.set_page_config(
    page_title="StudyVault",
    page_icon="📚",
    layout="wide",
)


st.title("📚 StudyVault")

st.caption(
    "Your personal AI-powered learning assistant"
)


# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []


if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


if "editing_conversation_id" not in st.session_state:
    st.session_state.editing_conversation_id = None

if "study_mode" not in st.session_state:
    st.session_state.study_mode = "explain"



# Sidebar
with st.sidebar:

    # Study Mode
    st.header("🎓 Study Mode")

    study_mode = st.selectbox(
        "Choose how StudyVault should help you",
        options=[
            "explain",
            "summary",
            "quiz",
            "flashcards",
            "key_points",
        ],
        format_func=lambda mode: {
            "explain": "📖 Explain",
            "summary": "📝 Summary",
            "quiz": "❓ Quiz",
            "flashcards": "🧠 Flashcards",
            "key_points": "🔑 Key Points",
        }[mode],
    )

    st.session_state.study_mode = study_mode

    # Conversations
    st.header("💬 Conversations")

    if st.button(
        "➕ New Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.session_state.editing_conversation_id = None

        st.rerun()


    conversations = get_conversations()

    st.caption(
        f"{len(conversations)} conversation(s)"
    )


    if not conversations:
        st.caption(
            "No previous conversations yet."
        )


    for conversation in conversations:

        conversation_id = conversation["id"]
        title = conversation["title"]


        # Conversation currently being edited
        if (
            st.session_state.editing_conversation_id
            == conversation_id
        ):

            new_title = st.text_input(
                "Conversation title",
                value=title,
                key=f"rename_input_{conversation_id}",
            )


            col1, col2 = st.columns(2)


            with col1:
                if st.button(
                    "💾 Save",
                    key=f"save_{conversation_id}",
                    use_container_width=True,
                ):

                    if new_title.strip():

                        result = rename_conversation(
                            conversation_id,
                            new_title,
                        )

                        if result:
                            st.session_state.editing_conversation_id = None
                            st.rerun()

                    else:
                        st.warning(
                            "Title cannot be empty."
                        )


            with col2:
                if st.button(
                    "❌ Cancel",
                    key=f"cancel_{conversation_id}",
                    use_container_width=True,
                ):

                    st.session_state.editing_conversation_id = None
                    st.rerun()


        else:

            # Open conversation
            if st.button(
                title,
                key=f"conversation_{conversation_id}",
                use_container_width=True,
            ):

                messages = get_messages(
                    conversation_id
                )

                st.session_state.conversation_id = (
                    conversation_id
                )

                st.session_state.messages = [
                    {
                        "role": message["role"],
                        "content": message["content"],
                    }
                    for message in messages
                ]

                st.session_state.editing_conversation_id = None

                st.rerun()

            # Conversation actions
            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "✏️",
                    key=f"edit_{conversation_id}",
                    help="Rename conversation",
                    use_container_width=True,
                ):

                    st.session_state.editing_conversation_id = (
                        conversation_id
                    )

                    st.rerun()


            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{conversation_id}",
                    help="Delete conversation",
                    use_container_width=True,
                ):

                    result = remove_conversation(
                        conversation_id
                    )

                    if result:

                        if (
                            st.session_state.conversation_id
                            == conversation_id
                        ):
                            st.session_state.messages = []
                            st.session_state.conversation_id = None

                        st.success(
                            "Conversation deleted."
                        )

                        st.rerun()


    st.divider()

    # Study Materials
    st.header("📄 Study Materials")


    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        help=(
            "Upload lecture notes, textbooks, "
            "research papers, or other study materials."
        ),
    )


    if st.button(
        "📤 Process Document",
        use_container_width=True,
        disabled=uploaded_file is None,
    ):

        with st.spinner(
            "📚 Reading, chunking, and indexing your document..."
        ):

            result = upload_document(
                uploaded_file
            )


        if result:

            st.success(
                "✅ Document processed successfully!"
            )

            st.write(
                f"📄 **{result['filename']}**"
            )

            st.write(
                f"📑 **Pages:** {result['pages']}"
            )

            st.write(
                f"🧩 **Chunks:** {result['chunks']}"
            )

            st.rerun()


    st.divider()

    # Uploaded Documents
    st.header("📚 Uploaded Documents")


    documents = get_documents()


    total_documents = len(documents)

    total_chunks = sum(
        document["chunks"]
        for document in documents
    )


    col1, col2 = st.columns(2)


    with col1:
        st.metric(
            "Documents",
            total_documents,
        )


    with col2:
        st.metric(
            "Chunks",
            total_chunks,
        )


    if st.button(
        "🔄 Refresh Documents",
        use_container_width=True,
    ):
        st.rerun()


    if not documents:

        st.caption(
            "No documents uploaded yet."
        )


    for document in documents:

        document_id = document[
            "document_id"
        ]

        filename = document[
            "filename"
        ]

        chunks = document[
            "chunks"
        ]


        st.write(
            f"📄 **{filename}**"
        )

        st.caption(
            f"🧩 {chunks} chunks"
        )


        if st.button(
            "🗑️ Delete",
            key=f"delete_document_{document_id}",
            use_container_width=True,
        ):

            with st.spinner(
                "Deleting document..."
            ):

                result = delete_document(
                    document_id
                )


            if result:

                st.success(
                    "✅ Document deleted."
                )

                st.rerun()

# Main Chat Area
if not st.session_state.messages:

    st.info(
        "👋 Welcome to StudyVault!\n\n"
        "Upload your study materials and ask "
        "questions about them below."
    )


    st.markdown(
        """
        ### What can I ask?

        - 📖 Explain a concept from my documents
        - 🔍 Find specific information
        - 📝 Summarize a topic
        - 💡 Ask follow-up questions
        - 📚 Compare concepts from my study materials
        """
    )

# Chat History
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# Chat Input
question = st.chat_input(
    "Ask a question about your study materials..."
)


if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    with st.chat_message("user"):

        st.markdown(question)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Searching your study materials..."
        ):

            try:

                data = ask_question(
                    question
                )


                st.session_state.conversation_id = (
                    data["conversation_id"]
                )


                answer = data["answer"]


                st.markdown(answer)


                # Sources
                sources = data.get(
                    "sources",
                    [],
                )


                if sources:

                    with st.expander(
                        "📚 Sources",
                        expanded=False,
                    ):

                        for source in sources:

                            st.markdown(
                                f"📄 **{source['filename']}**  \n"
                                f"Page: **{source['page']}**"
                            )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )


            except requests.exceptions.HTTPError as exc:

                st.error(
                    "❌ The StudyVault API returned an error."
                )

                st.caption(
                    str(exc)
                )


            except requests.exceptions.RequestException as exc:

                st.error(
                    "❌ Could not connect to the StudyVault API."
                )

                st.caption(
                    str(exc)
                )


            except Exception as exc:

                st.error(
                    "❌ Something went wrong while processing your question."
                )

                st.caption(
                    str(exc)
                )