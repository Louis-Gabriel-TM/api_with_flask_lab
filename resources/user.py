import sqlite3

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="'Username' field cannot be left blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="'Password' field cannot be left blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data.get('username')):
            return {'message': "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO Users VALUES (NULL, ?, ?);"
        cursor.execute(query, (data.get('username'), data.get('password')))

        connection.commit()
        connection.close()

        return {'message': "User created succesfully"}, 201