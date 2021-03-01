"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


def serialize_cupcake(cupcake):
	return {
		"id": cupcake.id,
		"flavor": cupcake.flavor,
		"size": cupcake.size,
		"rating": cupcake.rating,
		"image": cupcake.image,
	}

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/api/cupcakes', methods=["GET"])
def show_all_cupcakes():
	cupcakes = Cupcake.query.all()
	serialized = [serialize_cupcake(c) for c in cupcakes]
	
	return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<cupcake_id>', methods=["GET"])
def show_cupcake_details(cupcake_id):
	cupcake = Cupcake.query.get_or_404(cupcake_id)
	serialized = serialize_cupcake(cupcake)
	
	return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=["POST"])
def post_new_cupcake():
	flavor = request.json['flavor']
	size = request.json['size']
	rating = request.json['rating']
	image = request.json['image']
	
	new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
	
	db.session.add(new_cupcake)
	db.session.commit()
	serialized = serialize_cupcake(new_cupcake)
	
	return jsonify(cupcake=serialized), 201


@app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def update_todo(cupcake_id):
	cupcake = Cupcake.query.get_or_404(cupcake_id)
	cupcake.flavor = request.json.get('flavor', cupcake.flavor)
	cupcake.size = request.json.get('size', cupcake.size)
	cupcake.rating = request.json.get('rating', cupcake.rating)
	cupcake.image = request.json.get('image', cupcake.image)
	db.session.commit()
	
	return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def delete_todo(cupcake_id):
	cupcake = Cupcake.query.get_or_404(cupcake_id)
	db.session.delete(cupcake)
	db.session.commit()
	
	return jsonify(message="deleted")
