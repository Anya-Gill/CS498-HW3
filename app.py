from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference
from pymongo.write_concern import WriteConcern
from pymongo.errors import PyMongoError

app = Flask(__name__)

MONGO_URI = "mongodb+srv://anyagillind_db_user:ntNJ5rO7jSIygodM@cluster0.twbpouw.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["ev_db"]
base_collection = db["vehicles"]

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    try:
        doc = request.get_json()
        if not doc:
            return jsonify({"error": "No JSON body provided"}), 400

        fast_collection = base_collection.with_options(
            write_concern=WriteConcern(w=1)
        )
        result = fast_collection.insert_one(doc)
        return jsonify({"inserted_id": str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    try:
        doc = request.get_json()
        if not doc:
            return jsonify({"error": "No JSON body provided"}), 400

        safe_collection = base_collection.with_options(
            write_concern=WriteConcern(w="majority")
        )
        result = safe_collection.insert_one(doc)
        return jsonify({"inserted_id": str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    try:

        primary_collection = base_collection.with_options(
            read_preference=ReadPreference.PRIMARY
        )
        count = primary_collection.count_documents({"Make": "TESLA"})
        return jsonify({"count": count}), 200

    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    try:

        secondary_collection = base_collection.with_options(
            read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        count = secondary_collection.count_documents({"Make": "BMW"})
        return jsonify({"count": count}), 200

    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)