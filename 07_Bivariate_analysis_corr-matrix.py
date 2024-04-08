import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation_matrix(df, x_column, y_column):
    """
    Plot a heatmap of the correlation matrix for selected x and y columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing numerical columns.
    x_column (str): The selected x column.
    y_column (str): The selected y column.

    Returns:
    None
    """
    # Create a subset DataFrame with selected x and y columns
    subset_df = df[[x_column, y_column]]

    # Compute the correlation matrix
    correlation_matrix = subset_df.corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(8, 6))

    # Plot the heatmap
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

    # Customize the plot
    plt.title(f'Correlation Matrix: {x_column} vs {y_column}')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Show the plot using Streamlit's pyplot
    st.pyplot()

def plot_all_correlations(df):
    """
    Plot correlation matrices for all possible pairs of numerical columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing numerical columns.

    Returns:
    None
    """
    # Compute the correlation matrix for all numerical columns
    correlation_matrix = df.select_dtypes(include=['int', 'float']).corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))

    # Plot the heatmap
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

    # Customize the plot
    plt.title('Correlation Matrix for All Numerical Columns')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Show the plot using Streamlit's pyplot
    st.pyplot()

def main():
    # Title of the app
    st.title("Correlation Matrix Analysis")

    # Retrieve the DataFrame from session state
    df = st.session_state['df']

    # Select numerical columns
    numerical_columns = df.select_dtypes(include=['int', 'float']).columns.tolist()

    # Sidebar for selecting x and y columns
    st.sidebar.title("Select Columns")
    x_column = st.sidebar.selectbox("Select X Column", numerical_columns)
    y_column = st.sidebar.selectbox("Select Y Column", numerical_columns)

    # Button to plot correlation matrix for selected x and y columns
    if st.sidebar.button("Plot Correlation Matrix"):
        plot_correlation_matrix(df, x_column, y_column)

    # Button to plot correlation matrix for all numerical columns
    if st.sidebar.button("Plot All Correlations"):
        plot_all_correlations(df)

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
