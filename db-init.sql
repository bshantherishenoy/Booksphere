-- Booksphere Database Schema
-- Initialization script for PostgreSQL

-- Create users table (members)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    membership_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create books table (library inventory)
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create book_borrowings table (track borrowed books and their status)
CREATE TABLE book_borrowings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    borrowed_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    returned_date TIMESTAMP,
    renewal_count INTEGER DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'borrowed', -- borrowed, returned, renewed, overdue
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create admin_logs table (track all admin stock updates)
CREATE TABLE admin_logs (
    id SERIAL PRIMARY KEY,
    admin_name VARCHAR(255),
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL, -- add_stock, remove_stock, etc.
    quantity_changed INTEGER NOT NULL,
    old_quantity INTEGER NOT NULL,
    new_quantity INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_book_borrowings_user_id ON book_borrowings(user_id);
CREATE INDEX idx_book_borrowings_book_id ON book_borrowings(book_id);
CREATE INDEX idx_book_borrowings_status ON book_borrowings(status);
CREATE INDEX idx_book_borrowings_due_date ON book_borrowings(due_date);
CREATE INDEX idx_users_membership_id ON users(membership_id);
CREATE INDEX idx_books_author ON books(author);

-- Insert sample data
INSERT INTO users (name, membership_id, email) VALUES
('John Doe', 'MEM001', 'john@example.com'),
('Jane Smith', 'MEM002', 'jane@example.com'),
('Robert Johnson', 'MEM003', 'robert@example.com');

INSERT INTO books (name, author, stock_quantity) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 5),
('To Kill a Mockingbird', 'Harper Lee', 3),
('1984', 'George Orwell', 4),
('Pride and Prejudice', 'Jane Austen', 6),
('The Hobbit', 'J.R.R. Tolkien', 2);

-- Insert a sample borrowing record (due in 15 days from now)
INSERT INTO book_borrowings (user_id, book_id, borrowed_date, due_date, status) VALUES
(1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '15 days', 'borrowed'),
(2, 3, CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP + INTERVAL '10 days', 'borrowed');
