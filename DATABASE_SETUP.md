# Booksphere Database Setup Guide

## Overview
This setup provides a complete PostgreSQL database for the Booksphere library management system, running on Docker Desktop.

## Database Structure

### Tables

#### 1. **users** - Library members
- `id` (INT, Primary Key): Unique user ID
- `name` (VARCHAR): User's full name
- `membership_id` (VARCHAR): Unique membership identifier
- `email` (VARCHAR): User's email
- `created_at`, `updated_at` (TIMESTAMP): Audit timestamps

#### 2. **books** - Library inventory
- `id` (INT, Primary Key): Unique book ID
- `name` (VARCHAR): Book title
- `author` (VARCHAR): Author name
- `stock_quantity` (INT): Current number of copies available
- `created_at`, `updated_at` (TIMESTAMP): Audit timestamps

#### 3. **book_borrowings** - Borrowing transactions
- `id` (INT, Primary Key): Transaction ID
- `user_id` (INT, FK): Reference to users table
- `book_id` (INT, FK): Reference to books table
- `borrowed_date` (TIMESTAMP): When the book was borrowed
- `due_date` (TIMESTAMP): When the book must be returned (15 days from borrowed_date)
- `returned_date` (TIMESTAMP): When the book was actually returned
- `renewal_count` (INT): Number of times renewed
- `status` (VARCHAR): 'borrowed', 'returned', 'renewed', 'overdue'
- `created_at`, `updated_at` (TIMESTAMP): Audit timestamps

#### 4. **admin_logs** - Admin activity tracking
- `id` (INT, Primary Key): Log entry ID
- `admin_name` (VARCHAR): Name of admin performing the action
- `book_id` (INT, FK): Book being updated
- `action` (VARCHAR): Type of action (e.g., 'add_stock', 'remove_stock')
- `quantity_changed` (INT): Amount of change
- `old_quantity`, `new_quantity` (INT): Before/after values
- `notes` (TEXT): Additional notes about the change
- `created_at` (TIMESTAMP): When the action occurred

## Getting Started

### Prerequisites
- Docker Desktop installed and running
- Docker Compose v3.8 or higher

### Step 1: Start the Database

```bash
docker-compose up -d
```

This command:
- Starts a PostgreSQL 15 container named `booksphere_db`
- Initializes the database with the schema from `db-init.sql`
- Creates sample data (3 users, 5 books)
- Exposes the database on `localhost:5432`

### Step 2: Verify the Database is Running

```bash
docker-compose ps
```

You should see:
```
booksphere_db    postgres:15-alpine    Up (healthy)
```

### Step 3: Connect to the Database

#### Using psql (PostgreSQL CLI)
```bash
docker exec -it booksphere_db psql -U booksphere_user -d booksphere_db
```

#### Connection Details
- **Host**: `postgres` (from Docker) or `localhost` (from host machine)
- **Port**: `5432`
- **Database**: `booksphere_db`
- **Username**: `booksphere_user`
- **Password**: `booksphere_password`

### Step 4: Connect from Your Application

**Python (using psycopg2)**:
```python
import psycopg2

conn = psycopg2.connect(
    host="postgres",  # or "localhost" if running outside Docker
    database="booksphere_db",
    user="booksphere_user",
    password="booksphere_password",
    port="5432"
)
```

**Python (using SQLAlchemy)**:
```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://booksphere_user:booksphere_password@postgres:5432/booksphere_db"
)
```

**Node.js (using pg)**:
```javascript
const { Client } = require('pg');

const client = new Client({
    host: 'postgres',
    port: 5432,
    database: 'booksphere_db',
    user: 'booksphere_user',
    password: 'booksphere_password'
});
```

## Business Logic Implementation

### 15-Day Borrowing Rule
Every book borrowed must be returned or renewed after 15 days:
- `due_date` is automatically set to `borrowed_date + 15 days`
- An admin can check for overdue books using the query below
- Status becomes 'overdue' if not returned/renewed by due_date

### Admin Functions

#### Update Stock (Add Books)
```sql
-- Admin adds 10 copies of "The Great Gatsby"
INSERT INTO admin_logs (admin_name, book_id, action, quantity_changed, old_quantity, new_quantity, notes)
SELECT 'John Admin', 1, 'add_stock', 10, stock_quantity, stock_quantity + 10, 'New delivery'
FROM books WHERE id = 1;

UPDATE books SET stock_quantity = stock_quantity + 10 WHERE id = 1;
```

#### Remove Stock (Lost/Damaged Books)
```sql
-- Admin removes 1 copy due to damage
INSERT INTO admin_logs (admin_name, book_id, action, quantity_changed, old_quantity, new_quantity, notes)
SELECT 'John Admin', 1, 'remove_stock', -1, stock_quantity, stock_quantity - 1, 'Book damaged during return'
FROM books WHERE id = 1;

UPDATE books SET stock_quantity = stock_quantity - 1 WHERE id = 1;
```

### User Functions

#### Borrow a Book
```sql
INSERT INTO book_borrowings (user_id, book_id, due_date)
VALUES (1, 1, CURRENT_TIMESTAMP + INTERVAL '15 days');

UPDATE books SET stock_quantity = stock_quantity - 1 WHERE id = 1;
```

#### Return a Book
```sql
UPDATE book_borrowings 
SET status = 'returned', returned_date = CURRENT_TIMESTAMP
WHERE id = 1;

UPDATE books SET stock_quantity = stock_quantity + 1 WHERE id = 1;
```

#### Renew a Book
```sql
UPDATE book_borrowings 
SET status = 'renewed', due_date = CURRENT_TIMESTAMP + INTERVAL '15 days', renewal_count = renewal_count + 1
WHERE id = 1;
```

### Useful Queries

#### Find All Overdue Books
```sql
SELECT 
    u.name,
    u.membership_id,
    b.name,
    b.author,
    bb.borrowed_date,
    bb.due_date,
    (bb.due_date - CURRENT_TIMESTAMP) as days_overdue
FROM book_borrowings bb
JOIN users u ON bb.user_id = u.id
JOIN books b ON bb.book_id = b.id
WHERE bb.status = 'borrowed' AND bb.due_date < CURRENT_TIMESTAMP
ORDER BY bb.due_date DESC;
```

#### Book Availability
```sql
SELECT name, author, stock_quantity 
FROM books 
ORDER BY stock_quantity DESC;
```

#### User Borrowing History
```sql
SELECT 
    b.name,
    b.author,
    bb.borrowed_date,
    bb.due_date,
    bb.returned_date,
    bb.status
FROM book_borrowings bb
JOIN books b ON bb.book_id = b.id
WHERE bb.user_id = 1
ORDER BY bb.borrowed_date DESC;
```

#### Admin Activity Log
```sql
SELECT * FROM admin_logs 
ORDER BY created_at DESC 
LIMIT 20;
```

## Docker Commands

### Start the database
```bash
docker-compose up -d
```

### Stop the database
```bash
docker-compose down
```

### Stop and remove all data
```bash
docker-compose down -v
```

### View logs
```bash
docker-compose logs -f postgres
```

### Access the database directly
```bash
docker exec -it booksphere_db psql -U booksphere_user -d booksphere_db
```

## Troubleshooting

### Database won't start
Check logs:
```bash
docker-compose logs postgres
```

### Connection refused
- Ensure Docker Desktop is running
- Check if port 5432 is available
- Wait 10-15 seconds for the database to be fully ready

### Reset the database
```bash
docker-compose down -v
docker-compose up -d
```

This will remove all data and recreate the database with sample data.

## Next Steps

1. Update `app/` to use the database connection string
2. Implement API endpoints for:
   - Creating users and books
   - Borrowing and returning books
   - Renewing books
   - Admin stock management
   - Checking overdue books

3. Add authentication/authorization for admin functions
4. Implement notifications for overdue books (email, SMS, etc.)
