import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from app.database import get_connection, reset_db

# Constants for synthetic data
NUM_USERS = 2500
START_DATE = datetime.now() - timedelta(days=30)

def generate_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Generate Campaigns
    campaigns = [
        ('Google', 5000.0, START_DATE.isoformat()),
        ('Facebook', 3000.0, START_DATE.isoformat()),
        ('Organic', 0.0, START_DATE.isoformat()),
        ('Direct', 0.0, START_DATE.isoformat())
    ]
    cursor.executemany("INSERT INTO campaigns (source, cost, start_date) VALUES (?, ?, ?)", campaigns)
    
    # 2. Generate Users
    sources = ['Google', 'Facebook', 'Organic', 'Direct']
    source_weights = [0.4, 0.3, 0.2, 0.1]
    device_types = ['mobile', 'desktop', 'tablet']
    
    users = []
    
    for user_id in range(1, NUM_USERS + 1):
        source = random.choices(sources, weights=source_weights)[0]
        device = random.choices(device_types, weights=[0.6, 0.3, 0.1])[0]
        
        # Random time within last 30 days
        join_date = START_DATE + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        users.append((user_id, join_date.isoformat(), device, source))
        
    cursor.executemany("INSERT INTO users (user_id, join_date, device_type, source) VALUES (?, ?, ?, ?)", users)
    
    # 3. Generate Events & Orders
    events = []
    orders = []
    event_id = 1
    
    for user in users:
        u_id = user[0]
        device = user[2]
        current_time = datetime.fromisoformat(user[1])
        
        # 1. Visit
        events.append((event_id, u_id, 'visit', current_time.isoformat()))
        event_id += 1
        
        # 2. Product View (70% conversion from visit)
        if random.random() < 0.70:
            current_time += timedelta(seconds=random.randint(10, 120))
            events.append((event_id, u_id, 'product_view', current_time.isoformat()))
            event_id += 1
            
            # 3. Add to Cart (40% conversion from view)
            if random.random() < 0.40:
                current_time += timedelta(seconds=random.randint(20, 300))
                events.append((event_id, u_id, 'add_to_cart', current_time.isoformat()))
                event_id += 1
                
                # 4. Checkout Start 
                # -> THIS IS OUR BIG LEAK #1: Mobile users drop off heavily at cart
                checkout_prob = 0.25 if device == 'mobile' else 0.75
                
                if random.random() < checkout_prob:
                    current_time += timedelta(seconds=random.randint(15, 180))
                    events.append((event_id, u_id, 'checkout_start', current_time.isoformat()))
                    event_id += 1
                    
                    # 5. Purchase 
                    # -> THIS IS LEAK #2: Overall friction
                    if random.random() < 0.65:
                        current_time += timedelta(seconds=random.randint(60, 400))
                        events.append((event_id, u_id, 'purchase', current_time.isoformat()))
                        event_id += 1
                        
                        # Generate Order (Average Order Value ~$120)
                        revenue = round(random.gauss(120.0, 40.0), 2)
                        revenue = max(10.0, revenue) # ensure positive
                        orders.append((u_id, revenue, current_time.isoformat()))
    
    cursor.executemany("INSERT INTO events (event_id, user_id, event_type, timestamp) VALUES (?, ?, ?, ?)", events)
    cursor.executemany("INSERT INTO orders (user_id, revenue, timestamp) VALUES (?, ?, ?)", orders)
    
    conn.commit()
    conn.close()
    
    print(f"Generated {NUM_USERS} users, {len(events)} events, and {len(orders)} orders.")

if __name__ == "__main__":
    print("Resetting database...")
    reset_db()
    print("Generating synthetic data...")
    generate_data()
