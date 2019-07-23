from flask import Flask, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):

    def get(self, name):
        for item in items:
            if item.get('name') == name:
                return item
        return {'item': None}, 404

    def post(self, name):
        data = request.get_json()
        item = {'name': name, 'price': data.get('price')}
        items.append(item)
        return item, 201


class ItemList(Resource):

    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)
