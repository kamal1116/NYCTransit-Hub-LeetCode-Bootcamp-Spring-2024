import csv
from flask import Flask, jsonify, request, render_template
import requests
from google.transit import gtfs_realtime_pb2

def load_data(filepath, key_field, value_field):
    data_dict = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row[key_field]
            value = row[value_field]
            data_dict[key] = value
    return data_dict

app = Flask(__name__, static_folder='static', template_folder='templates')

stops = load_data('stops.txt', 'stop_id', 'stop_name')
routes = load_data('routes.txt', 'route_id', 'route_short_name')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/updates/<string:line_code>', methods=['GET'])
def get_updates(line_code):
    endpoints = {
        'NQRW': 'nyct%2Fgtfs-nqrw',
        'ACE': 'nyct%2Fgtfs-ace',
        'BDFM': 'nyct%2Fgtfs-bdfm',
        'G': 'nyct%2Fgtfs-g',
        'JZ': 'nyct%2Fgtfs-jz',
        'L': 'nyct%2Fgtfs-l',
        'SIR': 'nyct%2Fgtfs-si'
    }
    url = f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/{endpoints.get(line_code, 'nyct%2Fgtfs')}"
    response = requests.get(url)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    updates = []
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            route_id = entity.trip_update.trip.route_id
            route_name = routes.get(route_id, "Unknown Route")
            for update in entity.trip_update.stop_time_update:
                updates.append({
                    'train': route_name,
                    'stop_name': stops.get(update.stop_id, "Unknown Station"),
                    'arrival': update.arrival.time if update.arrival else None
                })
    return jsonify(updates)

if __name__ == '__main__':
    app.run(debug=True)
