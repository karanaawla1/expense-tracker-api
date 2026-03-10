from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Expense, Category
from app import db
from datetime import datetime
from sqlalchemy import func

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/total", methods=["GET"])
@jwt_required()
def total_spending():
    user_id = int(get_jwt_identity())

    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    query = Expense.query.filter_by(user_id=user_id)

    if month and year:
        query = query.filter(
            func.strftime("%m", Expense.date) == f"{month:02d}",
            func.strftime("%Y", Expense.date) == str(year)
        )
    elif year:
        query = query.filter(
            func.strftime("%Y", Expense.date) == str(year)
        )

    expenses = query.all()
    total = sum(e.amount for e in expenses)

    return jsonify({
        "total_expenses": len(expenses),
        "total_amount": round(total, 2),
        "filters": {"month": month, "year": year}
    }), 200


@summary_bp.route("/by-category", methods=["GET"])
@jwt_required()
def spending_by_category():
    user_id = int(get_jwt_identity())

    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    query = Expense.query.filter_by(user_id=user_id)

    if month and year:
        query = query.filter(
            func.strftime("%m", Expense.date) == f"{month:02d}",
            func.strftime("%Y", Expense.date) == str(year)
        )

    expenses = query.all()

    category_map = {}
    for e in expenses:
        cat_name = e.category.name if e.category else "Uncategorized"
        if cat_name not in category_map:
            category_map[cat_name] = {"count": 0, "total": 0.0}
        category_map[cat_name]["count"] += 1
        category_map[cat_name]["total"] += e.amount

    result = [
        {"category": cat, "count": data["count"], "total": round(data["total"], 2)}
        for cat, data in category_map.items()
    ]
    result.sort(key=lambda x: x["total"], reverse=True)

    return jsonify(result), 200


@summary_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = int(get_jwt_identity())
    year = request.args.get("year", type=int, default=datetime.utcnow().year)

    expenses = Expense.query.filter(
        Expense.user_id == user_id,
        func.strftime("%Y", Expense.date) == str(year)
    ).all()

    monthly_map = {str(m).zfill(2): {"month": m, "count": 0, "total": 0.0} for m in range(1, 13)}

    for e in expenses:
        m = e.date.strftime("%m")
        monthly_map[m]["count"] += 1
        monthly_map[m]["total"] += e.amount

    result = list(monthly_map.values())
    for r in result:
        r["total"] = round(r["total"], 2)

    return jsonify({"year": year, "monthly_data": result}), 200
