# Real-Time Analytics (RTA) Project

This project demonstrates a real-time analytics dashboard using Kafka, Dash, and Python. It includes a producer that generates sales data and a dashboard to visualize the data in real-time.

## Features

- **Producer**: Generates random sales data and sends it to a Kafka topic.
- **Dashboard**: Displays real-time visualizations of sales data, including:
  - Bar chart for item quantities.
  - Pie chart for card type distribution.

## Prerequisites

- Python 3.7 or higher
- Kafka broker running locally on `localhost:9092`
- Required Python libraries (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/olgierrd/rta-project.git
   cd <repository-name>
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Kafka is running locally on `localhost:9092`.

## Usage

1. Start the producer to generate sales data:
   ```bash
   python producer.py
   ```

2. Start the dashboard to visualize the data:
   ```bash
   python statistics-app.py
   ```

3. Open the dashboard in your browser at `http://127.0.0.1:8050`.

4. To stop the dashboard, send a POST request to the `/shutdown` endpoint:
   ```bash
   curl -X POST http://127.0.0.1:8050/shutdown
   ```

## File Descriptions

- `start.py`: Script to start the containers.
- `producer.py`: Generates random sales data and sends it to a Kafka topic.
- `statistics-app.py`: Dash application for visualizing sales data in real-time.
- `requirements.txt`: Lists the Python dependencies for the project.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [Dash](https://dash.plotly.com/) for building interactive dashboards.
- [Kafka](https://kafka.apache.org/) for real-time data streaming.
