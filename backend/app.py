from cmath import exp
from urllib import response
from flask import Flask, request, Response
from flask_cors import CORS
import pymongo
import json
from bson .objectid import ObjectId

#init app
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/CRUDtestdb'

CORS(app)

try:
    mongo = pymongo.MongoClient(
        host="localhost", 
        port = 27017,
        serverSelectionTimeoutMS = 1000 #Catch exception
        )
    db = mongo.CRUDtestdb #database name
    mongo.server_info() #Start exception if cannot connect
except: 
    print('ERROR - Cannot connect to database')


@app.route('/users', methods = ['POST'])
def createUsers():
    try:
        user = {
        'type_dni': request.json['type_dni'],
        'dni': request.json['dni'],
        'name': request.json['name'],
        'last_name': request.json['last_name'],
        'hobbie': request.json['hobbie']
        }
        dbResponse = db.users.insert_one(user)
        #print(dbResponse.inserted_id)
        return Response(
            #json de respuesta  
            response = json.dumps({
                'message': 'Usuario Creado', 
                'id': f"{dbResponse.inserted_id}"
            }), 
            status= 200, #Status indicando que todo OK
            mimetype="application/json" #typedata
        )
    except Exception as ex:
        print(ex)
        return Response(
            #json de respuesta  
            response = json.dumps({'message': 'ERROR - Usuario no pueden ser creado'}), 
            status= 500, #Error interno
            mimetype="application/json" #typedata
        )

@app.route('/users', methods = ['GET'])
def getUsers():
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user['_id']) #Id as string without objectId
        return Response(
            #json de respuesta  
            response = json.dumps(data), 
            status= 200, #OK
            mimetype="application/json" #typedata
        )
    except Exception as ex:
        print(ex)
        return Response(
            #json de respuesta  
            response = json.dumps({'message': 'ERROR - Usuario no pueden ser leidos'}), 
            status= 500, #Error interno
            mimetype="application/json" #typedata
        )

@app.route('/users/<id>', methods = ['DELETE'])
def deleteUser(id):
    try:
        dbResponse = db.users.delete_one({'_id': ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                #json de respuesta  
                response = json.dumps({
                    'message': 'Usuario Eliminado',
                    'id':f'{id}'}), 
                status= 200, #OK
                mimetype="application/json" #typedata
            )
        else:
            return Response(
                #json de respuesta  
                response = json.dumps({
                    'message': 'Usuario no encontrado',
                    'id':f'{id}'}), 
                status= 200, #OK
                mimetype="application/json" #typedata
            )
    except Exception as ex:
        print(ex)
        return Response(
            #json de respuesta  
            response = json.dumps({'message': 'ERROR - Usuario no puede ser eliminado'}), 
            status= 500, #Error interno
            mimetype="application/json" #typedata
        )

@app.route('/users/<id>', methods = ['PATCH'])
def updateUser(id):
    try:
        dbResponse = db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'type_dni':request.json['type_dni'],
                      'dni':request.json['dni'],
                      'name':request.json['name'],
                      'last_name':request.json['last_name'],
                      'hobbie':request.json['hobbie'],
            }}
        )
        if dbResponse.modified_count == 1:
            return Response(
                #json de respuesta  
                response = json.dumps({'message': 'Usuario Actualizado'}), 
                status= 200, #OK
                mimetype="application/json" #typedata
            )
        else:
            return Response(
                #json de respuesta  
                response = json.dumps({'message': 'No hay nada que actualizar'}), 
                status= 200, #OK
                mimetype="application/json" #typedata
            )

    except Exception as ex:
        print(ex)
        return Response(
            #json de respuesta  
            response = json.dumps({'message': 'ERROR - No se puede actualizar'}), 
            status= 500, #Error interno
            mimetype="application/json" #typedata
        )

@app.route('/<id>', methods = ['GET'])
def getone(id):
    try:
        dbResponse = db.users.find_one({'_id': ObjectId(id)})
        if dbResponse['_id'] != None: 
            return Response(
                #json de respuesta  
                response = json.dumps({'message': 'ID encontrado',
                '_id': str(dbResponse['_id']),
                'name': str(dbResponse['name']),
                'last_name': str(dbResponse['last_name']),
                'type_dni': str(dbResponse['type_dni']),
                'dni': str(dbResponse['dni']),
                'hobbie': str(dbResponse['hobbie'])
                }),
                status= 200, #OK
                mimetype="application/json" #typedata
            )
        else:
            return Response(
                #json de respuesta  
                response = json.dumps({'message': 'ID no encontrado'}), 
                status= 200, #OK
                mimetype="application/json" #typedata
            )


    except Exception as ex:
        print(ex)
        return Response(
            #json de respuesta  
            response = json.dumps({'message': 'ERROR - No se puede encontrar data'}), 
            status= 500, #Error interno
            mimetype="application/json" #typedata
        )


if __name__ == "__main__":
    app.run(debug=True)
