import streamlit as st
import pandas as pd
import io
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)
    

    number_rows, number_columns = df.shape
    categorical_var = df.select_dtypes(include='object').shape[1]
    numerical_var = df.select_dtypes(include=['int', 'float']).shape[1]
    bool_var = df.select_dtypes(include='bool').shape[1]

    st.write(f"total rows: {number_rows}")
    st.write(f"total columns: {number_columns}")
    st.write(f"total categorical variables: {categorical_var}")
    st.write(f"total numerical variables: {numerical_var}")
    st.write(f"total boolean variables: {bool_var}")


    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      sns.histplot(df[numerical_column], bins = hist_bins, alpha = choose_opacity, color = choose_color)
      
      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      st.write()

      summary = df[numerical_column].describe()

      minimum = summary['min']
      q1 = summary['25%']
      median = summary['50%']
      q3 = summary['75%']
      maximum = summary['max']

      st.write("Minimum:", minimum)
      st.write("Q1:", q1)
      st.write("Median:", median)
      st.write("Q3:", q3)
      st.write("Maximum:", maximum)


      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

    if column_type == "Categorical":
      categorical_column = st.selectbox(
      'Categorical :', df.select_dtypes(include = ['object']).columns)
      opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      df3 = df
      df3['total'] = 1
      df3 = df3.groupby(categorical_column)['total'].count().reset_index()
      df3['proportion'] = df3['total'] / df3['total'].sum()
      st.table(df3)

      df2 = df[categorical_column].value_counts().reset_index()
      df2.columns = [categorical_column, "Count"]
      fig, ax = plt.subplots()
      sns.barplot(data = df2, x = "Count", y = categorical_column , alpha = 1)
      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)
      


      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )