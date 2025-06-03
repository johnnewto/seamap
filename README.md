# Seamap

A real-time ship tracking application built with Flask and Folium, designed to monitor vessel movements in the Ōrākei Bay marine area. The application provides an interactive map interface with live updates of ship positions, speed, and timestamps.

## Features

- Interactive map display using OpenStreetMap and OpenSeaMap layers
- Real-time ship position updates
- Ship tracking with speed and timestamp information
- Measurement tools for distance and area calculations
- Marker clustering for better visualization
- Responsive web interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/seamap.git
cd seamap
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated (if you're using one)

2. Start the Flask application:
```bash
python map_app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

The application will start with a map centered on Ōrākei Bay, showing simulated ship movements. The map will automatically update every 3 seconds with new ship positions.

## Map Features

- **Base Layers**:
  - OpenStreetMap: Standard map view
  - OpenSeaMap: Nautical chart overlay

- **Controls**:
  - Layer Control: Toggle between different map layers
  - Measure Control: Measure distances and areas
  - Ship Markers: Click to view ship details
  - Ship Path: Blue line showing the vessel's route

## Development

The application uses:
- Flask for the web framework
- Folium for map visualization
- Pandas for data handling
- OpenStreetMap and OpenSeaMap for map tiles

## License

This project is licensed under the terms of the included LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
