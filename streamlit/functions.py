import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import random
from scipy.stats import norm
import re

data = pd.read_csv('df2020.csv')
df2018 = pd.read_csv('df2018.csv')
full_data2018 = pd.read_csv('../Data/survey_results_public_2018.csv')
full_data2019=pd.read_csv('../Data/survey_results_public_2019.csv')
full_df2020 = pd.read_csv('../Data/survey_results_public_2020.csv')
df2019 = pd.read_csv('df2019.csv')
df2020 = data[(data['SalaryUSD'] < 200000)]

# features for job satisfaction
results = pd.read_csv("results.csv")


#######################################
# VISUALISATION STARTS
#######################################

######-Nikita-########

def plot_boxplot(data, x, y, title):
    fig = go.Figure()
    for group_name, group_data in data.groupby(x):
        fig.add_trace(go.Box(y=group_data[y], name=group_name))
    fig.update_layout(title=title, xaxis_title=x, yaxis_title=y)
    st.plotly_chart(fig)

#########################################################################    

def plot_bar_plotly(df, column_name, top_n=10, height=450, width=700):
    df_counts = df[column_name].value_counts().head(top_n).reset_index()
    df_counts.columns = [column_name, 'Count']
    
    fig = px.bar(df_counts, x=column_name, y='Count', 
                 labels={column_name: column_name, 'Count': 'Number of Developers'},
                 color=column_name, color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_layout(xaxis_title=column_name, yaxis_title='Number of Developers')
    fig.update_layout(height=height, width=width)

    return st.plotly_chart(fig)


def plot_pie_plotly(df, column_name,top_n=10,  height=400, width=400 ):
    participation_rate = df[column_name].value_counts().keys().tolist()[:top_n]
    count = df[column_name].value_counts().tolist()[:top_n]

    fig_pie = go.Figure(data=[go.Pie(labels=participation_rate, values=count)])
    fig_pie.update_layout(title='Top {} Distribution'.format(column_name))
    fig_pie.update_layout(height=height, width=width)

    st.plotly_chart(fig_pie)    

def plot_value_counts_plotly(df, column_name):
    colors = ['lightseagreen', 'lightgreen', 'lightyellow', 'lightcoral', 'lightsalmon', 'lavender']

    counts = df[column_name].value_counts()
    fig = go.Figure(go.Bar(x=counts.index, y=counts.values, marker_color=random.choice(colors)))
    fig.update_layout(title=f'Value Counts for {column_name}', xaxis_title='Response', yaxis_title='Count')
    return fig


def generate_normal_distribution_plots(df, column, top_n=10):
    countries = df[column].value_counts().sort_values(ascending=False)[:top_n].index.tolist()

    for country in countries:
        temp_salaries = df.loc[df[column] == country, 'SalaryUSD']

        #normal distribution curve
        x_values = np.linspace(temp_salaries.min(), temp_salaries.max(), 100)
        y_values = norm.pdf(x_values, temp_salaries.mean(), temp_salaries.std())

        fig = go.Figure(data=go.Scatter(x=x_values, y=y_values))
        
        # mean line
        fig.add_shape(type="line",
                      x0=temp_salaries.mean(), y0=0,
                      x1=temp_salaries.mean(), y1=norm.pdf(temp_salaries.mean(), temp_salaries.mean(), temp_salaries.std()),
                      line=dict(color="red", width=2, dash="dash"))

        fig.update_layout(title='Normal Distribution of Annual Salaries in {}'.format(country),
                          xaxis_title="Annual Salary in USD",
                          yaxis_title="Density")
        fig.update_layout(height=400, width=370)

        # st.plotly_chart(fig)
        yield fig


def plot_age_distribution(df, column_name):
    df['Age_range'] = np.where((df[column_name] >= 15) & (df[column_name] <= 19), '15 - 19 years', 'Age_unknown')
    df['Age_range'] = np.where((df[column_name] >= 20) & (df[column_name] <= 24), '20 - 24 years', df['Age_range'])
    df['Age_range'] = np.where((df[column_name] >= 25) & (df[column_name] <= 29), '25 - 29 years', df['Age_range'])
    df['Age_range'] = np.where((df[column_name] >= 30) & (df[column_name] <= 34), '30 - 34 years', df['Age_range'])
    df['Age_range'] = np.where((df[column_name] >= 35) & (df[column_name] <= 39), '35 - 39 years', df['Age_range'])
    df['Age_range'] = np.where((df[column_name] >= 40) & (df[column_name] <= 45), '40 - 45 years', df['Age_range'])
    df['Age_range'] = np.where((df[column_name] >= 46), '46 and above years', df['Age_range'])

    df_age = df.groupby(['Age_range']).size().reset_index(name='Count')
    df_age.sort_values(by=['Count'], ascending=False, inplace=True)

    # Plotly bar chart
    fig = go.Figure(data=go.Bar(
        x=df_age['Count'],
        y=df_age['Age_range'],
        orientation='h'
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Count',
        yaxis_title='Age Range',
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig)

def counts(df, column_name, year):
    language_counts = df[column_name].str.split(';', expand=True).stack().value_counts().to_frame(name=year)
    language_counts[column_name] = language_counts.index
    language_counts.reset_index(drop=True, inplace=True)
    language_counts = language_counts[[column_name, year]]
    return language_counts

def compare_column_and_plot(column):
    languagedesire_2018 = counts(df2018, column, '2018')
    languagedesire_2019 = counts(df2019, column, '2019')
    languagedesire_2020 = counts(df2020, column, '2020')

    # Merge language counts for both years
    languagedesire_all = pd.merge(languagedesire_2018, languagedesire_2019, on=column, how='outer')
    languagedesire_all = pd.merge(languagedesire_all, languagedesire_2020, on=column, how='outer')

    
    # Fill NaN values with 0 and convert counts to integers
    languagedesire_all.fillna(0, inplace=True)
    languagedesire_all['2018'] = languagedesire_all['2018'].astype(int)
    languagedesire_all['2019'] = languagedesire_all['2019'].astype(int)
    languagedesire_all['2020'] = languagedesire_all['2020'].astype(int)
    
    
    languagedesire_all.set_index(column, inplace=True)

    languagedesire19_20 = languagedesire_all.div(languagedesire_all.sum())

    st.write(languagedesire19_20.head(5))
    fig = go.Figure()

    for column in languagedesire19_20.columns:
        fig.add_trace(go.Bar(x=languagedesire19_20.index, y=languagedesire19_20[column], name=column))

    fig.update_layout(
        xaxis_title=column,
        yaxis_title='Percentages',
        font=dict(size=14),
        barmode='group',
        height=600,
        width=800
    )


    st.plotly_chart(fig)

def generate_choropleth(df, column_name):
    grouped_df = df.groupby('Country').size().reset_index(name='Respondents')

    # ISO country code from the country name
    def get_country_code(name):
        try:
            return pycountry.countries.lookup(name).alpha_3
        except LookupError:
            return None

    # Adding country code column
    grouped_df['Country_code'] = grouped_df['Country'].apply(get_country_code)

    #choropleth map
    fig = px.choropleth(grouped_df,
                        locations="Country_code",
                        color=column_name,
                        hover_name="Country",
                        projection="natural earth",
                        color_continuous_scale='Peach',
                        range_color=[0, 10000],
                        labels={column_name: 'Respondents'}
                        )
    fig.update_layout(height=600, width=900)
    return st.plotly_chart(fig)

def gender_vs_top5countries(df):
    all_data = df.groupby(['Country', 'Gender']).size().reset_index(name='Count')
    all_data['Total'] = all_data.groupby('Country')['Count'].transform('sum')
    all_data['Percentage'] = all_data['Count'] / all_data['Total'] * 100


    top_countries = all_data.groupby('Country')['Total'].max().nlargest(5).index
    top_data = all_data[all_data['Country'].isin(top_countries)]

    # men and women data
    men_data = top_data[top_data['Gender'] == 'Man']
    women_data = top_data[top_data['Gender'] == 'Woman']

    fig = go.Figure()

    #bars for 'Men'
    fig.add_trace(go.Bar(x=men_data['Country'], y=men_data['Percentage'], name='Men', marker_color='darkblue'))

    #bars for 'Women'
    fig.add_trace(go.Bar(x=women_data['Country'], y=women_data['Percentage'], name='Women', marker_color='#5E96E9'))

    fig.update_layout(
        title='Gender vs Top 5 Countries in 2019',
        xaxis_title='Top 5 Countries',
        yaxis_title='Percentage',
        barmode='group'
    )

    return fig
def heighest_paying_2019():
    ds = df2019[df2019['DevType'].str.contains('Data scientist') == True ]
    ds_mean_salary = ds.groupby('Country')['SalaryUSD'].mean().reset_index(name='Mean')
    ds_mean_salary.sort_values(by=['Mean'], ascending=False, inplace=True)
    ds_mean_salary = ds_mean_salary[(ds_mean_salary['Mean'] <= 280000)]
    Top_mean_salary = ds_mean_salary[:10]
    
    fig = px.bar(Top_mean_salary, x='Mean', y='Country', orientation='h',
                 labels={'Mean': 'Average Salary in US$', 'Country': 'Country'},
                 title='The Top 10 highest paying data scientist countries in 2019')
    
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, 
                      title={'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    st.plotly_chart(fig)
def heighest_paying(df):
    ds = df[df['DevType'].str.contains('Data scientist') == True ]
    ds_mean_salary = ds.groupby('Country')['SalaryUSD'].mean().reset_index(name='Mean')
    ds_mean_salary.sort_values(by=['Mean'], ascending=False, inplace=True)
    ds_mean_salary = ds_mean_salary[(ds_mean_salary['Mean'] <= 280000)]
    Top_mean_salary = ds_mean_salary[:10]
    
    fig = px.bar(Top_mean_salary, x='Mean', y='Country', orientation='h',
                 labels={'Mean': 'Average Salary in US$', 'Country': 'Country'},
                 title='The Top 10 highest paying data scientist countries ')
    
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, 
                      title={'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    st.plotly_chart(fig)
def plot_value_counts_plotly(column_name, df, column):
    values = df[column_name].value_counts()
    fig = go.Figure(data=[go.Bar(x=values.index, y=values.values, marker_color=random.choice(['lightseagreen', 'lightgreen', 'lightyellow', 'lightcoral', 'lightsalmon', 'lavender']))])
    fig.update_layout(title=f'Value Counts for {column_name}', xaxis_title='Response', yaxis_title='Count')
    column.plotly_chart(fig)

def ai_graphs():
    st.title('AI Survey Responses')
    df = full_data2018[['AIDangerous', 'AIInteresting', 'AIResponsible', 'AIFuture']]

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    short_mapping = {
        'Algorithms making important decisions': 'Algorithms',
        'Artificial intelligence surpassing human intelligence ("the singularity")': 'AI Singularity',
        'Evolving definitions of "fairness" in algorithmic versus human decisions': 'Fairness Evolution',
        "Increasing automation of jobs": 'Automation',
        "The developers or the people creating the AI": 'Developers',
        "A governmental or other regulatory body": 'Government/Regulatory',
        "Prominent industry leaders": 'Industry Leaders',
        "Nobody": 'No Responsibility',
        "I'm excited about the possibilities more than worried about the dangers.": 'Excited about AI Future',
        "I'm worried about the dangers more than I'm excited about the possibilities.": 'Worried about AI Future',
        "I don't care about it, or I haven't thought about it.": 'Indifferent about AI Future'
    }

    df.replace(short_mapping, inplace=True)

    col1, col2 = st.columns(2)

    plot_value_counts_plotly('AIDangerous', df, col1)
    plot_value_counts_plotly('AIInteresting', df, col1)
    plot_value_counts_plotly('AIResponsible', df, col2)
    plot_value_counts_plotly('AIFuture', df, col2)   


def result_plot(data):
    new_index = data.Rates.sort_values(ascending=False).index
    sorted_results = data.reindex(new_index)

    filtered_results = sorted_results[np.abs(sorted_results.Rates) > 0.1]

    #Plotly figure
    fig = px.bar(
        filtered_results,
        x='Rates',
        y='Columns',
        orientation='h',
        labels={'Rates': 'Negative and Positive Features', 'Columns': 'Features'},
    )

    fig.update_layout(
        xaxis_title='Negative and Positive Features',
        yaxis_title='Features',
        title_font_size=25,
        xaxis_title_font_size=25,
        yaxis_title_font_size=25,
        height=800,
    )

    st.plotly_chart(fig, use_container_width=True)
