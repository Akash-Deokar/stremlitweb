import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def select_and_store_columns(df):
    # Get numerical columns
    numerical_columns = df.select_dtypes(include=['int', 'float']).columns.tolist()

    # Dropdowns to choose x and y columns for scatter plot
    x_column = st.sidebar.selectbox("Select X Column", numerical_columns)
    y_column = st.sidebar.selectbox("Select Y Column", numerical_columns)

    # Button to plot individual scatter plot
    if st.sidebar.button("Plot Scatter Plot"):
        plot_scatter_plot(df, x_column, y_column)

def plot_scatter_plot(df, x_column, y_column):
    # Plot individual scatter plot based on selected x and y columns
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write(f"### Scatter Plot: {x_column} vs {y_column}")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_column, y=y_column, data=df)
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    # Create a download link for the scatter plot
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
    download_link = f'<a href="data:image/png;base64,{plot_base64}" download="scatter_plot.png">Download Scatter Plot</a>'

    return download_link

def main():
    # Title of the app
    st.title("Do Analysis using Scatter Plot")

    # Retrieve the DataFrame from session state
    if 'df' not in st.session_state:
        # Load your DataFrame into session state (replace this with your DataFrame loading logic)
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df

    df = st.session_state['df']
    st.write(df.head())  # Display a preview of the DataFrame

    # Sidebar options for selecting x and y columns
    st.sidebar.title("Select Columns for Scatter Plot")
    select_and_store_columns(df)

    # Sidebar button to plot pairplot for all numerical columns
    plot_button = st.sidebar.button("Plot Pairplot")

    if plot_button:
        # Select only numerical columns
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # Plot pairplot for all pairs of numerical columns
        sns.set(style='ticks')
        pair_plot = sns.pairplot(df[numeric_columns])
        plt.title('Pairplot of Numerical Columns')
        st.pyplot(pair_plot)  # Display the plot in Streamlit

if __name__ == '__main__':
    main()
