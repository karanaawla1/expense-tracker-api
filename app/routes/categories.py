from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Category

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    user_id = int(get_jwt_identity())
    categories = Category.query.filter_by(user_id=user_id).all()
    return jsonify([c.to_dict() for c in categories]), 200


@categories_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    existing = Category.query.filter_by(name=data["name"], user_id=user_id).first()
    if existing:
        return jsonify({"error": "Category already exists"}), 409

    category = Category(name=data["name"], user_id=user_id)
    db.session.add(category)
    db.session.commit()

    return jsonify({
        "message": "Category created successfully",
        "category": category.to_dict()
    }), 201


@categories_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    user_id = int(get_jwt_identity())
    category = Category.query.filter_by(id=category_id, user_id=user_id).first_or_404()

    data = request.get_json()
    if "name" in data:
        category.name = data["name"]

    db.session.commit()
    return jsonify({
        "message": "Category updated",
        "category": category.to_dict()
    }), 200


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    user_id = int(get_jwt_identity())
    category = Category.query.filter_by(id=category_id, user_id=user_id).first_or_404()

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200
