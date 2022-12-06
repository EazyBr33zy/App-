import streamlit as st
import pandas as pd
import base64
import numpy as np

st.title('Football Data App')
#st.subheader('Data Source')
#st.subheader('https://www.football-data.co.uk/')

st.sidebar.header('Leagues')
selected_league = st.sidebar.selectbox('League', ['England','Scotland','Germany','Italy','Spain','France','Netherlands','Belgium','Portugal','Turkey','Greece'])

st.sidebar.header('Season')
selected_year = st.sidebar.selectbox('Year', ['2022/2023', '2021/2022', '2020/2021',  '2019/2020',  '2018/2019', '2017/2018',  '2016/2017', '2015/2016', '2014/2015', '2013/2014', '2012/2013', '2011/2012', '2010/2011'])

# Web scraping
# https://www.football-data.co.uk/mmz4281/2223/E0.csv
@st.cache
def load_data(league, year):
    if selected_league == 'England':
        league = 'E0'
    if selected_league == 'Scotland':
        league = 'SC1'
    if selected_league == 'Germany':
        league = 'D1'
    if selected_league == 'Italy':
        league = 'I1'
    if selected_league == 'Spain':
        league = 'SP1'
    if selected_league == 'France':
        league = 'F1'
    if selected_league == 'Netherlands':
        league = 'N1'
    if selected_league == 'Belgium':
        league = 'B1'
    if selected_league == 'Portugal':
        league = 'P1'
    if selected_league == 'Turkey':
        league = 'T1'
    if selected_league == 'Greece':
        league = 'G1'

    if selected_year == '2010/2011':
        year = '1011'
    if selected_year == '2011/2012':
        year = '1112'
    if selected_year == '2012/2013':
        year = '1213'
    if selected_year == '2013/2014':
        year = '1314'
    if selected_year == '2014/2015':
        year = '1415'
    if selected_year == '2015/2016':
        year = '1516'
    if selected_year == '2016/2017':
        year = '1617'
    if selected_year == '2017/2018':
        year = '1718'
    if selected_year == '2018/2019':
        year = '1819'
    if selected_year == '2019/2020':
        year = '1920'
    if selected_year == '2020/2021':
        year = '2021'
    if selected_year == '2021/2022':
        year = '2122'
    if selected_year == '2022/2023':
        year = '2223'
    
    url = "https://www.football-data.co.uk/mmz4281/" + str(year) + "/" + league + ".csv"
    data = pd.read_csv(url)
    # data = data[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A']]
    # data.columns = ['Date', 'Home', 'Away', 'Goals_H', 'Goals_A', 'Result', 'Odd_H', 'Odd_D', 'Odd_A']
    # data.dropna(inplace=True)
    data.reset_index(inplace=True, drop=True)
    data.index = data.index.set_names(['Nº'])
    data = data.rename(index=lambda x: x + 1)
    return data
df = load_data(selected_league, selected_year)

# Sidebar - Columns selection
sorted_unique_column = df.columns.to_list()
selected_column = st.sidebar.multiselect('Columns', sorted_unique_column, ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A'])

# Sidebar - Team selection
sorted_unique_team = sorted(df.HomeTeam.unique())
selected_team = st.sidebar.multiselect('Teams', sorted_unique_team, sorted_unique_team)

# Filtering data
df_filtered = df[(df.HomeTeam.isin(selected_team))]
df_filtered = df_filtered[selected_column]

st.subheader('DataFrame - '+selected_league)
st.dataframe(df_filtered)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="dataframe.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_filtered), unsafe_allow_html=True)
