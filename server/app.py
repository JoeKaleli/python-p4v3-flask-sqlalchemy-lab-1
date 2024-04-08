# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquake/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        # If an earthquake is found, return its attributes as JSON
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        # If no earthquake is found, return an error message as JSON
        return jsonify({"error": "Earthquake not found"}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quake_data = []
    for quake in earthquakes:
        quake_data.append({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        })

    # Create a JSON response containing the count of matching earthquakes and the earthquake data
    response = {
        "count": len(earthquakes),
        "quakes": quake_data
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
