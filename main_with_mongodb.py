from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import pymongo

app = Flask(__name__)
api = Api(app)
cli=pymongo.MongoClient("mongodb://localhost:27017/")
print(cli)
db=cli['flask']
collection=db['videos']
print(collection)

names = {
    "pranay": {"age": 21, "gender": "male"},
    "ishwar": {"age": 22, "gender": "male"}
}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="field cannot be empty")
video_put_args.add_argument("views", type=str, help="field cannot be empty")
video_put_args.add_argument("likes", type=str, help="field cannot be empty")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str)
video_update_args.add_argument("views", type=str)
video_update_args.add_argument("likes", type=str)

Videos = {}

class HelloWorld(Resource):
    def get(self, name):
        if name in names:
            return names[name]
        else:
            return {"message": "Name not found"}, 404

def abort_video_does_not_exists(video_id):
    if video_id not in collection[video_id]:
        abort(404, message="Video id is not valid......\nPlease enter the correct video id")

def abort_video_if_exists(video_id):
    if video_id in collection[video_id]:
        abort(409, message="Video already exists with the id...")

class Videos(Resource):

    def get(self, video_id):
        video_data = collection.find_one({"_id": video_id})
        if video_data:
            return video_data
        else:
            return {"message": "Video not found"}, 404  
          
    def put(self, video_id):
        abort_video_if_exists(video_id)
        args = video_put_args.parse_args()
        video_data = {
            "_id": video_id,
            "name": args["name"],
            "likes": args["likes"],
            "views": args["views"]
        }
        collection.insert_one(video_data)
        return video_data, 201
    
    def delete(self, video_id):
        abort_video_does_not_exists(video_id)
        collection.delete_one({"_id": video_id})
        return "deleted sucessfully", 204
    
    def patch(self, video_id):
        args = video_update_args.parse_args()

        update_data = {} 
        
        if args["name"]:
            update_data["name"] = args["name"]
        if args["views"]:
            update_data["views"] = args["views"]
        if args["likes"]:
            update_data["likes"] = args["likes"]

        result = collection.update_many({"_id": video_id}, {"$set": update_data})
        if result.modified_count == 1:
            return update_data, 200
        else:
            return {"message": "Video not found"}, 404


api.add_resource(Videos, "/video/<int:video_id>")



if __name__ == "__main__":
    app.run(debug=True)