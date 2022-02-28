from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.car import Car

@app.route('/new_car')
def new_car():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
        }
    user = User.find_id(data)
    return render_template('new_car.html', user=user)

@app.route('/add_car', methods=['POST'])
def add_car():
    if "user_id" not in session:
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect('/new_car')
    data = {
        'price' : request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Car.add_car(data)
    return redirect('/dashboard')

@app.route("/view/<int:car_id>")
def view_car(car_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
        }
    data2 = {
        "id": car_id
    }
    user = User.find_id(data)
    car = Car.view_car(data2)
    seller_info = Car.seller_car_id(data2)
    # likes = Show.count_likes(data2)
    return render_template("view_car.html", user=user, car=car, seller_info=seller_info)

@app.route('/edit/<int:car_id>')
def edit(car_id):
    if "user_id" in session:
        data = {
            "id": car_id
        }
        car = Car.view_car(data)
        return render_template("edit_car.html", car=car)
    return redirect("/")

@app.route('/edit_car/<int:car_id>', methods=['POST'])
def edit_car(car_id):
    if "user_id" not in session:
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect(f'/edit/{car_id}')
    data = {
        'id' : car_id,
        'price' : request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Car.update_car(data)
    return redirect('/dashboard')

@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': car_id
        }
    Car.delete_car(data)
    return redirect('/dashboard')

#purchase car
@app.route('/purchase/<int:car_id>')
def purchase_car(car_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id'],
        'car_id' : car_id
    }
    Car.purchase_car(data)
    return redirect('/dashboard')

@app.route('/view_purchases')
def view_purchases():
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    purchases = Car.view_purchases(data)
    user = User.find_id(data)

    return render_template("purchases.html", purchases=purchases, user=user)
