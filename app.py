"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2118@localhost/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'asdfghjkl'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

@app.route('/')
def homepage():

    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcake_list():
    """Get information about cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake"""

    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=serialize_cupcake(cupcake)), 201)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake_data(id):
    """Get information about a specific cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = [serialize_cupcake(cupcake)]

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake_data(id):
    """Update information about a specific cupcake"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor=request.json.get('flavor', cupcake.flavor)
    cupcake.size=request.json.get('size', cupcake.size)
    cupcake.rating=request.json.get('rating', cupcake.rating)
    cupcake.image=request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=serialize_cupcake(cupcake))

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete a specific cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')