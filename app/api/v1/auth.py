from datetime import timedelta
import json
import random
from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import check_password_hash
from app.helpers.email import send_mail
from app.helpers.utils import create_response
from app.models.credentials import Credentials
from app.schemas.login import LoginSchema
from flask_jwt_extended import create_access_token, decode_token
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    
    data = request.json
    request_data = LoginSchema(**data).model_dump()
    user = Credentials.objects(email=data.get('email')).first()

    if user.update_password == False:
        return create_response(False,"Update your password to login",None,None,400)
    
    if not user or not check_password_hash(user.password, data.get('password')):
        return create_response(False,'Email or Password Incorrect',None,None,401)
    
    access_token = create_access_token(identity=str(user.user_id), additional_claims={'roles': user.user_type},expires_delta=timedelta(hours=2) )
    result = {
        'access_token':access_token,
        **json.loads(user.to_json())
    }
    result.pop("password", None)
    return create_response(True, 'Login successfull', result, None, 200)


@auth_bp.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
   
    user = Credentials.objects(email=data.get('email')).first()
    if not user :
        return create_response(False,'User does not exists',None,None,401)
    otp_number = random.randint(100000, 999999)

    token = create_access_token(identity=str(data.get('email')), additional_claims={'otp_number': otp_number,'email':data.get('email')},expires_delta=timedelta(minutes=10) )
    result = {
        'token':token,        
    }

    html_template = render_template('forgot_password_template.html',otp_number=otp_number)
    send_mail(data.get('email'),"Password Reset OTP",html_template,'hrm25085@gmail.com')

    return create_response(True, 'Otp sent successfully', result, None, 200)


@auth_bp.route('/verify_otp', methods=['PUT'])
def verify_otp():

    data = request.json
    token = decode_token(data.get('token'))

    otp_number = token.get('otp_number')
    email_id = token.get('email')

    if (otp_number) != (data.get('otp_number')):
        return create_response(False,"Otp mismatch",None,None,400)
    
    hashed_password = generate_password_hash(data['password'])

    update_password = Credentials.objects(email = email_id).first()
    update_password.update(password = hashed_password )
    
    return create_response(True, 'Otp verified and updated successfully', None, None, 200)



@auth_bp.route('/update_password', methods=['PUT'])
def update_password():
    data = request.json
    user = Credentials.objects(email=data.get('email')).first()
   
    if not user :
        return create_response(False,'Incorrect email',None,None,401)
    
    if not check_password_hash(user.password, data.get('old_password')):
        return create_response(False,"Password mismatch",None,None,401)
    
    hashed_password = generate_password_hash(data['new_password'])
    update_password = user.update(password = hashed_password,update_password = True)
    return create_response(True, 'Password updated successfully', None, None, 200)