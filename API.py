from flask import Flask, request
from flask_restful import Resource, Api
from bson import ObjectId
import pymongo
import time

with open("/run/secrets/hostname") as f:
    host = f.read()

app = Flask(__name__)
api = Api(app)

client = pymongo.MongoClient(host, 27017)
db = client['database']
blabs = db['blabs']

class Blabber(Resource):
    """GET/POST referencing entire database"""
    
    def get(self):
        """GET all blabs"""
        createdSince = request.args.get("createdSince")
        if not createdSince:
            createdSince  = 0
        else:
            createdSince = float(createdSince)

        items = list(blabs.find({"postTime": {"$gt": createdSince}}))
        # Need to convert ObjectId's to strings or else JSON will throw 85 errors
        for i, v in enumerate(items):
            items[i]["id"] = str(v["_id"])
            del items[i]["_id"]

        return items, 200

    def post(self):
        """POST a new blab"""
        post = request.get_json()
        post["postTime"] = time.time()
        _id = blabs.insert_one(post).inserted_id

        blab = blabs.find_one({"_id": ObjectId(_id)})
        blab["id"] = str(blab["_id"])
        del blab["_id"]

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

# Add routes/endpoints
api.add_resource(Blabber, '/blabs')
api.add_resource(Blabber_edit, '/blabs/<blab_id>')

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
