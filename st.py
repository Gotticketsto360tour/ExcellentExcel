from re import split
import streamlit as st
import pandas as pd
import utils
import base64

"# Excellent Excel"

uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls"])

if uploaded_file is not None:
    value_dict, new_df = utils.excel_helper(uploaded_file)
    new_df
    #value_dict

    split_name, _ = uploaded_file.name.split(".")

    user_input = st.text_input(
        "What should your downloaded file be called? (DON'T WRITE '.csv')",
        split_name + "_excellent",
    )

    final_name = user_input + ".csv"
    csv = new_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko = f'<a href="data:file/csv;base64,{b64}" download="{final_name}">Download csv file</a>'
    st.markdown(linko, unsafe_allow_html=True)
