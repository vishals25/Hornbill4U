from pages.data_loader import geo_df, map_options, cluster_df
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px


def plot_bird_movement_with_legend(bird_id, basemap):
    bird_data = geo_df[geo_df['individual-local-identifier'] == bird_id]
    grouped = bird_data.groupby(['year', 'month_name'])

    fig = go.Figure()
    colors = [f"rgba({i*30 % 255}, {i*60 % 255}, {i*90 % 255}, 0.7)" for i in range(len(grouped))]

    for (year, month), group in zip(grouped.groups.keys(), grouped):
        group_data = grouped.get_group((year, month))
        fig.add_trace(go.Scattermapbox(
            lat=group_data['location-lat'],
            lon=group_data['location-long'],
            mode='markers',
            marker=dict(size=9, color=colors.pop(0)),
            name=f"{month}, {year}"
        ))

    fig.update_layout(
        title=f"Movement of {bird_id} by Year-Month",
        mapbox=dict(
            style=map_options[basemap],
            center=dict(lat=bird_data['location-lat'].mean(), lon=bird_data['location-long'].mean()),
            zoom=10
        ),
        showlegend=True
    )
    return fig.to_json()

def plot_all_birds_unique_colors(year, month, basemap):
    filtered_data = geo_df[(geo_df['year'] == year) & (geo_df['month_name'] == month)]
    grouped = filtered_data.groupby('individual-local-identifier')

    fig = go.Figure()
    colors = [f"rgba({i*30 % 255}, {i*60 % 255}, {i*90 % 255}, 0.7)" for i in range(len(grouped))]

    for bird_id, group in grouped:
        fig.add_trace(go.Scattermapbox(
            lat=group['location-lat'],
            lon=group['location-long'],
            mode='markers',
            marker=dict(size=9, color=colors.pop(0)),
            name=bird_id
        ))

    fig.update_layout(
        title=f"All Birds' Movement in {month}, {year}",
        mapbox=dict(
            style=map_options[basemap],
            center=dict(lat=filtered_data['location-lat'].mean(), lon=filtered_data['location-long'].mean()),
            zoom=10
        ),
        showlegend=True
    )
    return fig.to_json()

def plot_combined_movement(bird_id, year, month, basemap):
    bird_data = geo_df[geo_df['individual-local-identifier'] == bird_id]
    filtered_bird_data = bird_data[(bird_data['year'] == year) & (bird_data['month_name'] == month)]
    all_birds_data = geo_df[(geo_df['year'] == year) & (geo_df['month_name'] == month)]

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=filtered_bird_data['location-lat'],
        lon=filtered_bird_data['location-long'],
        mode='markers',
        marker=dict(size=9, color='red'),
        name=f"{bird_id}"
    ))

    fig.add_trace(go.Scattermapbox(
        lat=all_birds_data['location-lat'],
        lon=all_birds_data['location-long'],
        mode='markers',
        marker=dict(size=6, color='blue'),
        name="Other Birds"
    ))

    fig.update_layout(
        title=f"Combined Movement in {month}, {year}",
        mapbox=dict(
            style=map_options[basemap],
            center=dict(lat=all_birds_data['location-lat'].mean(), lon=all_birds_data['location-long'].mean()),
            zoom=10
        ),
        showlegend=True
    )
    return fig.to_json()

def plot_clusters(basemap='OpenStreetMap'):
    # Create a color palette for different clusters
    unique_clusters = cluster_df['cluster'].unique()
    color_palette = [
        'red', 'blue', 'green', 'purple', 'orange', 'pink', 
        'cyan', 'magenta', 'yellow', 'brown'
    ]
    
    # Ensure we have enough colors for all clusters
    if len(unique_clusters) > len(color_palette):
        # Generate additional colors if needed
        import matplotlib.cm as cm
        import matplotlib.colors as mcolors
        additional_colors = cm.rainbow(np.linspace(0, 1, len(unique_clusters)))
        color_palette.extend([mcolors.to_hex(color) for color in additional_colors])

    # Create the figure
    fig = go.Figure()

    # Add a trace for each cluster
    for i, cluster in enumerate(unique_clusters):
        cluster_data = cluster_df[cluster_df['cluster'] == cluster]
        
        # Get the cluster name (replace 'cluster_name' with your actual column name)
        cluster_name = cluster_data['cluster_name'].iloc[0] if 'cluster_name' in cluster_data.columns else f"Cluster {cluster}"
        
        fig.add_trace(go.Scattermapbox(
            lat=cluster_data['location-lat'],
            lon=cluster_data['location-long'],
            mode='markers',
            marker=dict(
                size=9, 
                color=color_palette[i],
                opacity=0.7
            ),
            text=[cluster_name for _ in range(len(cluster_data))],  # Use cluster name instead of number
            hoverinfo='text',
            name=cluster_name  # Legend will also show names
        ))

    # Update layout with mapbox settings
    fig.update_layout(
        title="Cluster Visualization of Bird Movements",
        mapbox=dict(
            style=map_options.get(basemap, 'open-street-map'),
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

    return fig.to_json()



import pandas as pd
import plotly.express as px
import plotly.io as pio

def calculate_total_distance_by_interval(data, bird_id, start_date, end_date):
    # Convert timestamp to datetime if not already
    data['timestamp'] = pd.to_datetime(data['start_time'])
    
    filtered_data = data.loc[
        (data['bird_id'] == bird_id) &
        (data['timestamp'] >= start_date) &
        (data['timestamp'] <= end_date)
    ].copy()

    filtered_data['year'] = filtered_data['timestamp'].dt.year
    filtered_data['month'] = filtered_data['timestamp'].dt.month
    filtered_data['day'] = filtered_data['timestamp'].dt.day

    total_distance_per_interval = filtered_data.groupby(['year', 'month', 'day'])['distance_km'].sum().reset_index()
    total_distance_per_interval['date'] = pd.to_datetime(total_distance_per_interval[['year', 'month', 'day']])
    
    return total_distance_per_interval

def generate_plot(data, bird_id, start_date, end_date):
    filtered_data = calculate_total_distance_by_interval(data, bird_id, start_date, end_date)

    if filtered_data.empty:
        return None

    fig = px.bar(
        filtered_data,
        x='date',
        y='distance_km',
        labels={'distance_km': 'Total Distance (km)', 'date': 'Date'},
        title=f'Total Distance Traveled by {bird_id} from {start_date} to {end_date}'
    )

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Distance (km)',
        showlegend=False,
    )

    # Convert the plot to HTML
    plot_html = pio.to_html(fig, full_html=False)
    return plot_html

def calculate_total_distance_by_bird(data, bird_id, start_date, end_date):
    # Convert timestamp to datetime if not already
    data['timestamp'] = pd.to_datetime(data['start_time'])
    
    # Filter data by the specified date range and bird ID
    filtered_data = data.loc[
        (data['bird_id'] == bird_id) &
        (data['timestamp'] >= start_date) &
        (data['timestamp'] <= end_date)
    ].copy()

    # Group by bird identifier and sum the distances
    total_distance_by_bird = filtered_data.groupby('bird_id')['distance_km'].sum().reset_index()
    
    return total_distance_by_bird

def generate_plot(data, bird_id, start_date, end_date):
    filtered_data = calculate_total_distance_by_interval(data, bird_id, start_date, end_date)

    fig = px.bar(
        filtered_data,
        x='date',
        y='distance_km',
        labels={'distance_km': 'Total Distance (km)', 'date': 'Date'},
        title=f'Total Distance Traveled by {bird_id} from {start_date} to {end_date}'
    )

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Distance (km)',
        showlegend=False,
    )

    # Convert the plot to HTML
    plot_html = pio.to_html(fig, full_html=False)
    return plot_html
    
    
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import networkx as nx
import numpy as np
from collections import defaultdict, Counter

# def plot_travel_patterns():
#     """Create a network graph showing bird navigation between clusters"""
#     data = pd.read_csv('data/migration.csv')
    
#     if 'start_date' not in data.columns:
#         print("Error: 'start_date' column not found in dataset.")
#         return None
    
#     data['start_date'] = pd.to_datetime(data['start_date'])
#     data['end_date'] = pd.to_datetime(data['end_date'])
    
#     # Parse time_spent to get numeric days
#     data['days_spent'] = data['time_spent'].str.extract('(\d+)').astype(float)
    
#     # Create network graph
#     G = nx.DiGraph()
#     edge_weights = defaultdict(int)
#     bird_paths = defaultdict(list)
    
#     # Process each bird's journey
#     for bird_id in data['individual-local-identifier'].unique():
#         bird_data = data[data['individual-local-identifier'] == bird_id].sort_values('start_date')
        
#         # Track transitions between clusters
#         for i in range(len(bird_data) - 1):
#             current_cluster = bird_data.iloc[i]['cluster']
#             next_cluster = bird_data.iloc[i + 1]['cluster']
            
#             if current_cluster != next_cluster:
#                 edge_weights[(current_cluster, next_cluster)] += 1
#                 bird_paths[bird_id].append((current_cluster, next_cluster))
    
#     # Add nodes and edges to graph
#     all_clusters = sorted(data['cluster'].unique())
#     for cluster in all_clusters:
#         G.add_node(cluster)
    
#     for (source, target), weight in edge_weights.items():
#         G.add_edge(source, target, weight=weight)
    
#     # Create layout
#     pos = nx.spring_layout(G, k=3, iterations=50)
    
#     # Prepare edge traces
#     edge_x = []
#     edge_y = []
#     edge_info = []
    
#     for edge in G.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_x.extend([x0, x1, None])
#         edge_y.extend([y0, y1, None])
#         weight = G[edge[0]][edge[1]]['weight']
#         edge_info.append(f"{edge[0]} → {edge[1]}: {weight} transitions")
    
#     # Create edge trace
#     edge_trace = go.Scatter(
#         x=edge_x, y=edge_y,
#         line=dict(width=2, color='#888'),
#         hoverinfo='none',
#         mode='lines'
#     )
    
#     # Create node trace
#     node_x = []
#     node_y = []
#     node_text = []
#     node_info = []
    
#     for node in G.nodes():
#         x, y = pos[node]
#         node_x.append(x)
#         node_y.append(y)
#         node_text.append(f'Cluster {node}')
        
#         # Count bird visits to this cluster
#         visits = len(data[data['cluster'] == node])
#         total_time = data[data['cluster'] == node]['days_spent'].sum()
#         node_info.append(f'Cluster {node}<br>Visits: {visits}<br>Total days: {total_time:.1f}')
    
#     node_trace = go.Scatter(
#         x=node_x, y=node_y,
#         mode='markers+text',
#         hoverinfo='text',
#         text=node_text,
#         textposition="middle center",
#         hovertext=node_info,
#         marker=dict(
#             showscale=True,
#             colorscale='Viridis',
#             size=30,
#             color=[len(data[data['cluster'] == node]) for node in G.nodes()],
#             colorbar=dict(
#                 thickness=15,
#                 len=0.5,
#                 xanchor="left",
#                 title="Number of Visits"
#             ),
#             line=dict(width=2, color='white')
#         )
#     )
    
#     # Create figure
#     fig = go.Figure(data=[edge_trace, node_trace],
#                     layout=go.Layout(
#                         title='Bird Migration Network - Cluster Transitions',
#                         titlefont_size=16,
#                         showlegend=False,
#                         hovermode='closest',
#                         margin=dict(b=20,l=5,r=5,t=40),
#                         annotations=[ dict(
#                             text="Node size = number of visits<br>Edges show migration paths",
#                             showarrow=False,
#                             xref="paper", yref="paper",
#                             x=0.005, y=-0.002,
#                             xanchor='left', yanchor='bottom',
#                             font=dict(color='gray', size=12)
#                         )],
#                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
#                     ))
    
#     return pio.to_html(fig, full_html=False)
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots

def plot_migration_path():
    """Create two figures: one for individual bird subplots, one for overall comparison"""
    data = pd.read_csv('data/migration.csv')

    if 'start_date' not in data.columns:
        print("Error: 'start_date' column not found in dataset.")
        return None, None

    # Preprocessing
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])
    data['days_spent'] = data['time_spent'].str.extract('(\d+)').astype(float)

    birds = sorted(data['individual-local-identifier'].unique())
    n_birds = len(birds)
    cols = 3
    n_sub_rows = (n_birds + cols - 1) // cols

    colors = px.colors.qualitative.Set3

    # ----------------------------- #
    # First Plot: Individual Subplots
    # ----------------------------- #
    fig_subplots = make_subplots(
        rows=n_sub_rows,
        cols=cols,
        subplot_titles=birds,
        shared_xaxes=False,
        shared_yaxes=True,
        vertical_spacing=0.12,
        horizontal_spacing=0.07,
    )

    for i, bird in enumerate(birds):
        row = (i // cols) + 1
        col = (i % cols) + 1
        bird_data = data[data['individual-local-identifier'] == bird].sort_values('start_date')

        fig_subplots.add_trace(
            go.Scatter(
                x=bird_data['start_date'],
                y=bird_data['cluster'],
                mode='lines+markers',
                name=bird,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8, symbol='circle'),
                hovertemplate=f'<b>{bird}</b><br>Date: %{{x}}<br>Cluster: %{{y}}<br>Days spent: %{{customdata}}<extra></extra>',
                customdata=bird_data['days_spent'],
                showlegend=False
            ),
            row=row,
            col=col
        )

        for j in range(len(bird_data) - 1):
            current = bird_data.iloc[j]
            next_point = bird_data.iloc[j + 1]

            if current['cluster'] != next_point['cluster']:
                fig_subplots.add_annotation(
                    x=next_point['start_date'],
                    y=next_point['cluster'],
                    ax=current['start_date'],
                    ay=current['cluster'],
                    xref=f'x{i+1}',
                    yref=f'y{i+1}',
                    axref=f'x{i+1}',
                    ayref=f'y{i+1}',
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='red',
                    opacity=0.6,
                    row=row,
                    col=col
                )

    fig_subplots.update_layout(
        title_text="Individual Bird Migration Paths",
        height=300 * n_sub_rows,
        showlegend=False,
    )

    for i in range(1, n_birds + 1):
        row_idx = (i - 1) // cols + 1
        col_idx = (i - 1) % cols + 1
        fig_subplots.update_yaxes(title_text="Cluster", dtick=1, row=row_idx, col=col_idx)
        fig_subplots.update_xaxes(title_text="Date", tickformat="%d %b", row=row_idx, col=col_idx)

    # ----------------------------- #
    # Second Plot: Combined Comparison
    # ----------------------------- #
    fig_compare = go.Figure()
    for i, bird in enumerate(birds):
        bird_data = data[data['individual-local-identifier'] == bird].sort_values('start_date')

        fig_compare.add_trace(
            go.Scatter(
                x=bird_data['start_date'],
                y=bird_data['cluster'],
                mode='lines+markers',
                name=bird,
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6, symbol='circle'),
                hovertemplate=f'<b>{bird}</b><br>Date: %{{x}}<br>Cluster: %{{y}}<br>Days spent: %{{customdata}}<extra></extra>',
                customdata=bird_data['days_spent']
            )
        )

        for j in range(len(bird_data) - 1):
            current = bird_data.iloc[j]
            next_point = bird_data.iloc[j + 1]

            if current['cluster'] != next_point['cluster']:
                fig_compare.add_annotation(
                    x=next_point['start_date'],
                    y=next_point['cluster'],
                    ax=current['start_date'],
                    ay=current['cluster'],
                    arrowhead=2,
                    arrowsize=0.8,
                    arrowwidth=1.5,
                    arrowcolor='red',
                    opacity=0.4
                )

    fig_compare.update_layout(
        title_text="All Birds Migration Path Comparison",
        height=600,
        xaxis_title="Date",
        yaxis_title="Cluster",
        yaxis=dict(dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=40, r=20, t=60, b=80)
    )

    return pio.to_html(fig_subplots, full_html=False), pio.to_html(fig_compare, full_html=False)



# def plot_total_time_spent():
#     """Create a heatmap showing cluster usage patterns over time"""
#     data = pd.read_csv('data/migration.csv')
    
#     if 'start_date' not in data.columns:
#         print("Error: 'start_date' column not found in dataset.")
#         return None
    
#     data['start_date'] = pd.to_datetime(data['start_date'])
#     data['end_date'] = pd.to_datetime(data['end_date'])
    
#     # Parse time_spent to get numeric days
#     data['days_spent'] = data['time_spent'].str.extract('(\d+)').astype(float)
    
#     # Create a matrix for heatmap
#     birds = sorted(data['individual-local-identifier'].unique())
#     clusters = sorted(data['cluster'].unique())
    
#     # Create matrix of time spent by each bird in each cluster
#     heatmap_data = []
#     for bird in birds:
#         bird_data = data[data['individual-local-identifier'] == bird]
#         bird_row = []
#         for cluster in clusters:
#             cluster_time = bird_data[bird_data['cluster'] == cluster]['days_spent'].sum()
#             bird_row.append(cluster_time)
#         heatmap_data.append(bird_row)
    
#     fig = go.Figure(data=go.Heatmap(
#         z=heatmap_data,
#         x=[f'Cluster {c}' for c in clusters],
#         y=birds,
#         colorscale='Viridis',
#         hoverongaps=False,
#         hovertemplate='Bird: %{y}<br>Cluster: %{x}<br>Days: %{z}<extra></extra>'
#     ))
    
#     fig.update_layout(
#         title='Cluster Usage Heatmap - Days Spent by Each Bird',
#         xaxis_title='Clusters',
#         yaxis_title='Birds',
#         height=400
#     )
    
#     return pio.to_html(fig, full_html=False)
