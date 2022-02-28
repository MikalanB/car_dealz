from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        #foreign key for cars table - before black belt haha
        self.user_id = data['user_id']
    
    #add a car to db
    @classmethod
    def add_car(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id, created_at) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s, NOW());"
        result = connectToMySQL("cars_schema").query_db(query,data)
        return result
    
    #show all cars in db
    @classmethod
    def all_cars(cls):
        query = "SELECT * FROM cars;"
        result = connectToMySQL("cars_schema").query_db(query)
        all_cars = []
        for row in result:
            all_cars.append(cls(row))
        return all_cars
    
    #find seller information based on car id
    @classmethod
    def seller_car_id(cls,data):
        query = "SELECT * FROM cars JOIN users ON users.id = cars.user_id WHERE cars.id = %(id)s"
        result = connectToMySQL('cars_schema').query_db(query,data) 
        sellers = []
        for row in result:
            one_seller = cls(row)
            user_data = {
                "id" : row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_seller.user = user.User(user_data)

            sellers.append(one_seller)
        return sellers
    
    #find seller information
    @classmethod
    def seller(cls):
        query = "SELECT * FROM cars JOIN users ON users.id = cars.user_id"
        result = connectToMySQL('cars_schema').query_db(query) 
        sellers = []
        for row in result:
            one_seller = cls(row)
            user_data = {
                "id" : row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_seller.user = user.User(user_data)

            sellers.append(one_seller)
        return sellers
    
    #view car
    @classmethod
    def view_car(cls, data):
        query = "SELECT * FROM cars WHERE id = %(id)s"
        result = connectToMySQL('cars_schema').query_db(query,data)
        return cls(result[0])

    #update car 
    @classmethod
    def update_car(cls, data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s,  year = %(year)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s"
        result = connectToMySQL("cars_schema").query_db(query,data)
        return result

    #delete car listing
    @classmethod
    def delete_car(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s"
        result = connectToMySQL("cars_schema").query_db(query,data)
        return result

    # ==================== Black Belt portion============================================
    # add car to purchases table
    @classmethod
    def purchase_car(cls,data):
        query = "INSERT INTO purchases (user_id, car_id, created_at) VALUES ('%(user_id)s', '%(car_id)s', NOW());"
        result = connectToMySQL("cars_schema").query_db(query,data)
        return result

    # view purchases by user id
    @classmethod
    def view_purchases(cls, data):
        query = "SELECT * FROM cars LEFT JOIN purchases ON purchases.car_id = cars.id LEFT JOIN users ON purchases.user_id = users.id WHERE users.id = %(id)s"
        result = connectToMySQL("cars_schema").query_db(query,data)
        all_purchases = []
        for row in result:
            one_purchase = cls(row)
            user_data = {
                "id" : row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_purchase.info = user.User(user_data)

            all_purchases.append(one_purchase)
        return all_purchases


    @staticmethod
    #validate car
    def validate_car(car):
        is_valid = True
        if len(car['price']) < 1:
            flash("Price must be greater than zero.")
            is_valid = False
        if len(car['model']) < 1:
            flash("Model field cannot be empty. Please enter the model of the car.")
            is_valid = False
        if len(car['make']) < 1:
            flash("Make field cannot be empty. Please enter the Make of the car.")
            is_valid= False
        if len(car['year']) < 1:
            flash("Price must be greater than zero.")
            is_valid = False
        if len(car['description']) < 1:
            flash("Car Description is too short! Please enter more details.")
            is_valid = False
        return is_valid