import streamlit as st
import pandas as pd
import requests
import numpy as np
import csv
import os
import uuid
from PIL import Image
import random
import time
from scipy.stats import bernoulli
# =========================================================
# BERNOULLI TRIAL
# =========================================================
def sustainability_section():
    try:
        p = st.slider(
            "Probability of sustainable day",
            0.0,
            1.0,
            0.5
        )
        # 1. Initialize the only two variables you need
        if 'bernoulli_result' not in st.session_state.bernoulli_result:
            st.session_state.bernoulli_result = None
        result = st.session_state.get("bernoulli_result", 0)
        st.write(f"Bernoulli Result: {result}")
        
        if "sustainable" not in st.session_state:
            st.session_state.sustainable = 0
        if "unsustainable" not in st.session_state:
            st.session_state.unsustainable = 0
    
        # 2. Separate functions to strictly modify the counts
        def increment_sustainable():
            st.session_state.sustainable += 1
    
        def increment_unsustainable():
            st.session_state.unsustainable += 1
        
        if st.button(
            "Run Bernoulli Trial",
            key="bernoulli_button"
        ):
            st.session_state.bernoulli_result = bernoulli.rvs(p)
        result = st.session_state.bernoulli_result
        st.write(f"DEBUG result: {result}")
        if result is not None:
            if result == 1:
                st.success("Sustainable outcome")
                st.session_state.sustainable += 1
            else:
                st.error("Unsustainable outcome")
                st.session_state.unsustainable += 1
        st.session_state.total += 1
        
        st.divider()
    
        # 3. Calculate the total instantly on the fly (Prevents +1 overhead errors)
        total_outcomes = st.session_state.sustainable + st.session_state.unsustainable
    
        # 4. Display the results in 3 columns
        col1, col2, col3 = st.columns(3)
    
        col1.metric("Sustainable outcomes", st.session_state.sustainable)
        col2.metric("Unsustainable outcomes", st.session_state.unsustainable)
        col3.metric("Total Outcomes", total_outcomes)
    
    except Exception as e:
    
        st.warning(
            f"Bernoulli Trial Function unavailable: {e}"
        )
    
    except KeyError as e:
    
        st.error(
            f"Display error: missing field {e}"
        )
    
    except Exception as e:
    
        st.error(
            f"Unexpected display error: {e}"
        )
