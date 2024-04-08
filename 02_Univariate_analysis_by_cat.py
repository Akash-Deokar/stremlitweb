import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def display_value_counts(df):
    # Get categorical columns
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Display value counts for each categorical column individually
    st.write("### Value Counts for Categorical Columns")
    for column in categorical_columns:
        st.write(f"##### {column}")
        value_counts = df[column].value_counts().reset_index()
        value_counts.columns = [column, 'Count']
        st.dataframe(value_counts)

def select_and_store_columns(df):
    # Get categorical columns
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Multiselect to choose multiple categorical columns to store
    selected_columns = st.sidebar.multiselect("Select Categorical Columns to Store", categorical_columns)

    # Store selected columns in session state when "Store Columns" button is clicked
    if st.sidebar.button("Store Columns"):
        st.session_state['stored_columns'] = selected_columns

def plot_countplots(df):
    # Retrieve stored columns from session state
    stored_columns = st.session_state.get('stored_columns', [])

    if stored_columns:
        st.write("### Count Plots for Stored Categorical Columns")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Generate count plots for each stored column
        for column in stored_columns:
            st.write(f"#### {column} Count Plot")
            plt.figure(figsize=(10, 6))
            sns.countplot(x=column, data=df)
            plt.xticks(rotation=45)
            plt.xlabel(column)
            plt.ylabel('Count')
            st.pyplot()

def download_plots(df):
    # Retrieve stored columns from session state
    stored_columns = st.session_state.get('stored_columns', [])

    if stored_columns:
        st.write("### Download Plots for Final Presentation")

        # Generate and download plots for each stored column
        for i, column in enumerate(stored_columns):
            plt.figure(figsize=(10, 6))
            sns.countplot(x=column, data=df)
            plt.xticks(rotation=45)
            plt.xlabel(column)
            plt.ylabel('Count')
            # Save plot to BytesIO buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            # Generate base64 encoded string for download link
            b64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            # Create download link
            href = f'<a href="data:file/png;base64,{b64}" download="countplot_{i+1}.png">Download Plot {i+1}</a>'
            st.markdown(href, unsafe_allow_html=True)

def main():
    # Title of the app
    st.title("Do analysis using categorical variables")

    # Retrieve the DataFrame from session state
    df = st.session_state['df']
    st.write(df.head())  # Display a preview of the DataFrame

    # Display value counts for each categorical column
    display_value_counts(df)

    # Sidebar options for selecting and storing categorical columns
    st.sidebar.title("Select and Store Categorical Columns")

    select_and_store_columns(df)

    # Button to plot count plots for stored columns
    if st.sidebar.button("Plot Count Plots"):
        plot_countplots(df)

    # Button to download plots for final presentation
    if st.sidebar.button("Download Plots"):
        download_plots(df)  # Pass df to download_plots function

if __name__ == '__main__':
    # Check if 'df' is in session state
    if 'df' not in st.session_state:
        # Load your DataFrame into session state (replace this with your DataFrame loading logic)
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df

    # Run the main app
    main()
