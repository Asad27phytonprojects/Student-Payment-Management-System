CREATE TABLE records (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    marks INT CHECK (marks >= 0 AND marks <= 100)
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(10) NOT NULL,
    payment_month DATE NOT NULL,
    status ENUM('Paid', 'Pending', 'Late') DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES records(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Optional demo data
INSERT INTO records (student_name, subject, marks) VALUES
('Ali Khan', 'Mathematics', 85),
('Sara Ahmed', 'Physics', 90),
('Hassan Raza', 'Computer Science', 78),
('Ayesha Noor', 'English', 88),
('Bilal Hussain', 'Chemistry', 92);

INSERT INTO payments (student_id, payment_month, amount, payment_method, status) VALUES
(1, '2025-01-01', 5000.00, 'Cash', 'Paid'),
(1, '2025-02-01', 5000.00, 'Cash', 'Paid'),
(2, '2025-01-01', 4800.00, 'Card', 'Paid'),
(2, '2025-02-01', 4800.00, 'Card', 'Pending'),
(3, '2025-01-01', 5200.00, 'Cash', 'Late'),
(4, '2025-01-01', 5000.00, 'Card', 'Paid'),
(5, '2025-02-01', 5300.00, 'Cash', 'Pending'),
(5, '2025-03-01', 5300.00, 'Cash', 'Paid');

