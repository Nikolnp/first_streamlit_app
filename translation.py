import streamlit as st
from openai import OpenAI
from openai import RateLimitError


def render_with_llm(content: str) -> str:

    language = st.session_state.get(
        "language",
        "English"
    )

    if language == "English":
        return content

    if "OPENAI_API_KEY" not in st.secrets:
        st.warning(
            "OpenAI API key not configured."
        )
        return content

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    try:

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

    except RateLimitError:

        st.warning(
            "Translation quota exceeded."
        )

        return content

    except Exception as e:

        st.warning(
            f"Translation failed: {e}"
        )

        return content