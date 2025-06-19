from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registers a new user with validation."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    
    # --- ADDED VALIDATION ---
    if len(username) < 5:
        return jsonify({"msg": "Username must be at least 5 characters long"}), 400
    if len(password) < 8:
        return jsonify({"msg": "Password must be at least 8 characters long"}), 400
    # --- END OF VALIDATION ---

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409

    new_user = User(username=username, role='user')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Logs in a user and returns an access token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # --- FIX 1: Correct token creation ---
        # Identity is now just the user's ID (as a string).
        # The role is passed as an additional claim.
        identity = str(user.id)
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=identity, additional_claims=additional_claims)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401


# Custom decorator to check for a specific role
def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # --- FIX 2: Correctly check the role from additional claims ---
            verify_jwt_in_request()
            claims = get_jwt()
            # The role is now a top-level claim, not nested under 'sub'
            if claims.get("role") != required_role:
                return jsonify(msg=f"Access denied: '{required_role}' role required!"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@auth_bp.route('/profile')
@jwt_required()
def my_profile():
    """An example protected route that returns the logged-in user's data."""
    # --- FIX 3: Fetch user data based on the identity from the token ---
    # get_jwt_identity() now returns the user's ID as a string
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Return safe user information
    user_data = {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
    return jsonify(logged_in_as=user_data), 200


@auth_bp.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    """An example admin-only route."""
    return jsonify(message="Welcome to the Admin Dashboard!")
