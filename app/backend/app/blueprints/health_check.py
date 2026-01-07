from flask import Blueprint, jsonify,request,g
from flask import current_app as app
import time

health_bp = Blueprint("health", __name__, url_prefix="/health")

## CONSTANTS

## HELPER FUNCTIONS 

## MAIN ROUTES


@health_bp.route("/check", methods=["GET"])
def health():
    return jsonify({"message": "OK"}), 200


@health_bp.route("/tests",methods=["GET"])
def run_tests():
    return jsonify({
        "msg" :"Under Contruction"
    }),200
    




