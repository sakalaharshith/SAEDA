import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go

st.markdown('''
    ### Welcome to :rainbow[SAEDA]: *SEMI AUTOMATED EXPLORATORY DATA ANALYSIS*''')
uploaded_file = st.file_uploader("Please upload a CSV file :seedling:",type=['csv'],key='csvfile')

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    total_number_of_cells_shape=dataframe.shape
    total_number_of_cells=total_number_of_cells_shape[0]*total_number_of_cells_shape[1]
    print(total_number_of_cells)
    st.write(dataframe.head())
    option = st.selectbox(
    '#### :rainbow[Please select the ouput label or column here.]', dataframe.columns, placeholder='Please select an output column')
    st.write("#### selected output label is {options}".format(options=option))

    st.write('## :blue[OVERVIEW]')
    container = st.container(border=True)
    container.write("##### Number of columns: :green[{column}]".format(column=len(dataframe.columns)))
    container.write("##### Number of observations: :green[{rows}]".format(rows=len(dataframe)))
    container.write("##### Total number of null values in the dataset: :green[{n}]".format(n=sum(dataframe.isna().sum()[0:])))
    container.write('##### Total number of empty(empty string) values in the dataset: :green[{empty}]'.format(empty=sum(dataframe.eq('').sum(axis=1))))
    container.write('##### Total number of missing or invalid values in the dataset: :green[{missing}]'.format(missing=sum(dataframe.isna().sum()[0:])+sum(dataframe.eq('').sum(axis=1))))
    missing_value_proportion=((sum(dataframe.isna().sum()[0:])+sum(dataframe.eq('').sum(axis=1)))/total_number_of_cells)*100
    container.write('##### Total number of missing values in proportion to total data cells: :green[{missing}%]'.format(missing=round(missing_value_proportion,3)))

    st.write('## :blue[VARIABLES]')
    
    variable = st.selectbox(
    '#### :rainbow[Please select a variable to generate variable statistics.]', dataframe.columns, placeholder='Please select a variable')
    
    container=st.container(border=True)
    if(dataframe[variable].dtype !='object'):
        container.write('##### Variable name: :green[{var}]'.format(var=variable))
        container.write('##### Variable Datatype: :green[{var}]'.format(var=dataframe[variable].dtype))
        container.write('##### Number of distinct values: :green[{var}]'.format(var=len(dataframe[variable].unique())))
        unique_value_per=((dataframe[variable].nunique())/len(dataframe[variable]))*100
        container.write('##### Proportion of unique values: :green[{var}]'.format(var=round(unique_value_per,3)))
        missing_value_num=(sum(dataframe[[variable]].isna().sum()[0:])+sum(dataframe[[variable]].eq('').sum(axis=1)))
        container.write('##### Number of missing values: :green[{var}]'.format(var=missing_value_num))
        missing_value_prop=((sum(dataframe[[variable]].isna().sum()[0:])+sum(dataframe[[variable]].eq('').sum(axis=1)))/total_number_of_cells)*100
        container.write('##### Proportion of missing values to entire column: :green[{var}]'.format(var=round(missing_value_prop,3)))
        tab1, tab2= st.tabs(['Statistics','Data Distribution'])


        with tab1:
            container=st.container(border=True)
            container.header(":blue[QUANTILE STATISTICS]")

            container.write('##### Minimum value: :green[{var}]'.format(var=dataframe[variable].min()))
            first_quartile=np.percentile(dataframe[variable],25)
            container.write('##### First Quartile value: :green[{var}]'.format(var=first_quartile))
            container.write('##### Median of the distribution: :green[{var}]'.format(var=dataframe[variable].median(skipna=True)))
            second_quartile=np.percentile(dataframe[variable],75)
            container.write('##### Second Quartile value: :green[{var}]'.format(var=second_quartile))
            container.write('##### Inter Quartile range: :green[{var}]'.format(var=second_quartile-first_quartile))
            container.write('##### Maximum value: :green[{var}]'.format(var=dataframe[variable].max()))
            container.write('##### Data spread(standard deviation): :green[{var}]'.format(var=dataframe[variable].std()))
            container.write('##### Quartile Deviation: :green[{var}]'.format(var=(second_quartile-first_quartile)/2))
            container.header(":blue[DESCRIPTIVE STATISTICS]")
            standard_deviation_var=dataframe[variable].std(ddof=1)
            mean_var=dataframe[variable].mean()
            container.write('##### Mean: :green[{var}]'.format(var=mean_var))
            container.write('##### Standard Deviation: :green[{var}]'.format(var=standard_deviation_var))
            container.write('##### Coefficient of variation: :green[{var}]'.format(var=(standard_deviation_var/mean_var)*100))
            container.write('##### Skewness: :green[{var}]'.format(var=dataframe[variable].skew()))
            container.write('##### Kurtosis: :green[{var}]'.format(var=dataframe[variable].kurtosis()))


            
        with tab2:
            container=st.container(border=True)
            container.header(":blue[DATA DISTRIBUTIONS]")
            fig = px.histogram(dataframe, x=variable,color_discrete_sequence=['yellow'],text_auto=True).update_layout(title='Distribution of {var}'.format(var=variable))
            fig.update_layout(bargap=0.1)
            container.plotly_chart(fig,theme="streamlit", use_container_width=True)
            fig = px.box(dataframe, y=variable,color_discrete_sequence=['yellow'])
            container.plotly_chart(fig,theme='streamlit',use_container_width=True)
    else:
        container=st.container(border=True)
        container.warning('The threshold set for cardinality is 2% of total dataset size. ', icon="⚠️")
        cardinality_threshold=(len(dataframe)*2)/100
        if(dataframe[variable].nunique()<=cardinality_threshold):
            container.write('##### Cardinality: :green[{var}]'.format(var='Low Cardinality'))
        if(dataframe[variable].nunique()>cardinality_threshold):
            container.write('##### Cardinality: :red[{var}]'.format(var='High Cardinality'))
        unique_values_var=len(dataframe[variable].unique())
        unique_value_per=round((unique_values_var/len(dataframe[variable]))*100,2)
        if unique_values_var<=cardinality_threshold:
            container.write('##### Unique values: :green[{var}]'.format(var=unique_values_var))
            container.write('##### Unique values prop: :green[{var}%]'.format(var=unique_value_per))
        if unique_values_var>cardinality_threshold:
            container.write('##### Unique values: :red[{var}]'.format(var=unique_values_var))
            container.write('##### Unique values prop: :red[{var}%]'.format(var=unique_value_per))
        missing_value_num=(sum(dataframe[[variable]].isna().sum()[0:])+sum(dataframe[[variable]].eq('').sum(axis=1)))
        missing_value_prop=((sum(dataframe[[variable]].isna().sum()[0:])+sum(dataframe[[variable]].eq('').sum(axis=1)))/len(dataframe[variable]))*100
        if (missing_value_prop<=25):
            container.write('##### Missing values: :green[{var}]'.format(var=missing_value_num))
            container.write('##### Missing values prop: :green[{var}%]'.format(var=missing_value_prop))
        if(missing_value_prop>25):
            container.write('##### Missing values: :red[{var}]'.format(var=missing_value_num))
            container.write('##### Missing values : :red[{var}%]'.format(var=missing_value_prop))
        hist_variable=px.histogram(dataframe, x=variable,color_discrete_sequence=['yellow'])
        container.plotly_chart(hist_variable,theme='streamlit',use_container_width=True)
    container_bivariate=st.container(border=True)
    container_bivariate.header(":blue[BI-VARIATE ANALYSIS]")
    columns_list=dataframe.columns.tolist()
    columns_list.remove(option)
    if len(columns_list)>10:
        select_box_variable=container_bivariate.selectbox("Select the Independent variable to analyze: ", columns_list[:])
        dependent_variable_dtype=dataframe[option].dtype
        independen_variable_dtype=dataframe[select_box_variable].dtype
        if ((independen_variable_dtype=='int64') or (independen_variable_dtype=='float64')) and \
           ((dependent_variable_dtype=='object')or(dependent_variable_dtype=='bool')):
            fig = px.box(dataframe, x=dataframe[option], y=dataframe[select_box_variable], color=dataframe[option],color_discrete_sequence=['yellow'],title='BOX PLOT BETWEEN {x} and {y}'.format(x=option,y=select_box_variable))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
            fig = px.bar(dataframe, x=option, y=select_box_variable,color_discrete_sequence=['yellow'],title='BAR CHART BETWEEN {x} and {y}'.format(x=option,y=select_box_variable))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
            fig = px.bar(dataframe, x=dataframe.groupby(option)[option].count().index.tolist(), y=dataframe.groupby(option)[select_box_variable].count(),color_discrete_sequence=['yellow'])
            fig.update_layout(xaxis_title=select_box_variable,yaxis_title=option, title='COUNT PLOT BETWEEN {x} and {y}'.format(x=option,y=select_box_variable))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)

        if ((independen_variable_dtype=='int64') or (independen_variable_dtype=='float64'))and \
           ((dependent_variable_dtype=='int64') or (dependent_variable_dtype=='float64')):
            fig=px.scatter(dataframe,x=dataframe[select_box_variable],y=dataframe[option],color_discrete_sequence=['yellow'],title='SCATTER PLOT BETWEEN {x} and {y}'.format(x=select_box_variable,y=option))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
            fig = px.line(dataframe, x=select_box_variable, y=option,color_discrete_sequence=['yellow'] ,title='LINE PLOT BETWEEN {x} and {y}'.format(x=select_box_variable,y=option))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
        if (independen_variable_dtype=='object')and \
           (dependent_variable_dtype=='object'):
            cont_table = pd.crosstab(dataframe[option], dataframe[select_box_variable])
            container_bivariate.write(cont_table)
            #heatmap=sns.heatmap(dataframe.groupby([option, select_box_variable]).size().unstack(fill_value=0), cmap='YlGnBu')
            heatmap_df=dataframe.groupby([option, select_box_variable]).size().unstack(fill_value=0)
            fig1=px.imshow(heatmap_df)
            container_bivariate.plotly_chart(fig1, theme="streamlit",use_container_width=True)
        
        if ((independen_variable_dtype=='object') and (dependent_variable_dtype=='int64') or (dependent_variable_dtype=='float64') or (dependent_variable_dtype=='bool')):
            fig = px.box(dataframe, x=dataframe[select_box_variable], y=dataframe[option], color=dataframe[option],color_discrete_sequence=['yellow'],title='BOX PLOT BETWEEN {x} and {y}'.format(x=select_box_variable,y=option))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
            fig = px.bar(dataframe, x=select_box_variable, y=option,color_discrete_sequence=['yellow'],title='BAR CHART BETWEEN {x} and {y}'.format(x=select_box_variable,y=option))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
            fig = px.bar(dataframe, x=dataframe.groupby(select_box_variable)[select_box_variable].count().index.tolist(), y=dataframe.groupby(select_box_variable)[option].count(),color_discrete_sequence=['yellow'])
            fig.update_layout(xaxis_title=select_box_variable,yaxis_title=option, title='COUNT PLOT BETWEEN {x} and {y}'.format(x=select_box_variable,y=option))
            container_bivariate.plotly_chart(fig,theme='streamlit',use_container_width=True)
            

            
            


            


    

    




