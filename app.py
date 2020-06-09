"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes = [cupcake.serialized() for cupcake in Cupcake.query.all()]
    return jsonify(all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id).serialized()
    return jsonify(cupcake)

@app.route('/api/cupcakes', methods = ["POST"])
def add_cupcake():
    new_cupcake = Cupcake(flavor = request.json['flavor'],
                            size = request.json['size'],
                            rating = request.json['rating'],
                            image = request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialized())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["PATCH"])
def edit_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    response_json = jsonify(serial_cupcake = cupcake.serialized())
    return (response_json, 200)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    if cupcake:
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message="deleted")

@app.route('/')
def show_home():
    return render_template('home.html')