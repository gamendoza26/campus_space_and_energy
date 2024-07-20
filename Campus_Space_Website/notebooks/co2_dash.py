import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output
import os

# Function to process CSV files
def process_files(file_list, timestamp_col, date_format=None):
    data_frames = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            if date_format:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], format=date_format, errors='coerce')
            else:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
            df = df.dropna(subset=[timestamp_col])
            data_frames.append(df)
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
    if not data_frames:
        raise ValueError("No valid data frames were created. Check your input files.")
    combined_df = pd.concat(data_frames, ignore_index=True)
    return combined_df.sort_values(by=timestamp_col)

# Function to create visualizations
def create_visualizations(date, room_volume):
    # Lists of file paths and date formats
    occupancy_files = [
        ('./resources/CO2_occupancy_data/20th_CO2_occupancy_data.csv', '%m/%d/%Y %H:%M'),
        ('./resources/CO2_occupancy_data/24th_occupancy_data - Sheet1.csv', '%m-%d-%Y %H:%M:%S'),
        ('./resources/CO2_occupancy_data/25th_Co2_occupancy_data - Sheet1.csv', '%m-%d-%Y %H:%M:%S')
    ]
    co2_pi1_files = [
        './resources/CO2_data/co2_data_24th_pi1.csv',
        './resources/CO2_data_25th_pi1.csv',
        './resources/CO2_data/co2_data_pi1.csv'
    ]
    co2_pi2_files = [
        './resources/CO2_data/co2_data_24th_pi2.csv',
        './resources/CO2_data/co2_data_25th_pi2.csv',
        './resources/CO2_data/co2_data.csv'
    ]

    # Process occupancy files with their respective date formats
    occupancy_data = []
    for file, fmt in occupancy_files:
        occupancy_data.append(process_files([file], 'Time', fmt))
    occupancy = pd.concat(occupancy_data, ignore_index=True).sort_values(by='Time')

    # Process CO2 files
    co2_pi1 = process_files(co2_pi1_files, 'timestamp')
    co2_pi2 = process_files(co2_pi2_files, 'timestamp')

    # Merge data
    co2_data = pd.merge_asof(co2_pi1, co2_pi2, on='timestamp', suffixes=('_pi1', '_pi2'))
    merged_data = pd.merge_asof(co2_data, occupancy, left_on='timestamp', right_on='Time')

    # Calculate average CO2 and CO2 per volume
    merged_data['co2_avg'] = (merged_data['co2_pi1'] + merged_data['co2_pi2']) / 2
    merged_data['co2_avg_per_volume'] = merged_data['co2_avg'] / room_volume

    # Check if there is data for the selected date
    selected_date = pd.to_datetime(date).date()
    if not any(merged_data['timestamp'].dt.date == selected_date):
        print(f"Sorry, we don't have data for {date}")
        return

    # Boxplot of CO2 concentration distribution by occupancy (using all data)
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='count', y='co2_avg_per_volume', data=merged_data)
    plt.xlabel('Occupancy')
    plt.ylabel('Average CO2 per Volume (ppm/m^3)')
    plt.title('CO2 Concentration Distribution by Occupancy')
    plt.tight_layout()
    plt.show()

    # Filter for the selected date for heatmap
    filtered_data = merged_data[merged_data['timestamp'].dt.date == selected_date]

    # CO2 Heatmap (for the specified date)
    pivot_data = filtered_data.pivot_table(
        values='co2_avg_per_volume', 
        index=filtered_data['timestamp'].dt.floor('15min').dt.time, 
        columns=filtered_data['timestamp'].dt.hour,
        aggfunc='mean'
    )
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_data, cmap='YlOrRd', cbar_kws={'label': 'Average CO2 per Volume (ppm/m^3)'})
    plt.xlabel('Hour of Day')
    plt.ylabel('15-Minute Interval')
    plt.title(f'CO2 Levels Heatmap on {date}')
    plt.tight_layout()
    plt.show()

# Widgets for user input
room_selector = widgets.ToggleButtons(
    options=[('Room 133', 33.6475), ('Room 127', 334.40298596)],
    description='Select Room:'
)
date_picker = widgets.DatePicker(description='Select Date')
generate_button = widgets.Button(description='Generate Graph', button_style='success')

output = widgets.Output()

def display_co2_options():
    generate_button.on_click(on_generate_button_clicked)
    display(room_selector, date_picker, generate_button, output)

def on_generate_button_clicked(b):
    with output:
        output.clear_output()
        selected_room_volume = room_selector.value
        selected_date = date_picker.value
        if selected_room_volume and selected_date:
            create_visualizations(selected_date.strftime('%Y-%m-%d'), selected_room_volume)
        else:
            print("Please select both a room and a date.")
