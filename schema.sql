-- =========================================
-- EXPENSE TRACKER - DATABASE SCHEMA
-- =========================================

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(150)  NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORIES TABLE
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    user_id     INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(name, user_id)  -- Each user has unique category names
);

-- EXPENSES TABLE
CREATE TABLE IF NOT EXISTS expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       VARCHAR(200) NOT NULL,
    amount      REAL NOT NULL CHECK(amount > 0),
    description TEXT,
    date        DATE NOT NULL DEFAULT CURRENT_DATE,
    category_id INTEGER,
    user_id     INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- =========================================
-- SAMPLE DATA (for testing)
-- =========================================

-- Insert sample user (password: Test@123)
INSERT INTO users (name, email, password_hash) VALUES
('Karan Aawla', 'karan@example.com', 'pbkdf2:sha256:...');

-- Insert sample categories
INSERT INTO categories (name, user_id) VALUES
('Food', 1),
('Transport', 1),
('Shopping', 1),
('Entertainment', 1),
('Health', 1),
('Bills', 1);

-- Insert sample expenses
INSERT INTO expenses (title, amount, description, date, category_id, user_id) VALUES
('Swiggy Order', 250.00, 'Dinner from Swiggy', '2024-03-01', 1, 1),
('Uber Ride', 120.00, 'Office to home', '2024-03-02', 2, 1),
('Amazon Purchase', 1500.00, 'Bought a book', '2024-03-05', 3, 1),
('Movie Ticket', 300.00, 'Weekend movie', '2024-03-08', 4, 1),
('Electricity Bill', 800.00, 'Monthly bill', '2024-03-10', 6, 1),
('Gym Membership', 999.00, 'Monthly gym fee', '2024-03-12', 5, 1);
