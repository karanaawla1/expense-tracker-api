# Expense Tracker API

A personal expense tracking REST API I built to learn backend development with Python and Flask. It lets users register, log their daily expenses, organize them by category, and view monthly spending summaries.

---

## Why I built this

I wanted a simple way to track where my money goes every month. Instead of using an existing app, I thought — why not build one myself and learn backend along the way? So here it is.

---

## Tech used

- Python 3.x
- Flask
- SQLAlchemy (ORM)
- SQLite (database)
- JWT for authentication
- Postman for API testing

---

## Project structure

```
expense-tracker/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes/
│       ├── auth.py
│       ├── categories.py
│       ├── expenses.py
│       └── summary.py
├── main.py
├── requirements.txt
├── schema.sql
└── ExpenseTracker.postman_collection.json
```

---

## How to run it locally

```bash
# 1. Clone the repo
git clone https://github.com/karanaawla1/expense-tracker-api.git
cd expense-tracker-api

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python main.py
```

Server runs at `http://localhost:5000`

---

## Authentication

After registering or logging in, you'll get a JWT token. Pass it in every request header like this:

```
Authorization: Bearer <your_token>
```

---

## API Endpoints

### Auth
| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | /api/auth/register | Create a new account |
| POST | /api/auth/login | Login and get token |
| GET | /api/auth/me | View your profile |

### Categories
| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /api/categories/ | List all your categories |
| POST | /api/categories/ | Add a new category |
| PUT | /api/categories/:id | Rename a category |
| DELETE | /api/categories/:id | Delete a category |

### Expenses
| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /api/expenses/ | Get all expenses |
| GET | /api/expenses/?category_id=1 | Filter by category |
| GET | /api/expenses/?start_date=2024-03-01&end_date=2024-03-31 | Filter by date range |
| POST | /api/expenses/ | Add a new expense |
| PUT | /api/expenses/:id | Edit an expense |
| DELETE | /api/expenses/:id | Delete an expense |

### Summary
| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /api/summary/total | Total spending |
| GET | /api/summary/total?month=3&year=2024 | Monthly total |
| GET | /api/summary/by-category | Breakdown by category |
| GET | /api/summary/monthly?year=2024 | Full year overview |

---

## Testing with Postman

Import the `ExpenseTracker.postman_collection.json` file into Postman. Set the `BASE_URL` to `http://localhost:5000`, then:

1. Hit the **Register** request
2. Copy the `access_token` from the response
3. Set it as the `TOKEN` variable
4. Everything else should work from there

---

## Sample request

**POST** `/api/expenses/`
```json
{
  "title": "Swiggy Order",
  "amount": 250,
  "date": "2024-03-15",
  "category_id": 1,
  "description": "Late night food"
}
```

**Response:**
```json
{
  "message": "Expense added successfully",
  "expense": {
    "id": 1,
    "title": "Swiggy Order",
    "amount": 250.0,
    "category": "Food",
    "date": "2024-03-15"
  }
}
```

---

## What I learned

- How to structure a Flask project using Blueprints
- JWT-based authentication flow
- SQLAlchemy ORM and database relationships
- Writing clean REST APIs with proper status codes
- Filtering and aggregating data from a database

---

## Author

**Karan Aawla**  
GitHub: [@karanaawla1](https://github.com/karanaawla1)
