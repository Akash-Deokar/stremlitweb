import streamlit as st


df=st.session_state['df']

st.title('Dataframe description')
st.subheader('Shape of dataset')
st.write(df.shape)

st.subheader('First five rows of dataset')
st.write(df.head())

st.subheader('Random five rows of dataset')
st.write(df.sample(5))

st.subheader('Last five rows of dataset')
st.write(df.tail(5))

st.subheader('Datatypes of each column of dataset')
st.write(df.dtypes)

st.subheader('How your dataset looks mathematically')
st.write(df.describe())

st.subheader('Missing values each column of dataset')
st.write(df.isnull().sum())

st.subheader('Duplicate values of dataset')
st.write(df.duplicated().sum())

numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
numeric_df = df[numeric_columns]

st.subheader('Columns names of dataset containing numeric datatype ')
st.write(numeric_columns)

categorical_columns = df.select_dtypes(include=['object']).columns
categorical_df = df[categorical_columns]
st.subheader('Columns names of dataset containing categorical datatype ')
st.write(categorical_columns)

