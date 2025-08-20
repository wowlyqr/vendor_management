
import random
import string


def serialize_data(user):
    user_dict = user.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict


def create_response(success, message, data=None, error=None, status_code=200):
    return {
        "success": success,
        "message": message,
        "data": data if data else {},
        "error": error if error else None
    }, status_code


def generate_uniform_unique_id(prefix = None):
    # prefix = "pl"
    constant = "VM"
    
    # Generate two 4-digit random segments
    random_segment1 = ''.join(random.choices(string.ascii_uppercase, k=4))
    random_segment2 = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
    # Combine to form the ID
    formatted_id = f"{prefix}-{random_segment1}-{constant}-{random_segment2}"
    return formatted_id