-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    device_type TEXT, -- e.g., 'mobile', 'desktop', 'tablet'
    source TEXT -- e.g., 'Google', 'Facebook', 'Organic', 'Direct'
);

-- Events Table
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type TEXT, -- 'visit', 'product_view', 'add_to_cart', 'checkout_start', 'purchase'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    revenue REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- Campaigns Table
CREATE TABLE IF NOT EXISTS campaigns (
    source TEXT PRIMARY KEY,
    cost REAL,
    start_date DATETIME
);
