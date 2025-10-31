from flask import Blueprint, jsonify
from .core import compute_odds

router = Blueprint('router', __name__, url_prefix='/router')

@router.route('/', methods=['GET'])
def index():
    return jsonify(compute_odds(2))
