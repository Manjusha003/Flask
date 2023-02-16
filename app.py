from flask import Flask, appcontext_popped, request, jsonify

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

# app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Flask"]

    @app.route("/register", methods=["POST"])
    def create_data():
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"})
        result = db.student.insert_one(data)
        return (
            jsonify(
                {
                    "message": "Student is created successfully",
                    "payload": {"_id": str(result.inserted_id)},
                    "sucess": True,
                }
            ),
            200,
        )

    @app.route("/students", methods=["GET"])
    def get_students():
        query = request.args.to_dict()
        data = list(db.student.find())
        group_by = query.get("groupBy")

        if group_by is not None:
            group = [
                {"$group": {"_id": f"${group_by}", "name": {"$push": "$name"}}},
                {"$project": {group_by: "$_id", "_id": 0, "name": "$name"}},
            ]
            agregated_data = db.student.aggregate(group)
            agregated_list = list(agregated_data)
            return (
                jsonify(
                    {
                        "message": "fetched data",
                        "payload": {"data": agregated_list},
                        "sucess": True,
                    }
                ),
                200,
            )

        order_by = query.get("orderBy")
        if order_by is not None:
            student = db.student.find({}, {"_id": 0}).sort(order_by)
            student_order = list(student)
            return (
                jsonify(
                    {
                        "message": "fetched data",
                        "payload": {"data": student_order},
                        "sucess": True,
                    }
                ),
                200,
            )

        if query.get("page") is not None:
            if query.get("pageSize") is not None:
                start = (int(query.get("page")) - 1) * int(query.get("pageSize"))
                end = int(query.get("page")) * int(query.get("pageSize"))
                student = db.student.find({}, {"_id": 0}).skip(start).limit(end)

                paginated_data = list(student)

                return (
                    jsonify(
                        {
                            "message": "fetched data",
                            "payload": {"data": paginated_data},
                            "sucess": True,
                        }
                    ),
                    200,
                )

        for student in data:
            student["_id"] = str(student["_id"])

        return (
            jsonify(
                {"message": "fetched data", "payload": {"data": data}, "sucess": True}
            ),
            200,
        )

    @app.route("/students/<objectid>", methods=["GET", "PUT", "DELETE"])
    def update_student(objectid):
        data = {"_id": ObjectId(objectid)}
        student = db.student.find_one(data)

        if request.method == "GET":
            return json.loads(dumps(student))

        if request.method == "PUT":
            updated_data = db.student.update_one(data, {"$set": request.get_json()})
            print(data)
            if updated_data.modified_count == 1:
                return jsonify(
                    {
                        "message": "Student updated successfully",
                        "sucess": True,
                        "payload": {"id": objectid},
                    },
                    {"status": 200},
                )
            return jsonify(
                {
                    "message": "Student is not present with given id",
                    "sucess": True,
                    "payload": {"id": objectid},
                },
                {"status": 200},
            )

        if request.method == "DELETE":
            delete_data = db.student.delete_one(data)
            return jsonify(
                {
                    "message": "Student deleted successfully",
                    "sucess": True,
                    "payload": {"id": objectid},
                },
                200,
            )


    return app
# if __name__ == '__main__':
#   app.run(debug=True,port=5000)
