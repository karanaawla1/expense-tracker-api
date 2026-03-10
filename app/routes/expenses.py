from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Expense
from datetime import datetime

expenses_bp = Blueprint("expenses", __name__)


@expenses_bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = int(get_jwt_identity())

    # Optional filters from query params
    category_id = request.args.get("category_id", type=int)
    start_date = request.args.get("start_date")  # format: YYYY-MM-DD
    end_date = request.args.get("end_date")

    query = Expense.query.filter_by(user_id=user_id)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(Expense.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    if end_date:
        query = query.filter(Expense.date <= datetime.strptime(end_date, "%Y-%m-%d").date())

    expenses = query.order_by(Expense.date.desc()).all()
    return jsonify([e.to_dict() for e in expenses]), 200


@expenses_bp.route("/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()
    return jsonify(expense.to_dict()), 200


@expenses_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    required_fields = ("title", "amount")
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "title and amount are required"}), 400

    if data["amount"] <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    expense_date = datetime.utcnow().date()
    if "date" in data:
        expense_date = datetime.strptime(data["date"], "%Y-%m-%d").date()

    expense = Expense(
        title=data["title"],
        amount=data["amount"],
        description=data.get("description"),
        date=expense_date,
        category_id=data.get("category_id"),
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "message": "Expense added successfully",
        "expense": expense.to_dict()
    }), 201


@expenses_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()

    data = request.get_json()

    if "title" in data:
        expense.title = data["title"]
    if "amount" in data:
        if data["amount"] <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
        expense.amount = data["amount"]
    if "description" in data:
        expense.description = data["description"]
    if "date" in data:
        expense.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    if "category_id" in data:
        expense.category_id = data["category_id"]

    db.session.commit()
    return jsonify({
        "message": "Expense updated successfully",
        "expense": expense.to_dict()
    }), 200


@expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200
