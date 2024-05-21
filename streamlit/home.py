import streamlit as st
import pandas as pd
import functions as ff
import main_analysis as main
import random

#######################################
# FUNCTIONS
#######################################

def load_data(year):
    if year == '2018':
        df = pd.read_csv('df2018.csv').drop(columns=['Unnamed: 0'])
        full_data = pd.read_csv('../Data/survey_results_public_2018.csv')
        full_data.rename(columns={
            "Hobby": "Hobbyist",
            "RaceEthnicity": "Ethnicity",
            "YearsCoding": "YearsCode",
            "YearsCodingProf": "YearsCodePro",
            "JobSatisfaction": "JobSat",
            "FormalEducation": "EdLevel",
            "OperatingSystem": "OpSys",
            'ConvertedSalary': 'SalaryUSD'
        }, inplace=True)
        df['Gender'] = df['Gender'].replace({"Male": "Man", "Female": "Woman"})
    elif year == '2019':
        df = pd.read_csv('df2019.csv').drop(columns=['Unnamed: 0'])
        full_data = pd.read_csv('../Data/survey_results_public_2019.csv')
    else:
        df = pd.read_csv('df2020.csv')
        df = df[df['SalaryUSD'] < 200000]
        full_data = pd.read_csv('../Data/survey_results_public_2020.csv')
    return df, full_data

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_analysis_text(title, text):
    analysis_text = f"""
    <div style='margin-top: 400px !important' class='analysis-container'>
        <div class='analysis-title'>{title}</div>
        <div class='analysis-text'>{text}</div>
    </div>
    """
    st.markdown(analysis_text, unsafe_allow_html=True)

def display_highest_paying_countries(year):
    visual, analysis = st.columns((3, 1))
    with visual:
        st.title("Highest Paying Countries for Data Scientists")
        if year == '2018':
            ff.heighest_paying(full_data)
        elif year == '2019':
            ff.heighest_paying_2019()
        else:
            ff.heighest_paying(df)
    with analysis:
        display_analysis_text(
            "Analysis: Data Scientist Market",
            "The top three countries which have a highest mean annual salary of a data scientist are "
            "South Korea (253,315) in 2018, Ireland (275,851) in 2019, and the USA (118,863) in 2020. "
            "Apart from that, the mean salary of the rest of the countries is less than 200,000 per year. "
            "Japan provides the highest mean annual salary among Asian countries (118,969). Figures in Dollars $."
        )

def display_ai_analysis():
    ff.ai_graphs()
    ai_text = """
    <div style='margin-top: 400px !important' class='analysis-container-extra'>
        <div class='analysis-title'>Analysis: AI Perception</div>
        <div class='analysis-text'>
            1. <b>AIDangerous</b>: The most commonly cited concern is "Algorithms making important decisions," 
            followed closely by "Artificial intelligence surpassing human intelligence" and "Evolving definitions of fairness."
            "Increasing automation of jobs" is also a significant concern but appears to be less frequently mentioned compared to the other categories.
            2. <b>AIInteresting</b>: The most interesting aspect for respondents seems to be "Increasing automation of jobs," 
            followed by "Algorithms making important decisions" and "Artificial intelligence surpassing human intelligence."
            "Evolving definitions of fairness" appears to be less intriguing to respondents compared to other categories.  
            3. <b>AIResponsible</b>: The majority of respondents believe that responsibility lies with "The developers or the people creating the AI."
            Fewer respondents attribute responsibility to "A governmental or other regulatory body," "Prominent industry leaders," or "Nobody."
            4. <b>AIFuture</b>: A significant proportion of respondents express excitement about the future of AI, indicating that they are 
            "Excited about the possibilities more than worried about the dangers." However, there is also a notable percentage of respondents who are 
            "Worried about the dangers more than excited about the possibilities." A smaller portion of respondents either "Don't care about it" or "Haven't thought about it."
            5. Overall, these results suggest a complex and varied perspective on AI technology. While many see great potential in AI, there are also concerns about its implications, 
            particularly regarding decision-making, automation of jobs, and the ethical considerations surrounding its development and regulation.
        </div>
    </div>
    """
    st.markdown(ai_text, unsafe_allow_html=True)

def display_visualizations(year, full_data):
    if year == '2018':
        visual, analysis = st.columns((3, 1))
        with visual:
            st.title("Operating System")
            ff.plot_pie_plotly(full_data, 'OpSys')
        with analysis:
            display_analysis_text(
                "Analysis: Data Scientist Market",
                "Windows is the dominating operating system used by people. OS and Linux are almost tied. "
                "The knowledge about the operating system can help developers decide to whom their audience is catered towards."
            )

        visual, analysis = st.columns((3, 1))
        with visual:
            st.title("Top IDEs")
            ff.plot_bar_plotly(full_data, "IDE", 10, 500, 800)
            ff.plot_pie_plotly(full_data, "IDE", 10, 550, 600)
        with analysis:
            display_analysis_text(
                "Analysis: Popular IDEs",
                "1. <b>Popular IDEs</b>: Visual Studio Code, Visual Studio, and Notepad++ are among the most widely used IDEs, "
                "with high user counts ranging from 25,870 to 26,280."
                "2. <b>Text Editors</b>: Sublime Text, Vim, and IntelliJ are also popular choices, with user counts ranging from 19,477 to 21,810."
                "3. <b>General-purpose Editors</b>: TextMate, Coda, and Light Table are also used, although they have lower user counts compared to other IDEs."
                "4. <b>Emerging Trends</b>: IPython / Jupyter, Atom, and Emacs show significant adoption, indicating a growing interest in interactive computing environments, lightweight editors, and customizable text editors, respectively."
                "5. <b>Industry Standard</b>: Xcode, primarily used for macOS and iOS development, maintains a substantial user base due to its integration with Apple's development ecosystem."
            )
        display_ai_analysis()

#######################################
# MAIN SCRIPT
#######################################

st.set_page_config(layout='wide')
local_css("style.css")

year = st.sidebar.selectbox('Select Year', ['2018', '2019', '2020'])
df, full_data = load_data(year)

main.main_analysis(df)
display_highest_paying_countries(year)
display_visualizations(year, full_data)
