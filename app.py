"""Flask app for Cupcakes"""

from flask import Flask, render_template, flash, redirect, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config["SECRET_KEY"] = "pugsrcool24"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_DIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a dessert SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

# GET /api/cupcakes
# Get data about all cupcakes.

# Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
# The values should come from each cupcake instance.

@app.route('/')
def show_homepage():
    return render_template("index.html")

@app.route('/api/cupcakes')
def get_all_cupcakes():
    """Get data about all cupcakes"""
    cupcakes = Cupcake.query.all()
    output = [serialize_cupcake(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes=output)

# GET /api/cupcakes/[cupcake-id]
# Get data about a single cupcake.
# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
# This should raise a 404 if the cupcake cannot be found.

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    output = serialize_cupcake(cupcake)
    return jsonify(cupcake=output)

# POST /api/cupcakes
# Create a cupcake with flavor, size, rating and image data from the body of the request.
# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data"""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    if image != "":
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    else:
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating)
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.to_dict()), 201)

# PATCH /api/cupcakes/[cupcake-id]
# Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend.
# Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)

# DELETE /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.
# # Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in URL"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    Cupcake.query.filter_by(id = cupcake_id).delete()
    db.session.commit()
    return (jsonify({'message': "Deleted"}))




