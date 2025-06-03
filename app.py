# app.py
from flask import Flask, render_template, request, jsonify
from pages.plot_functions import plot_bird_movement_with_legend, plot_all_birds_unique_colors, plot_combined_movement,generate_plot,calculate_total_distance_by_bird
from pages.data_loader import geo_df, map_options, cluster_df, bird_data
from pages.plot_functions import plot_migration_path
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import requests

app = Flask(__name__)

@app.route('/visualize')
def index():
    birds = geo_df['individual-local-identifier'].unique()
    years = sorted(geo_df['year'].unique())
    months = sorted(geo_df['month_name'].unique())
    basemaps = list(map_options.keys())

    return render_template('analysis.html', birds=birds, years=years, months=months, basemaps=basemaps)

@app.route('/plot', methods=['POST'])
def plot():
    data = request.json
    section = data['section']

    if section == 'section1':
        bird_id = data['bird_id']
        basemap = data['basemap']
        return jsonify(plot_bird_movement_with_legend(bird_id, basemap))

    elif section == 'section2':
        year = int(data['year'])
        month = data['month']
        basemap = data['basemap']
        return jsonify(plot_all_birds_unique_colors(year, month, basemap))

    elif section == 'section3':
        bird_id = data['bird_id']
        year = int(data['year'])
        month = data['month']
        basemap = data['basemap']
        return jsonify(plot_combined_movement(bird_id, year, month, basemap))

    return jsonify({'error': 'Invalid section'})

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clustervisualize')
def cluster_visualize():
    clusters = cluster_df['cluster'].unique()
    identifiers = cluster_df['individual-local-identifier'].unique()  # Get unique identifiers
    return render_template('cluster_analysis.html', clusters=clusters, identifiers=identifiers)

@app.route('/plot_clusters', methods=['POST'])
def plot_clusters_route():
    # Create the plot for clusters
    fig = go.Figure()

    unique_clusters = cluster_df['cluster'].unique()
    color_palette = [
        'red', 'blue', 'green', 'purple', 'orange', 'pink', 
        'cyan', 'magenta', 'yellow', 'brown'
    ]

    for i, cluster in enumerate(unique_clusters):
        cluster_data = cluster_df[cluster_df['cluster'] == cluster]
        
        fig.add_trace(go.Scattermapbox(
            lat=cluster_data['location-lat'],
            lon=cluster_data['location-long'],
            mode='markers',
            marker=dict(size=9, color=color_palette[i % len(color_palette)]),
            text=[f"Cluster {cluster}" for _ in range(len(cluster_data))],
            hoverinfo='text',
            name=f"Cluster {cluster}"
        ))

    fig.update_layout(
        title="Cluster Visualization",
        mapbox=dict(
            style='open-street-map',
            center=dict(
                lat=cluster_df['location-lat'].mean(), 
                lon=cluster_df['location-long'].mean()
            ),
            zoom=5
        ),
        showlegend=True,
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    return jsonify(fig.to_json())

@app.route('/plot_bird_movement', methods=['POST'])
def plot_bird_movement_route():
    data = request.json
    identifier = data.get('identifier')

    # Filter the DataFrame for the specific bird identifier
    bird_data = cluster_df[cluster_df['individual-local-identifier'] == identifier]

    if bird_data.empty:
        return jsonify({'error': 'No data found for the specified identifier'}), 404

    # Sort data by timestamp
    bird_data = bird_data.sort_values(by="timestamp")

    # Create the plot
    fig = go.Figure()

    # Create a unique identifier for month and cluster combination
    bird_data['month'] = bird_data['timestamp'].dt.month_name()
    bird_data['month_cluster'] = bird_data['month'] + "_" + bird_data['cluster'].astype(str)

    # Get unique month-cluster combinations
    unique_combinations = bird_data['month_cluster'].unique()
    
    # Generate a color palette
    color_palette = px.colors.qualitative.Plotly  # Use Plotly's qualitative color palette
    if len(unique_combinations) > len(color_palette):
        color_palette = px.colors.qualitative.Plotly * (len(unique_combinations) // len(px.colors.qualitative.Plotly) + 1)

    # Create a mapping for month-cluster combinations to colors
    color_map = {combination: color_palette[i % len(color_palette)] for i, combination in enumerate(unique_combinations)}

    # Track previous month to detect changes
    prev_month = None

    for combination in unique_combinations:
        cluster_data = bird_data[bird_data['month_cluster'] == combination]

        # Format hover text with highlighted month
        cluster_data["hover_text"] = cluster_data["timestamp"].apply(
            lambda x: f"<b>Month: {x.strftime('%B')}</b><br>Date: {x.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Get the color for the current month-cluster combination
        color = color_map[combination]

        # Add trace for the month-cluster combination
        fig.add_trace(go.Scattermapbox(
            lat=cluster_data['location-lat'],
            lon=cluster_data['location-long'],
            mode='markers',
            marker=dict(size=9, color=color),
            text=cluster_data["hover_text"],
            hoverinfo='text',
            name=f"{combination}"  # Unique name for the legend
        ))

        # Add update label for month transition
        for index, row in cluster_data.iterrows():
            current_month = row["timestamp"].month
            if prev_month is not None and current_month != prev_month:
                fig.add_trace(go.Scattermapbox(
                    lat=[row['location-lat']],
                    lon=[row['location-long']],
                    mode='text',
                    text=[f"Update: {row['timestamp'].strftime('%B')}"],
                    hoverinfo='text',
                    name=f"Update {row['timestamp'].strftime('%B')}",
                    textfont=dict(size=12, color="black", family="Arial Black"),
                ))
            prev_month = current_month

    fig.update_layout(
        title=f"Movement of Bird with Identifier {identifier}",
        mapbox=dict(
            style='open-street-map',
            center=dict(
                lat=bird_data['location-lat'].mean(), 
                lon=bird_data['location-long'].mean()
            ),
            zoom=10
        ),
        showlegend=True,
        height=600,
        margin={"r":0, "t":50, "l":0, "b":0}
    )

    return jsonify(fig.to_json())



@app.route('/distance', methods=['GET', 'POST'])
def distance():
    selected_bird_total_distance = None
    plot_html = None
    start_date = None
    end_date = None

    if request.method == 'POST':
        bird_id = request.form.get('bird_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Generate the plot
        plot_html = generate_plot(bird_data, bird_id, start_date, end_date)

        # Calculate total distance
        total_distance_data = calculate_total_distance_by_bird(bird_data, bird_id, start_date, end_date)
        
        if not total_distance_data.empty:
            selected_bird_total_distance = {
                'bird_id': bird_id,
                'total_distance': total_distance_data['distance_km'].values[0]
            }

    return render_template(
        'distance.html', 
        plot_html=plot_html, 
        selected_bird_total_distance=selected_bird_total_distance,
        start_date=start_date,
        end_date=end_date
    )


@app.route('/travel_pattern', methods=['GET', 'POST'])
def travel_pattern():
    travel_patterns_plot = None
    migration_path_plot = None
    total_time_spent_plot = None

    if request.method == 'POST':
        # Check which button was clicked
        if 'show_migration_path' in request.form:
            migration_path_plot,total_time_spent_plot = plot_migration_path()
            
        # elif 'show_total_time_spent' in request.form:
        #     total_time_spent_plot = plot_total_time_spent()

    return render_template(
        'travel_pattern.html',
        travel_patterns_plot=travel_patterns_plot,
        migration_path_plot=migration_path_plot,
        total_time_spent_plot=total_time_spent_plot
    )


API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_KEY = "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"

def query_huggingface(user_message):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "inputs": user_message,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.5,
            "top_k": 40,
            "top_p": 0.9
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data[0]['generated_text'] if data else "I'm not sure about that."
    else:
        return "Sorry, I'm having trouble processing your request."
    
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=5000,debug=True)