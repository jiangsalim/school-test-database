-- ============================================
-- JINJA SENIOR SECONDARY SCHOOL
-- Existing School Database Setup
-- ============================================

CREATE DATABASE IF NOT EXISTS school_test_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_general_ci;

-- Create read-only user for OneCard
DROP USER IF EXISTS 'onecard_readonly'@'localhost';
CREATE USER 'onecard_readonly'@'localhost' IDENTIFIED BY 'OneCard@2026';
GRANT SELECT ON school_test_db.* TO 'onecard_readonly'@'localhost';
FLUSH PRIVILEGES;

USE school_test_db;

-- ============================================
-- STUDENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS students (
    admission_number VARCHAR(20) PRIMARY KEY COMMENT 'Format: YY-Level-Serial (26-3-5029)',
    full_name VARCHAR(100) NOT NULL,
    current_class VARCHAR(20) NOT NULL COMMENT 'Senior 1 to Senior 6',
    stream VARCHAR(10) NOT NULL COMMENT 'A to H',
    payment_code VARCHAR(20) UNIQUE NOT NULL COMMENT 'Format: 101{CC}{Serial}',
    category ENUM('day', 'hostel') DEFAULT 'day' COMMENT 'Day Scholar or Hostel Student',
    reg_no VARCHAR(20) DEFAULT '',
    subject_combination VARCHAR(50) DEFAULT '' COMMENT 'A-Level only',
    date_of_birth DATE,
    gender ENUM('M', 'F'),
    parent_name VARCHAR(100) DEFAULT '',
    parent_phone VARCHAR(15) DEFAULT '',
    student_phone VARCHAR(15) DEFAULT '',
    photo_path VARCHAR(255) DEFAULT '',
    status VARCHAR(10) DEFAULT 'active',
    admission_date DATE,
    INDEX idx_payment_code (payment_code),
    INDEX idx_class_stream (current_class, stream),
    INDEX idx_status (status),
    INDEX idx_category (category)
) ENGINE=InnoDB;

-- ============================================
-- PAYMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_code VARCHAR(20) NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_date DATETIME NOT NULL,
    payment_method VARCHAR(20) COMMENT 'MTN_UG, Airtel_UG, Bank Transfer, Cash',
    transaction_id VARCHAR(50),
    channel_memo TEXT,
    description TEXT,
    term VARCHAR(10),
    academic_year VARCHAR(10),
    INDEX idx_payment_code (payment_code),
    INDEX idx_payment_date (payment_date)
) ENGINE=InnoDB;

-- ============================================
-- CLASSES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS classes (
    class_name VARCHAR(20) PRIMARY KEY,
    level ENUM('O', 'A'),
    class_teacher VARCHAR(50)
);

-- ============================================
-- TERMS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS terms (
    term_name VARCHAR(10),
    academic_year VARCHAR(10),
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (term_name, academic_year)
);

-- ============================================
-- STAFF TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS staff (
    staff_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    role VARCHAR(30),
    phone VARCHAR(15)
);

-- ============================================
-- SEED DATA: CLASSES
-- ============================================
INSERT INTO classes VALUES
('Senior 1', 'O', 'Mr. Odoi'),
('Senior 2', 'O', 'Ms. Birungi'),
('Senior 3', 'O', 'Mr. Waiswa'),
('Senior 4', 'O', 'Ms. Akello'),
('Senior 5', 'A', 'Mr. Ssali'),
('Senior 6', 'A', 'Ms. Nalule');

-- ============================================
-- SEED DATA: TERMS
-- ============================================
INSERT INTO terms VALUES
('Term 1', '2026', '2026-01-15', '2026-04-30'),
('Term 2', '2026', '2026-05-15', '2026-08-15'),
('Term 3', '2026', '2026-09-01', '2026-12-05');

-- ============================================
-- SEED DATA: STAFF
-- ============================================
INSERT INTO staff VALUES
('STF-001', 'Mr. Okello', 'Head Teacher', '0772404055'),
('STF-002', 'Ms. Nalule', 'Bursar', '0771234567'),
('STF-003', 'Mr. Odoi', 'Gate Staff', '0779876543'),
('STF-004', 'Mr. Waiswa', 'Class Teacher (S.3)', '0775555555'),
('STF-005', 'Ms. Birungi', 'Class Teacher (S.2)', '0776666666');

SELECT '✅ School database tables and seed data created!' AS status;