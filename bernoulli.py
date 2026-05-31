# =========================================================
# BERNOULLI LEARNING VISUALIZATION ENGINE
# =========================================================

from random import random

import streamlit as st
import pandas as pd
import altair as alt


# =========================================================
# VISUALIZATION FUNCTION
# =========================================================

def visualize_outcomes(history):

    if len(history) == 0:

        st.info("No trials yet.")

        return

    df = pd.DataFrame({

        "Trial": list(range(len(history))),

        "Outcome": [

            "Sustainable"
            if x == 1
            else "Unsustainable"

            for x in history
        ]
    })

    chart = alt.Chart(df).mark_circle(
        size=120
    ).encode(

        x="Trial",

        y=alt.Y(
            "Outcome",
            sort=[
                "Sustainable",
                "Unsustainable"
            ]
        ),

        color="Outcome",

        tooltip=[
            "Trial",
            "Outcome"
        ]
    ).properties(

        title=
        "Bernoulli Trial Visualization",

        width=700,

        height=300
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )

# =========================================================
# BERNOULLI SECTION
# =========================================================

def bernoulli_trial():

    try:

        st.title(
            "🧠 Bernoulli Trial Explorer"
        )
      
        st.header("🌱 Will Tomorrow Be Sustainable?")

        with st.expander("🤔 The Question"):

            st.markdown("""
            Imagine you're trying to live sustainably.

            Tomorrow will either be:

            - ✅ Sustainable
            - ❌ Unsustainable

            Only one outcome can happen.
            """)

        with st.expander("🧪 The Experiment"):

            st.markdown("""
            Move the slider and run a Bernoulli trial.
            Observe whether the outcome is sustainable or unsustainable.
            """)

        
        # =================================================
        # PROBABILITY SLIDER
        # =================================================

        p = st.slider(

            "Probability of sustainable day",

            0.0,

            1.0,

            0.5
        )

        # =================================================
        # SESSION INITIALIZATION
        # =================================================

        if "bernoulli_result" not in st.session_state:

            st.session_state.bernoulli_result = None

        if "probability" not in st.session_state:

            st.session_state.probability = p

        if "sustainable" not in st.session_state:

            st.session_state.sustainable = 0

        if "unsustainable" not in st.session_state:

            st.session_state.unsustainable = 0

        if "total" not in st.session_state:

            st.session_state.total = 0

        if "trial_history" not in st.session_state:

            st.session_state.trial_history = []

        if "sustainable_history" not in st.session_state:

            st.session_state.sustainable_history = []

        if "unsustainable_history" not in st.session_state:

            st.session_state.unsustainable_history = []

        # =================================================
        # RESET EXPERIMENT IF p CHANGES
        # =================================================

        if p != st.session_state.probability:

            st.session_state.sustainable = 0

            st.session_state.unsustainable = 0

            st.session_state.total = 0

            st.session_state.bernoulli_result = None

            st.session_state.trial_history = []

            st.session_state.sustainable_history = []

            st.session_state.unsustainable_history = []

            st.session_state.probability = p

            st.warning(

                "Probability changed. "
                "Experiment reset."
            )

        # =================================================
        # RUN BERNOULLI TRIAL
        # =================================================

        if st.button(

            "Run Bernoulli Trial",

            key="bernoulli_button"
        ):

            result = 1 if random() < p else 0

            st.session_state.bernoulli_result = result

            st.session_state.trial_history.append(
                result
            )

            if result == 1:

                st.success(
                    "Sustainable outcome"
                )

                st.session_state.sustainable += 1

                st.session_state.sustainable_history.append(
                    1
                )

                st.session_state.unsustainable_history.append(
                    0
                )

            else:

                st.error(
                    "Unsustainable outcome"
                )

                st.session_state.unsustainable += 1

                st.session_state.sustainable_history.append(
                    0
                )

                st.session_state.unsustainable_history.append(
                    1
                )

            st.session_state.total += 1

        # =================================================
        # METRICS
        # =================================================

        total_outcomes = (

            st.session_state.sustainable +

            st.session_state.unsustainable
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(

            "Sustainable Outcomes",

            st.session_state.sustainable
        )

        col2.metric(

            "Unsustainable Outcomes",

            st.session_state.unsustainable
        )

        col3.metric(

            "Total Outcomes",

            total_outcomes
        )
        # =================================================
        # VISUALIZATION
        # =================================================

        st.subheader(
            "📈 Outcome Visualization"
        )

        visualize_outcomes(

            st.session_state.trial_history
        )
        # =================================================
        # LIVE FORMULA
        # =================================================

        st.subheader(
            "📘 Bernoulli Formula"
        )

        st.latex(
            r"P(X=x)=p^x(1-p)^{1-x}"
        )

        st.markdown("""
        **Where:**

        - X = outcome
        - x = 0 or 1
        - p = probability of success

        For this simulation:

        - Success = Sustainable day
        - Failure = Unsustainable day
        """)

        # =================================================
        # MINI EXPERIMENT
        # =================================================

        st.subheader(
            "🔬 Mini Experiment"
        )

        st.info(

            "Set p = 0.65 and run 20 trials.\n\n"

            "Then compare against p = 0.2.\n\n"

            "Observe how the visualization changes."
        )
        with st.expander("👀 What Did We Observe?"):

            st.markdown("""
            Even when supposedly p = 0.65, failure can still occur.

            Probability is not certainty.

            A 65% chance of success still leaves a 35% chance of failure.
            """)
        
        # =================================================
        # ACTIVE LEARNING QUESTIONS
        # =================================================

        st.subheader(
            "🧪 Knowledge Check"
        )

        q1 = st.radio(

            "What happens when p approaches 1?",

            [

                "More failures",

                "More successes",

                "No change"
            ]
        )

        if q1 == "More successes":

            st.success(
                "Correct!"
            )

        q2 = st.radio(

            "Why must probability remain constant?",

            [

                "Because Bernoulli assumes identical trials",

                "Only for visualization",

                "It does not matter"
            ]
        )

        if q2 == "Because Bernoulli assumes identical trials":

            st.success(
                "Correct!"
            )

        q3 = st.radio(

            "What does a Bernoulli trial produce?",

            [

                "Continuous outcomes",

                "One binary outcome",

                "Infinite values"
            ]
        )

        if q3 == "One binary outcome":

            st.success(
                "Correct!"
            )

        

        # =================================================
        # RELATED CONCEPTS
        # =================================================

        st.subheader(
            "🔗 Related Concepts"
        )

        related_cols = st.columns(4)

        related_cols[0].button(
            "Probability"
        )

        related_cols[1].button(
            "Binomial Distribution"
        )

        related_cols[2].button(
            "Statistics"
        )

        related_cols[3].button(
            "Random Variables"
        )
        st.markdown("""
        ## 🔗 Where This Leads Next

        🌱 **Bernoulli Trial**
        ⬇️

        📊 **Binomial Distribution**
        ⬇️

        🎯 **Geometric Distribution**
        ⬇️

        📈 **Negative Binomial Distribution**
        ⬇️

        🤖 **Machine Learning Classification**
        """)

    except Exception as e:

        st.error(

            f"Bernoulli Section Error: {e}"
        )
