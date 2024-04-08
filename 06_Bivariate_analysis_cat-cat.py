import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def select_and_store_columns(df):
    # Get categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    # Dropdowns to choose x and y columns for stacked bar chart
    x_column = st.sidebar.selectbox("Select X Column", categorical_columns)
    y_column = st.sidebar.selectbox("Select Y Column", categorical_columns)

    # Button to plot stacked bar chart
    if st.sidebar.button("Plot Stacked Bar Chart"):
        plot_stacked_bar_chart(df, x_column, y_column)

def plot_stacked_bar_chart(df, x_column, y_column):
    # Plot size adjustment
    plot_width = st.session_state.get('plot_width', 12)
    plot_height = st.session_state.get('plot_height', 8)

    # Plot stacked bar chart based on selected x and y columns
    st.write(f"### Stacked Bar Chart: {x_column} vs {y_column}")
    plt.figure(figsize=(plot_width, plot_height))
    sns.countplot(x=x_column, hue=y_column, data=df, palette='viridis')
    plt.xlabel(x_column)
    plt.ylabel('Count')

    # Create a download link for the stacked bar chart
    download_link = download_plot_as_png(plt)
    st.markdown(download_link, unsafe_allow_html=True)

    st.pyplot()

def download_plot_as_png(plot):
    # Save the plot to a BytesIO buffer as a PNG image
    buffer = BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the PNG image as base64 and create a download link
    plot_base64 = base64.b64encode(buffer.getvalue()).decode()
    download_link = f'<a href="data:image/png;base64,{plot_base64}" download="plot.png">Download Plot</a>'
    
    return download_link

def main():
    # Title of the app
    st.title("Do analysis using Stacked bar chart")

    # Retrieve the DataFrame from session state
    if 'df' not in st.session_state:
        # Load your DataFrame into session state (replace this with your DataFrame loading logic)
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df

    df = st.session_state['df']
    st.write(df.head())  # Display a preview of the DataFrame

    # Sidebar options for selecting x and y columns for stacked bar chart
    st.sidebar.title("Select Columns for Stacked Bar Chart")
    select_and_store_columns(df)

    # Slider to adjust plot size
    st.sidebar.subheader("Adjust Plot Size")
    plot_width = st.sidebar.slider("Width", min_value=8, max_value=20, value=12)
    plot_height = st.sidebar.slider("Height", min_value=6, max_value=16, value=8)
    
    # Store plot size in session state
    st.session_state['plot_width'] = plot_width
    st.session_state['plot_height'] = plot_height

if __name__ == '__main__':
    main()
