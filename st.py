import streamlit as st
import pandas as pd
import utils
import base64
import io

"# Excellent Excel"

uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls"])

if uploaded_file is not None:
    sheet_names = utils.get_sheets_from_excel(uploaded_file)
    select = st.selectbox("Select Language:", options=sheet_names[:-1])
    if select:
        value_dict, new_df = utils.excel_helper(uploaded_file, language=select)
        try:
            new_df
        except Exception as e:
            f"Can't display the data because: {e}"
        # value_dict

        split_name, _ = uploaded_file.name.split(".")

        user_input = st.text_input(
            "What should your downloaded file be called? (DON'T WRITE '.xlsx')",
            split_name + "_excellent",
        )

        final_name = user_input + ".csv"
        towrite = io.BytesIO()
        downloaded_file = new_df.to_excel(
            towrite, encoding="utf-8", index=False, header=True
        )
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()  # some strings
        linko = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{final_name}.xlsx">Download excel file</a>'
        st.markdown(linko, unsafe_allow_html=True)

    # csv = new_df.to_csv(index=False)
    # b64 = base64.b64encode(csv.encode()).decode()  # some strings
    # linko = f'<a href="data:file/csv;base64,{b64}" download="{final_name}">Download csv file</a>'
    # st.markdown(linko, unsafe_allow_html=True)
