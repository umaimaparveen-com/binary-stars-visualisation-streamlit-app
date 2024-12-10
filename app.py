import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to get a single star data from user input
def get_star_data():
    st.title("Welcome to Stellar System HR Diagram Plotting!")
    
    star_name = st.text_input("Enter the star name:", key="star_name")
    if star_name:
        log_teff = st.number_input(f"Enter Log Teff for {star_name}:", format="%.2f", key="log_teff")
        log_l = st.number_input(f"Enter Log L for {star_name}:", format="%.2f", key="log_l")
        return star_name, log_teff, log_l
    return None

# Function to plot data for multiple metallicities
def plot_multiple_metallicities(df, metallicity_value, star_data):
    if star_data is None:
        st.warning("Please enter star data to plot.")
        return

    # Initialize figure for the current metallicity
    fig = go.Figure()

    # Check that 'mass', 'Log Teff', and 'Log L' columns exist in the dataframe
    if 'mass' not in df.columns or '"Log Teff"' not in df.columns or '"Log L"' not in df.columns:
        st.error("Columns 'mass', 'Log Teff', or 'Log L' not found in the DataFrame.")
        return

    # Add data for different mass values
    unique_mass = df['mass'].unique()
    for mass in unique_mass:
        group = df[df['mass'] == mass]
        fig.add_trace(go.Scatter(
            x=group['"Log Teff"'],
            y=group['"Log L"'],
            mode='lines',
            name=f'Mass: {mass} M',
            marker=dict(size=10)
        ))

    # Plot the user-defined star
    star_name, log_teff, log_l = star_data
    fig.add_trace(go.Scatter(
        x=[log_teff],
        y=[log_l],
        mode='markers+text',
        name=star_name,
        text=[star_name],
        textposition='top center',
        marker=dict(size=12, symbol='circle', color='red')  # Customize marker style
    ))

    # Add labels, title, and customize layout
    fig.update_layout(
        title=f'Log L vs Log Teff for Mass Values from 0.4 to 7.0 with Metallicity= {metallicity_value}',
        xaxis_title='Log Teff',
        yaxis_title='Log L',
        legend_title='Mass Values',
        showlegend=True,
        xaxis=dict(autorange='reversed')
    )

    # Show the plot for the current metallicity
    st.plotly_chart(fig)

# Main app
def main():
    st.title("Star Data Visualization")

    # Collect star data from the user
    star_data = get_star_data()

    if star_data:
        try:
            # Define DataFrames and their corresponding metallicity values
            df_008 = pd.read_csv('filtered_df_0.008.csv')  # Your DataFrame for metallicity 0.008
            df_019 = pd.read_csv('filtered_df_0.019.csv')  # Your DataFrame for metallicity 0.019
        except FileNotFoundError:
            st.error("One or more CSV files not found. Please ensure 'filtered_df_0.008.csv' and 'filtered_df_0.019.csv' are in the same folder.")
            return

        dataframes = [df_008, df_019]
        metallicity_values = [0.008, 0.019]

        # Iterate over DataFrames and their corresponding metallicity values and plot the data
        for df, metallicity_value in zip(dataframes, metallicity_values):
            plot_multiple_metallicities(df, metallicity_value, star_data)

# Run the main app
if __name__ == "__main__":
    main()
