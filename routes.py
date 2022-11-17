from flask import Flask, request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
import datetime
import json

#getting out heart data function
def getHeartData():
    try:
        with open ('./heart_rate.json', 'r') as jsonData:
            heartData = json.load(jsonData)
        return heartData
    except NameError:
        print("Name Error")

#modifying our heart data function
def writeHeartData(heartData):
    try:
        with open ('./heart_rate.json', 'w') as writeJson:
            writeJson.write(json.dumps(heartData))
    except NameError:
        print("Name Error")

#heart post (publish the data inside the json file) and get (read the data)
class HeartRate(Resource):
    def get(self):
        return jsonify(getHeartData())

    def post(self):
        heart = request.get_json()
        heartData = getHeartData()

        id = 1 if len(heartData) <= 0 else heartData[-1].get('id') + 1

        newHeart = {
            "id": id,
            "heart_rate": heart["heart_rate"],
            "date": str(datetime.datetime.now())
        }

        heartData.append(newHeart)
        writeHeartData(heartData)
        return jsonify(heartData)

#Searching for the specific heart data
#Deleting heart data
#
class HeartSearch(Resource):
    def get(self, id):

        heartData = getHeartData()
        selectedHeart = ''

        for data in heartData:
            if(data.get("id") == int(id)):
                selectedHeart = data
    
        if(selectedHeart == ''):
            res = make_response()
            return make_response(jsonify({"message": "No Heart Data is existing!"}), 404)

        return jsonify(selectedHeart())
    
    @jwt_required()
    def patch(self, id):
        req = request.get_json()
        heartData = getHeartData()
        selectedHeart = ''

        for data in heartData:
                if(data.get("id") == int(id)):
                    selectedHeart = data

        if(selectedHeart == ''): return make_response(jsonify({"message": "No Heart Data is existing!"}), 404)
        if(req.get("heart_rate") != None): selectedHeart["heart_rate"] = req.get("heart_rate")

        writeHeartData(heartData)
        return jsonify(heartData)
    
    @jwt_required()
    def delete(self, id):
        req = request.get_json()

        heartData = getHeartData()

        selectedHeart = ''

        for data in heartData:
                if(data.get("id") != int(id)):
                    selectedHeart.append(data)

        heartData = selectedHeart
        writeHeartData(heartData)
        return jsonify(heartData)

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')

        if username != 'admin':
            return make_response(jsonify({"message": "Wrong Credentials!"}), 401)

        expire = datetime.timedelta(days=1)
        access_token = create_access_token(identity=username, expires_delta=expire)

        return make_response({"access_token": access_token}, 200)


