from flask import Flask, request
from flask_restful import Resource, Api
from bson.json_util import dumps
from bson import ObjectId
import pymongo

app = Flask(__name__)
api = Api(app)

client = pymongo.MongoClient("db", 27017)
db = client['database']
blabs = db['blabs']

class Blabber(Resource):
    """GET/POST referencing entire database"""
    
    def get(self):
        """GET all blabs"""
        return dumps(blabs.find()), 200

    def post(self):
        """POST a new blab"""
        post = request.get_json()
        _id = blabs.insert_one(post).inserted_id
        blab = dumps(blabs.find({"_id": _id}))

        return blab, 201


class Blabber_edit(Resource):
    """DELETE specific blabs"""

    def delete(self, blab_id):
        """DELETE a specific blab by _id"""
        delete_blab = blabs.delete_one({"_id": ObjectId(blab_id)})

        if delete_blab.deleted_count > 0:
            return '', 200
        else:
            return '', 404


api.add_resource(Blabber, '/blabs')
api.add_resource(Blabber_edit, '/blabs/<blab_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)