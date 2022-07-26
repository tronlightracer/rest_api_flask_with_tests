from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.store import StoreModel

class Store(Resource):
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found"}, 404
    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "A store with '{}' already exists".format(name)}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating the store"}

        return store.json(), 201
    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}

class StoreList(Resource):
    def get(self):
        #return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {"stores": [store.json() for store in StoreModel.find_all()]}
