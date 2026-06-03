import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


def render_with_llm(
    content: str
) -> str:

    language = st.session_state.get(
        "language",
        "English"
    )

    if language == "English":

        return content

    response = client.responses.create(

        model="gpt-4o",

        input=f"""
Translate the following educational content into {language}.

Rules:
- Preserve markdown
- Preserve emojis
- Keep formulas unchanged
- Do not summarize
- Return only the translated content

Content:

{content}
"""
    )

    return response.output_text