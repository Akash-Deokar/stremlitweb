import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Main Page",
    page_icon="👋",
)

import streamlit as st
st.title('Hi buddy, Welcome and All the best for the  most important step of EDA ')
st.header("Convert your file into comma(,) separated form")

def main():
    st.subheader("CSV/Excel File Reader")

    # File upload and parameter selection
    file = st.file_uploader("Upload file", type=["csv", "xlsx"])
    if file is not None:
        file_extension = file.name.split(".")[-1]

        if file_extension == "csv":
            # CSV specific options
            separator = st.text_input("Separator (e.g., ',', ';')", ',')
            if separator == '':
                separator = ','
            
            # Read CSV file
            df = pd.read_csv(file, sep=separator)
        elif file_extension == "xlsx":
            # Read Excel file
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            return

        # Display DataFrame
        st.write("### DataFrame")
        st.write(df)

        # Optionally, you can save the DataFrame to a CSV file
        if st.button("Save DataFrame as CSV"):
            csv_file = df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv_file, file_name='output.csv', mime='text/csv')

if __name__ == "__main__":
    main()



st.write('Now upload your comma separated file')


file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx'])

if file is not None:
    df=pd.read_csv(file)
    st.session_state['df']=df