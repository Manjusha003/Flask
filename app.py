from flask import Flask, Response, request, jsonify
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads

app = Flask(__name__)


client = MongoClient("mongodb://localhost:27017/")
db = client["Flask"]


@app.route("/register", methods=["POST"])
def create_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"})
    result = db.student.insert_one(data)
    return jsonify(
        {
            "message": "Student is created successfully",
            "payload": {"_id": str(result.inserted_id)},
            "success": True,
        },
        200,
    )


@app.route("/students", methods=["GET"])
def get_students():
    data = list(db.student.find())
    for student in data:
        student["_id"] = str(student["_id"])

    return (
        jsonify({"message": "fetched data", "payload": {"data": data}, "sucess": True}),
        {"status": 200},
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
                    "payload": {"id": id},
                },
                200
            )
        return jsonify(
            {
                "message": "Student is not present with given id",
                "sucess": True,
                "payload": {"id": "id"},
            },
            200
        )

    if request.method == "DELETE":
        delete_data = db.student.delete_one(data)
        return jsonify(
            {
                "message": "Student deleted successfully",
                "sucess": True,
                "payload": {"id": "id"},
            },
            200
        )


if __name__ == "__main__":
    app.run(debug=True)
