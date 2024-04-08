import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Define caching for the plotting functions
@st.cache(show_spinner=False)
def plot_box_plot(df, x_column, y_column, plot_width, plot_height):
    # Plot boxplot based on selected x and y columns
    plt.figure(figsize=(plot_width, plot_height))
    sns.boxplot(x=x_column, y=y_column, data=df)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    return plt

@st.cache(show_spinner=False)
def plot_bar_plot(df, x_column, y_column, plot_width, plot_height):
    # Plot bar plot based on selected x and y columns
    plt.figure(figsize=(plot_width, plot_height))
    sns.barplot(x=x_column, y=y_column, data=df)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    return plt

def main():
    # Title of the app
    st.title("Do analysis using Boxplot and Barplot")

    # Retrieve the DataFrame from session state
    if 'df' not in st.session_state:
        # Load your DataFrame into session state (replace this with your DataFrame loading logic)
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df

    df = st.session_state['df']
    st.write(df.head())  # Display a preview of the DataFrame

    # Sidebar options for selecting x and y columns for plots
    st.sidebar.title("Select Columns for Plots")
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    numerical_columns = df.select_dtypes(include=['int', 'float']).columns.tolist()

    x_column = st.sidebar.selectbox("Select X Column", categorical_columns)
    y_column = st.sidebar.selectbox("Select Y Column", numerical_columns)

    plot_type = st.sidebar.radio("Select Plot Type", ["Box Plot", "Bar Plot"])

    plot_width = st.sidebar.slider("Plot Width", min_value=8, max_value=20, value=10)
    plot_height = st.sidebar.slider("Plot Height", min_value=6, max_value=16, value=6)

    # Button to plot selected plot type
    if st.sidebar.button(f"Plot {plot_type}"):
        if plot_type == "Box Plot":
            plot = plot_box_plot(df, x_column, y_column, plot_width, plot_height)
        elif plot_type == "Bar Plot":
            plot = plot_bar_plot(df, x_column, y_column, plot_width, plot_height)

        # Create a download link for the plot
        download_link = download_plot_as_png(plot)
        st.markdown(download_link, unsafe_allow_html=True)

        # Display the plot
        st.pyplot(plot)

def download_plot_as_png(plot):
    # Save the plot to a BytesIO buffer as a PNG image
    buffer = BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the PNG image as base64 and create a download link
    plot_base64 = base64.b64encode(buffer.getvalue()).decode()
    download_link = f'<a href="data:image/png;base64,{plot_base64}" download="plot.png">Download Plot</a>'
    return download_link

if __name__ == '__main__':
    main()
