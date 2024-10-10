import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache
def load_data():
    data = pd.read_csv(r'C:\Users\bolle\Downloads\KODE Labs - Data Analyst Aug2024\occupancy.csv')
    data['date_time'] = pd.to_datetime(data['date_time'])
    data['hour'] = data['date_time'].dt.hour
    data['weekday'] = data['date_time'].dt.day_name()
    data['capacity_utilization'] = data['occupancy'] / data['capacity'] * 100  # Calculate capacity utilization
    return data


def main():
    st.title('Building Occupancy Dashboard')
    data = load_data()

    
    st.sidebar.header('Select Options')
    building = st.sidebar.selectbox('Choose a Building', options=data['building_name'].unique())
    analysis_type = st.sidebar.radio('Choose Analysis Type', (
        'Trends Over Time', 'Occupancy by Time of Day', 'Occupancy by Weekday',
        'Capacity Utilization', 'Inflow and Outflow Analysis', 'Occupancy Anomalies'))

    
    if analysis_type == 'Trends Over Time':
        st.header('1. Occupancy Trends Over Time')
        fig = plot_trends(data, building)
        st.plotly_chart(fig)

   
    elif analysis_type == 'Occupancy by Time of Day':
        st.header('2. Occupancy Variation by Time of Day')
        fig = plot_time_of_day(data, building)
        st.plotly_chart(fig)

   
    elif analysis_type == 'Occupancy by Weekday':
        st.header('3. Occupancy by Weekday')
        fig = plot_weekday_occupancy(data)
        st.plotly_chart(fig)

    
    elif analysis_type == 'Capacity Utilization':
        st.header('4. Capacity Utilization')
        fig = plot_capacity_utilization(data, building)
        st.plotly_chart(fig)

    
    elif analysis_type == 'Inflow and Outflow Analysis':
        st.header('5. Inflow and Outflow Analysis')
        fig = plot_inflow_outflow(data, building)
        st.plotly_chart(fig)

    
    elif analysis_type == 'Occupancy Anomalies':
        st.header('6. Detecting Occupancy Anomalies')
        fig = plot_anomalies(data)
        st.plotly_chart(fig)


def plot_trends(data, building):
    filtered_data = data[data['building_name'] == building]
    fig = px.line(filtered_data, x='date_time', y='occupancy', title=f'Occupancy Trends for {building}')
    return fig


def plot_time_of_day(data, building):
    filtered_data = data[data['building_name'] == building]
    fig = px.histogram(filtered_data, x='hour', y='occupancy', title=f'Occupancy by Hour in {building}', histfunc='avg')
    return fig


def plot_weekday_occupancy(data):
    fig = px.bar(data, x='weekday', y='occupancy', title='Weekly Occupancy Trends', color='building_name', barmode='group')
    return fig


def plot_capacity_utilization(data, building):
    filtered_data = data[data['building_name'] == building]
    fig = px.bar(filtered_data, x='date_time', y='capacity_utilization', title=f'Capacity Utilization for {building}')
    return fig


def plot_inflow_outflow(data, building):
    filtered_data = data[data['building_name'] == building]
    fig = px.line(filtered_data, x='date_time', y=['people_in', 'people_out'], title=f'Inflow and Outflow Analysis for {building}')
    return fig


def plot_anomalies(data):
    fig = px.scatter(data, x='date_time', y='occupancy', title='Occupancy Anomalies', color='occupancy', size='occupancy', hover_data=['building_name', 'space_name'])
    return fig

if __name__ == '__main__':
    main()
