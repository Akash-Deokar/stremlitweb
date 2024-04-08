import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def select_and_store_columns(df):
    # Get numerical columns
    numerical_columns = df.select_dtypes(include=['int', 'float']).columns.tolist()

    # Multiselect to choose multiple numerical columns to store
    selected_columns = st.sidebar.multiselect("Select Numerical Columns to Store", numerical_columns)

    # Store selected columns in session state when "Store Columns" button is clicked
    if st.sidebar.button("Store Columns"):
        st.session_state['stored_columns'] = selected_columns

def plot_histogram(df):
    # Retrieve stored columns from session state
    stored_columns = st.session_state.get('stored_columns', [])

    if stored_columns:
        st.write("### Histogram for Stored Numerical Columns")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Generate histograms for each stored column
        for column in stored_columns:
            st.write(f"#### {column} Histogram Plot")
            plt.figure(figsize=(10, 6))
            sns.histplot(x=column, data=df)
            plt.xticks(rotation=45)
            plt.xlabel(column)
            plt.ylabel('Count')
            st.pyplot()

def plot_boxplot(df):
    # Retrieve stored columns from session state
    stored_columns = st.session_state.get('stored_columns', [])

    if stored_columns:
        st.write("### Boxplot for Stored Numerical Columns")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Generate boxplots for each stored column
        for column in stored_columns:
            st.write(f"#### {column} Boxplot")
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=column, data=df)
            plt.xticks(rotation=45)
            plt.xlabel(column)
            plt.ylabel('Value')
            st.pyplot()

def download_plots(df):
    # Retrieve stored columns from session state
    stored_columns = st.session_state.get('stored_columns', [])

    if stored_columns:
        st.write("### Download Plots for Final Presentation")

        # Generate and download plots for each stored column
        for i, column in enumerate(stored_columns):
            plt.figure(figsize=(10, 6))
            sns.histplot(x=column, data=df)
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
            href = f'<a href="data:file/png;base64,{b64}" download="plot_{i+1}.png">Download Plot {i+1}</a>'
            st.markdown(href, unsafe_allow_html=True)

def main():
    # Title of the app
    st.title("Do analysis using numerical variables")

    # Retrieve the DataFrame from session state
    df = st.session_state['df']
    st.write(df.head())  # Display a preview of the DataFrame

    # Sidebar options for selecting and storing numerical columns
    st.sidebar.title("Select and Store Numerical Columns")

    select_and_store_columns(df)

    # Button to plot histogram plots for stored columns
    if st.sidebar.button("Plot Histogram "):
        plot_histogram(df)

    # Button to plot boxplot for stored columns
    if st.sidebar.button("Plot Boxplot"):
        plot_boxplot(df)

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
