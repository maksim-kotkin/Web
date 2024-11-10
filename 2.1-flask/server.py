import flask
from flask import jsonify, request
from flask.views import MethodView
from models import Advertisement, Session
from sqlalchemy.exc import IntegrityError
from schema import  CreateAdvertisement, UpdateAdvertisement
from pydantic import ValidationError
# from flask_bcrypt import Bcrypt


app = flask.Flask('app')
# bcrypt = Bcrypt(app)


# def hash_password(password:str):
#     password = password.encode()
#     password = bcrypt.generate_password_hash(password)
#     password = password.decode()
#     return password

# def check_password(password: str, hashed_password: str):
#     password = password.encode()
#     hashed_password = hashed_password.encode()
#     return bcrypt.check_password_hash(hashed_password, password)
    
class HttpError(Exception):
    
    def __init__(self, status_code:int, error_msg: str | dict | list):
        self.status_code = status_code
        self.error_msg = error_msg
        
        
@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    http_response = jsonify({'status': 'error', 'message': err.error_msg})
    http_response.status_code = err.status_code
    return http_response


def validate_json(json_data: dict, schema_cls: type[CreateAdvertisement] | type[UpdateAdvertisement]):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)

@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def  after_request(http_response: flask.Response):
    request.session.close()
    return http_response


# def add_user(user:Advertisement):
#     try:
#         request.session.add(user)
#         request.session.commit()
#     except IntegrityError:
#         raise HttpError(409, 'user already exists')
#     return user

# def get_user(user_id: int):
#     user = request.session.get(User, user_id)
#     if user is None:
#         raise HttpError(404,'user not found')
#     return user
def add_adv(adv:Advertisement):
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, 'adv already exists')
    return adv



def get_adv(adv_id: int):
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, 'Advertisement not found')
    return adv

class AdvertisementView(MethodView):
    
    def get(self, adv_id: int):
        adv = get_adv(adv_id)
        return jsonify(adv.json)
    
    def post(self):
        json_data = validate_json(request.json, CreateAdvertisement)
        # json_data['password'] = hash_password(json_data['password'])
        adv = Advertisement(**json_data)
        adv = add_adv(adv)
        return jsonify({"id": adv.id})

    def patch(self, adv_id):
        json_data = validate_json(request.json, UpdateAdvertisement)
        # if "password" in json_data:
        #     json_data["password"] = hash_password(json_data["password"])
        adv = get_adv(adv_id)
        for field, value in json_data.items():
            setattr(adv, field, value)
        adv = get_adv(adv)
        return adv.json
    
    def delete(self, adv_id):
        adv = get_adv(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({'status': 'deleted'})
    
    
adv_view = AdvertisementView.as_view('adv')

app.add_url_rule('/adv/', view_func=adv_view, methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])

app.run()

