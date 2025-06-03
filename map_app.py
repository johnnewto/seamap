from flask import Flask, render_template_string, jsonify
import folium
from folium.plugins import Realtime, MeasureControl
from folium.elements import JavascriptLink, CssLink
import pandas as pd
from datetime import datetime, timedelta
import random

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Create sample AIS-like data for a ship's path around Ōrākei Bay
data = pd.DataFrame({
    'lat': [-36.8469, -36.8475, -36.8480, -36.8470, -36.8465],
    'lon': [174.8125, 174.8130, 174.8140, 174.8135, 174.8128],
    'ship_name': ['MV Explorer'] * 5,
    'speed': [5.2, 5.5, 5.0, 5.3, 5.1],  # Speed in knots
    'timestamp': [(datetime.now() - timedelta(minutes=20-i*5)).strftime('%Y-%m-%d %H:%M:%S') for i in range(5)]
})

def add_map_options(m):
    print("add_map_options")
    # Add OpenStreetMap base layer
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='© OpenStreetMap contributors',
        name='OpenStreetMap',
        overlay=False
    ).add_to(m)

    # Add OpenSeaMap layer for nautical charts
    folium.TileLayer(
        tiles='https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',
        attr='© OpenSeaMap contributors',
        name='OpenSeaMap',
        opacity=0.8,
        overlay=True
    ).add_to(m)

    # Create marker cluster
    marker_cluster = folium.plugins.MarkerCluster(name='Ship Positions').add_to(m)

    # Add markers for initial ship positions
    for _, row in data.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(
                f"{row['ship_name']}<br>Speed: {row['speed']} knots<br>Time: {row['timestamp']}",
                max_width=200
            ),
            icon=folium.Icon(color='red', icon='ship', prefix='fa')  # Use ship icon
        ).add_to(marker_cluster)
        # Add polyline for ship's path
    folium.PolyLine(
        locations=data[['lat', 'lon']].values,
        color='blue',
        weight=3,
        opacity=0.8,
        popup='Ship Path'
    ).add_to(m)

    # Add measure control
    measure = MeasureControl(
        position='topleft',
        primary_length_unit='meters',
        secondary_length_unit='kilometers',
        primary_area_unit='sqmeters',
        secondary_area_unit='hectares',
        localization='en'
    )
    m.add_child(measure)

    # Add layer control
    # folium.LayerControl(position='topright').add_to(m)



# # Add required CSS and JavaScript files
# m.get_root().header.add_child(CssLink('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'))
# m.get_root().header.add_child(CssLink('https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css'))
# m.get_root().header.add_child(CssLink('https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css'))
# m.get_root().header.add_child(CssLink('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'))
# m.get_root().header.add_child(CssLink('https://cdn.jsdelivr.net/npm/leaflet-measure@3.1.0/dist/leaflet-measure.css'))
# m.get_root().header.add_child(CssLink('./static/css/style.css'))

# m.get_root().html.add_child(JavascriptLink('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'))
# m.get_root().html.add_child(JavascriptLink('https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js'))
# m.get_root().html.add_child(JavascriptLink('https://code.jquery.com/jquery-3.6.0.min.js'))
# m.get_root().html.add_child(JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-measure@3.1.0/dist/leaflet-measure.js'))

# Add Realtime plugin to fetch data from /new_waypoint
source = folium.JsCode("""
    function(responseHandler, errorHandler) {
        console.log('Fetching new waypoint data...');
        var url = '/new_waypoint';
        
        fetch(url)
        .then((response) => {
            return response.json().then((data) => {
                var { lat, lon, ship_name, speed, timestamp } = data;
                
                return {
                    'type': 'FeatureCollection',
                    'features': [{
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [lon, lat]
                        },
                        'properties': {
                            'ship_name': ship_name,
                            'speed': speed,
                            'timestamp': timestamp
                        }
                    }]
                };
            })
        })
        .then(responseHandler)
        .catch(errorHandler);
    }
""")

html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ōrākei Bay Marine Area Ship Tracking</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>Ōrākei Bay Marine Area Ship Tracking</h1>
            {{ m._repr_html_() | safe }}
        </body>
        </html>
    """



# Flask route to serve the map
@app.route('/')
def index():
    # Get the last point from data for initial map center
    last_point = data.iloc[-1]
    center_lat, center_lon = last_point['lat'], last_point['lon']

    # Create Folium map
    m = folium.Map(
        location=[center_lat, center_lon],  # Center on last ship position
        zoom_start=25,
        control_scale=True
    )
    add_map_options(m)
    # Create and add Realtime layer with a name
    rt = Realtime(source, interval=3000, name='Ship Tracking')
    rt.add_to(m)
    # Render map to HTML
    return render_template_string(html, m=m)

# Flask route to provide new waypoint data
@app.route('/new_waypoint')
def new_waypoint():
    global data
    # Simulate a new waypoint near the last position
    last_point = data.iloc[-1]
    new_lat = last_point['lat'] + random.uniform(-0.001, 0.001)
    new_lon = last_point['lon'] + random.uniform(-0.001, 0.001)
    new_speed = round(random.uniform(4.8, 5.6), 1)
    new_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append to data for continuity
    new_row = pd.DataFrame({
        'lat': [new_lat],
        'lon': [new_lon],
        'ship_name': ['MV Explorer'],
        'speed': [new_speed],
        'timestamp': [new_timestamp]
    })
    data = pd.concat([data, new_row], ignore_index=True)
    
    return jsonify({
        'lat': new_lat,
        'lon': new_lon,
        'ship_name': 'MV Explorer',
        'speed': new_speed,
        'timestamp': new_timestamp
    })

if __name__ == '__main__':
    app.run(debug=True)