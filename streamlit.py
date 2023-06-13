import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import io
import numpy as np
from streamlit_pandas_profiling import st_profile_report

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.sidebar.checkbox("Show Data Frame", key="disabled")
    show_shape = st.sidebar.checkbox("Show the Shape of Data Frame")
    show_info = st.sidebar.checkbox("Show the Info of Data Frame")
    if show_df:
      st.write(df)
    if show_shape:
      #st.subheader('Shape of Data Frame')
      #st.write('Num of Rows: ', df.shape[0])
      #st.write('Num of Columns: ', df.shape[1])
      #st.write('Size:', df.size)
      col_info1, col_info2, col_info3 = st.columns(3)
      col_info1.metric('Num of Rows', df.shape[0])
      col_info2.metric('Num of Columns', df.shape[1])
      col_info3.metric('Size', df.size)
    if show_info:
      buffer = io.StringIO()
      df.info(buf=buffer)
      s = buffer.getvalue()
      st.text(s)

      categorical_count = 0
      numerical_count = 0
      boolean_count = 0
      datetime_count = 0

      for column in df.columns:
        if np.issubdtype(df[column].dtype, np.number):
          numerical_count += 1
        elif df[column].dtype == bool:
          boolean_count += 1
        elif df[column].dtype == 'datetime64[ns]':
          datetime_count += 1
        else:
          categorical_count += 1

      st.write(f"Number of categorical columns: {categorical_count}")
      st.write(f"Number of numerical columns: {numerical_count}")
      st.write(f"Number of boolean columns: {boolean_count}")
      st.write(f"Number of datetime columns: {datetime_count}")    


      
    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)
      
      show_df_column = st.sidebar.checkbox("Show the Data Frame with the selected column")
      if show_df_column:
        st.write(df[numerical_column])
      show_statistic = st.sidebar.checkbox("Show the Descriptive Statistic of Data Frame")
      if show_statistic:
        st.write(df.describe())
      
      pick_chart = st.selectbox('Select a Distribution Chart', ("Histogram", "Density Plot", "Box Plot"))
      # histogram 
      if pick_chart == "Histogram":
        choose_color = st.color_picker('Pick a Color', "#69b3a2")
        choose_opacity = st.slider(
            'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

        hist_bins = st.slider('Number of bins', min_value=5,
                              max_value=150, value=30)
        hist_title = st.text_input('Set Title', 'Histogram')
        hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

        fig, ax = plt.subplots()
        ax.hist(df[numerical_column], bins=hist_bins,
               edgecolor="black", color=choose_color, alpha=choose_opacity)
        ax.set_title(hist_title)
        ax.set_xlabel(hist_xtitle)
        ax.set_ylabel('Count')

        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)

        # Display the download button
        with open("plot.png", "rb") as file:
          btn = st.download_button(
             label="Download image",
             data=file,
             file_name="Figure.png",
             mime="image/png"
        )
      # Density Plot
      if pick_chart == "Density Plot":
        choose_color = st.color_picker('Pick a Color', "#C9154E")
        choose_opacity = st.slider(
           'Opacity', min_value=0.0, max_value=1.0, step=0.06)
        choose_shade = st.checkbox("Shade of Graph")
        fig, ax = plt.subplots()
        sns.kdeplot(df[numerical_column], color = choose_color, alpha = choose_opacity, shade = choose_shade)
        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)
        with open("plot.png", "rb") as file:
          btn = st.download_button(
            label="Download image",
            data=file,
            file_name="Figure.png",
            mime="image/png"
          )
      
      # Box Plot
      if pick_chart == "Box Plot":
        colors = st.color_picker('Pick a Color', "#6778D2")
        fig, ax = plt.subplots()
        sns.boxplot(y = df[numerical_column], color = colors)
        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)
        with open("plot.png", "rb") as file:
          btn = st.download_button(
          label="Download image",
          data=file,
          file_name="Figure.png",
          mime="image/png"
          )
      
    if column_type == "Categorical" or column_type == "Bool":
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object', 'bool']).columns)
      show_df_column = st.sidebar.checkbox("Show the Data Frame with the selected column")
      if show_df_column:
        st.write(df[categorical_column])
      choose_chart = st.selectbox(
          'Select a Chart',("Horizontal Bar Plot", "Vertical Bar Plot", "Pie Chart" ))
      choose_palette = st.selectbox('Pick a pallete', ("magma", "mako", "viridis", "rocket", "viridis_r", "rocket_r", "mako_r", "husl", "hls"))
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)
      df_category = df[categorical_column].value_counts().reset_index()
      df_category.columns = [categorical_column, "Frequency"]
      
      df_cat = df
      df_cat['count'] = 0
      df_cat = df_cat.groupby(categorical_column)['count'].count().reset_index()
      df_cat['proportion in %'] = df_cat['count'] / df_cat['count'].sum() * 100
      st.table(df_cat)

      if choose_chart == "Vertical Bar Plot":
        fig, ax = plt.subplots()
        sns.barplot(data = df_category, x = categorical_column, y = "Frequency", palette = choose_palette, alpha = choose_opacity)
        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)
        with open("plot.png", "rb") as file:
          btn = st.download_button(
            label="Download image",
            data=file,
            file_name="Figure.png",
            mime="image/png"
          )

      if choose_chart == "Horizontal Bar Plot":
        fig, ax = plt.subplots()
        sns.barplot(data = df_category, y = categorical_column, x = "Frequency", palette = choose_palette, alpha = choose_opacity)
        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)
        with open("plot.png", "rb") as file:
          btn = st.download_button(
            label="Download image",
            data=file,
            file_name="Figure.png",
            mime="image/png"
          )

      if choose_chart == "Pie Chart":
        fig, ax = plt.subplots()
        plt.pie(df_category["Frequency"], labels=df_category[categorical_column], colors = sns.color_palette(choose_palette, 5), autopct='%.0f%%')
        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)
        with open("plot.png", "rb") as file:
          btn = st.download_button(
            label="Download image",
            data=file,
            file_name="Figure.png",
            mime="image/png"
          )

          
