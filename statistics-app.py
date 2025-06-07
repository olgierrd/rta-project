import pandas as pd
from kafka import KafkaConsumer
import json
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask import request

# Initialize Kafka consumer
bootstrap_servers = 'localhost:9092'
topic = 'sales'
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Initialize empty DataFrame for sales data
sales_data = pd.DataFrame(columns=['sale_id', 'profit', 'transaction_date', 'buyer', 'card_type', 'item', 'quantity', 'amount'])

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard", style={'textAlign': 'center'}),
    html.Div("Visualizing sales data in real-time", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.Label("Item Quantities", style={'fontWeight': 'bold', 'marginTop': '20px'}),
    dcc.Graph(id='item-quantities'),
    html.Label("Card Type Distribution", style={'fontWeight': 'bold', 'marginTop': '20px'}),
    dcc.Graph(id='card-types'),
    dcc.Interval(id='update-interval', interval=1000, n_intervals=0)
])

@app.callback(
    [Output('item-quantities', 'figure'),
     Output('card-types', 'figure')],
    [Input('update-interval', 'n_intervals')]
)
def update_dashboard(n):
    global sales_data

    # Consume messages from Kafka
    for message in consumer:
        new_sale = message.value
        sales_data = pd.concat([sales_data, pd.DataFrame([new_sale])], ignore_index=True)
        break

    # Bar chart for item quantities
    item_data = sales_data.groupby('item')['quantity'].sum().reset_index()
    item_chart = {
        'data': [{'x': item_data['item'], 'y': item_data['quantity'], 'type': 'bar', 'name': 'Items'}],
        'layout': {'title': 'Item Quantities'}
    }

    # Pie chart for card types
    card_data = sales_data['card_type'].value_counts()
    card_chart = {
        'data': [{'labels': card_data.index, 'values': card_data.values, 'type': 'pie'}],
        'layout': {'title': 'Card Type Distribution'}
    }

    return item_chart, card_chart

@app.server.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(debug=True)