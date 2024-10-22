# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
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

@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquakes = Earthquake.query.all()
    return jsonify([eq.to_dict() for eq in earthquakes]), 200

@app.route('/earthquakes', methods=['POST'])
def create_earthquake():
    data = request.json
    new_eq = Earthquake(
        magnitude=data['magnitude'],
        location=data['location'],
        year=data['year']
    )
    db.session.add(new_eq)
    db.session.commit()
    return make_response(new_eq.to_dict(), 201)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    eq = Earthquake.query.get(id)
    if eq is None:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)
    return jsonify(eq.to_dict()), 200

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        'count': len(quakes),
        'quakes': [eq.to_dict() for eq in quakes]
    }), 200

@app.route('/earthquakes/<int:id>', methods=['PUT'])
def update_earthquake(id):
    data = request.json
    eq = Earthquake.query.get_or_404(id)
    eq.magnitude = data['magnitude']
    eq.location = data['location']
    eq.year = data['year']
    db.session.commit()
    return jsonify(eq.to_dict()), 200

@app.route('/earthquakes/<int:id>', methods=['DELETE'])
def delete_earthquake(id):
    eq = Earthquake.query.get_or_404(id)
    db.session.delete(eq)
    db.session.commit()
    return make_response({'message': 'Earthquake deleted'}, 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
