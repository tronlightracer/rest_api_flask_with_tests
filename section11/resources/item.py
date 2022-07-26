# TODO:
# need to remove jwt optional add it doesn't work


from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.item import ItemModel

#defining the Item Resource which to call http methods with 
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    #defining the methods the resource is going to accept
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    #makes authorization neccessary
    @jwt_required(fresh=True)
    def post(self, name):
        #deal with errors first
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        
        #then perform the wanted operations
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            #500 status code for internal server errors
            return {"message": "An error occurred inserting the item."}, 500
        #201 is the status code for created data
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privileges required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    @jwt_required(fresh=True)
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    # jwt_required(optional=True) allows the api to return some data if the user doesn't login
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        #if user_id:
            #return {"items": items}, 200
        if user_id:
            return jsonify(logged_in_as=user_id), {'items': items}, 200
        return {'items': [item['name'] for item in items], 'message': 'more data available if you login'}, 200  

    


