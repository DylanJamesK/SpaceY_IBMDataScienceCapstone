# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboardssssss',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                        dcc.Dropdown(id='site-dropdown',
                                                    options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    ],
                                                    value='ALL',
                                                    placeholder="Select a Launch Site here",
                                                    searchable=True
                                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                    1000: '1000',
                                    2000: '2000',
                                    3000: '3000',
                                    4000: '4000',
                                    5000: '5000',
                                    6000: '6000',
                                    7000: '7000',
                                    8000: '8000',
                                    9000: '9000',
                                    10000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # Filter the dataframe for successful launches only (class == 1)
        success_df = spacex_df[spacex_df['class'] == 1]
        
        # Group by launch site and count the number of successful launches per site
        success_count = success_df.groupby('Launch Site').size().reset_index(name='counts')
        
        # Create the pie chart showing total success launches per site
        fig = px.pie(success_count, 
                     values='counts', 
                     names='Launch Site', 
                     title='Total Successful Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        # filter the dataframe for the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # create a pie chart showing success (class=1) and failure (class=0) counts
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for Site {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Callback for updating the scatter plot based on dropdown and slider input
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, selected_payload_range):
    # Filter the dataframe based on the payload range
    low, high = selected_payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    # If ALL sites are selected
    if selected_site == 'ALL':
        # Scatter plot showing payload vs success, color by booster version
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites',
                         labels={'class': 'Launch Outcome (1=Success, 0=Failure)'})
        return fig
    else:
        # Filter the dataframe for the selected launch site
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        
        # Scatter plot showing payload vs success for the selected site, color by booster version
        fig = px.scatter(site_filtered_df, 
                         x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for Site {selected_site}',
                         labels={'class': 'Launch Outcome (1=Success, 0=Failure)'})
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
