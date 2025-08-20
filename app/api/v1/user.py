from flask import Blueprint, request, jsonify
from app.models.user import Users
from app.schemas.user import UserSchema
from app.exceptions import APIException
from app.decorators.auth import require_scope

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = UserSchema(**request.json)
    user = Users(username=data.username, email=data.email, password='changeme', roles=['user'])
    user.save()
    return jsonify({'id': str(user.id), 'username': user.username, 'status': 'success'}), 201

@user_bp.route('/', methods=['GET'])
def get_users():
    users = Users.objects.all()
    return jsonify({
        'users': [{'id': str(user.id), 'username': user.username, 'email': user.email} for user in users],
        'status': 'success'
    }), 200

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = Users.objects.get(id=user_id)
        return jsonify({
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'status': 'success'
        }), 200
    except Users.DoesNotExist:
        raise APIException("User not found", 404)

@user_bp.route('/admin-only', methods=['GET'])
@require_scope('admin')
def admin_only():
    return jsonify({'msg': 'You are an admin!'}) 