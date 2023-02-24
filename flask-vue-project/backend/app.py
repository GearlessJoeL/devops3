from flask import Flask, request
from flask.views import MethodView
from flask_cors import CORS
from models import Device, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:@127.0.0.1:3306/test1?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors = CORS()
cors.init_app(app)

@app.route('/')
def hello():
    return 'hello'

@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    User.init_db()
    Device.init_db()

class user_model_api(MethodView):
    def get(self, user_id):
        if not user_id:
            users  = User.query.all()
            results = [
                {
                    'id': user.id,
                    'username' : user.username,
                    'password' : user.password,
                    'email' : user.email,
                    'character' : user.character
                } for user in users
            ]
            return {
                'status' : 'success',
                'message' : 'query done',
                'results' : results
            }
        user = User.query.get(user_id)
        return {
            'status' : 'success',
            'message' : 'query done',
            'results' : {
                'id': user.id,
                'username' : user.username,
                'password' : user.password,
                'email' : user.email,
                'character' : user.character
            }
        }
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'delete successfully'
        }
    
    def put(self, user_id):
        user = User.query.get(user_id)
        user.username = request.json.get('username')
        user.password = request.json.get('password')
        user.email = request.json.get('email')
        user.character = request.json.get('character')
        db.session.commit()
        return {
            'status': 'success',
            'message': 'put successfully'
        }

    def post(self):
        form = request.json
        user = User()
        user.id = form.get('id')
        user.username = form.get('username')
        user.password = form.get('password')
        user.email = form.get('email')
        user.character = form.get('character')
        db.session.add(user)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'post successfully'
        }
    
class device_model_api(MethodView):
    def get(self, device_id):
        if not device_id:
            devices  = Device.query.all()
            results = [
                {
                    'device_id': device.device_id,
                    'device_name' : device.device_name,
                    'user_id' : device.user_id,
                    'device_temperature' : device.device_temperature,
                    'device_humidity' : device.device_humidity
                } for device in devices
            ]
            return {
                'status' : 'success',
                'message' : 'query done',
                'results' : results
            }
        device = device.query.get(device_id)
        return {
            'status' : 'success',
            'message' : 'query done',
            'results' : {
                'device_id': device.device_id,
                'device_name' : device.device_name,
                'user_id' : device.user_id,
                'device_temperature' : device.device_temperature,
                'device_humidity' : device.device_humidity
            }
        }
    
    def delete(self, device_id):
        device = Device.query.get(device_id)
        db.session.delete(device)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'delete successfully'
        }
    
    def put(self, device_id):
        device = Device.query.get(device_id)
        device.device_name = request.json.get('device_name')
        device.user_id = request.json.get('user_id')
        device.device_temperature = request.json.get('device_temperature')
        device.device_humidity = request.json.get('device_humidity')
        db.session.commit()
        return {
            'status': 'success',
            'message': 'put successfully'
        }

    def post(self):
        form = request.json
        device = Device()
        device.device_id = form.get('device_id')
        device.device_name = form.get('device_name')
        device.user_id = form.get('user_id')
        device.device_temperature = form.get('device_temperature')
        device.device_humidity = form.get('device_humidity')
        db.session.add(device)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'post successfully'
        }

user_view = user_model_api.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id' : None}, view_func=user_view, methods=['GET'])
app.add_url_rule('/users', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

device_view = device_model_api.as_view('device_api')
app.add_url_rule('/devices/', defaults={'device_id' : None}, view_func=device_view, methods=['GET'])
app.add_url_rule('/devices', view_func=device_view, methods=['POST'])
app.add_url_rule('/devices/<int:device_id>', view_func=device_view, methods=['GET', 'PUT', 'DELETE'])


if __name__ == '__main__':
    app.run(debug=True)