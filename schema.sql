CREATE DATABASE IF NOT EXISTS railway_reservation;
USE railway_reservation;

CREATE TABLE IF NOT EXISTS RAILWAY_ZONE (
    Zone_Id   INT          PRIMARY KEY,
    Zone_Name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS STATION (
    Station_Code VARCHAR(10)  PRIMARY KEY,
    Station_Name VARCHAR(100) NOT NULL,
    City         VARCHAR(100) NOT NULL,
    Zone_Id      INT,
    FOREIGN KEY (Zone_Id) REFERENCES RAILWAY_ZONE(Zone_Id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS TRAIN (
    Train_No   INT          PRIMARY KEY,
    Train_Name VARCHAR(100) NOT NULL,
    Type       VARCHAR(50)  NOT NULL,
    Zone_Id    INT,
    FOREIGN KEY (Zone_Id) REFERENCES RAILWAY_ZONE(Zone_Id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS COACH (
    Coach_No   VARCHAR(10) PRIMARY KEY,
    Coach_Type VARCHAR(50) NOT NULL,
    Train_No   INT,
    FOREIGN KEY (Train_No) REFERENCES TRAIN(Train_No)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS PASSENGER (
    Passenger_Id   INT          PRIMARY KEY AUTO_INCREMENT,
    Passenger_Name VARCHAR(100) NOT NULL,
    DOB            DATE         NOT NULL
);

CREATE TABLE IF NOT EXISTS TICKET (
    Ticket_No    INT          PRIMARY KEY AUTO_INCREMENT,
    Journey_Date DATE         NOT NULL,
    Fare         DECIMAL(8,2) NOT NULL,
    Passenger_Id INT,
    Train_No     INT,
    Coach_No     VARCHAR(10),
    FOREIGN KEY (Passenger_Id) REFERENCES PASSENGER(Passenger_Id)
        ON DELETE CASCADE,
    FOREIGN KEY (Train_No) REFERENCES TRAIN(Train_No)
        ON DELETE SET NULL,
    FOREIGN KEY (Coach_No) REFERENCES COACH(Coach_No)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS EMPLOYEE (
    Eid         INT          PRIMARY KEY AUTO_INCREMENT,
    Ename       VARCHAR(100) NOT NULL,
    Designation VARCHAR(100) NOT NULL,
    Zone_Id     INT,
    FOREIGN KEY (Zone_Id) REFERENCES RAILWAY_ZONE(Zone_Id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS PLATFORM (
    Platform_No  INT PRIMARY KEY,
    Capacity     INT NOT NULL,
    Station_Code VARCHAR(10),
    FOREIGN KEY (Station_Code) REFERENCES STATION(Station_Code)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS PAYMENT (
    Payment_Id INT          PRIMARY KEY AUTO_INCREMENT,
    Amount     DECIMAL(8,2) NOT NULL,
    Mode       VARCHAR(50)  NOT NULL,
    Ticket_No  INT,
    FOREIGN KEY (Ticket_No) REFERENCES TICKET(Ticket_No)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CANCELLATION (
    Cancel_Id     INT          PRIMARY KEY AUTO_INCREMENT,
    Refund_Amount DECIMAL(8,2) NOT NULL,
    Ticket_No     INT,
    FOREIGN KEY (Ticket_No) REFERENCES TICKET(Ticket_No)
        ON DELETE CASCADE
);

INSERT INTO RAILWAY_ZONE (Zone_Id, Zone_Name) VALUES
(1, 'Northern Railway'),
(2, 'Southern Railway'),
(3, 'Eastern Railway'),
(4, 'Western Railway'),
(5, 'Central Railway'),
(6, 'South Eastern Railway'),
(7, 'North Eastern Railway'),
(8, 'North Western Railway'),
(9, 'South Western Railway'),
(10, 'East Coast Railway'),
(11, 'West Central Railway'),
(12, 'North Central Railway'),
(13, 'South East Central Railway');

INSERT INTO STATION (Station_Code, Station_Name, City, Zone_Id) VALUES
('NDLS', 'New Delhi',          'New Delhi',   1),
('CST',  'Chhatrapati Shivaji', 'Mumbai',     5),
('HWH',  'Howrah Junction',    'Kolkata',     3),
('MAS',  'Chennai Central',    'Chennai',     2),
('BCT',  'Mumbai Central',     'Mumbai',      4),
('BPL',  'Bhopal Junction',    'Bhopal',      5),
('ADI',  'Ahmedabad Junction', 'Ahmedabad',   4),
('SBC',  'Bangalore City',     'Bengaluru',   2),
('PNBE', 'Patna Junction',     'Patna',       3),
('JP',   'Jaipur Junction',    'Jaipur',      8),
('CNB',  'Kanpur Central',     'Kanpur',      12),
('PUNE', 'Pune Junction',      'Pune',        5),
('BBS',  'Bhubaneswar',        'Bhubaneswar', 10),
('GKP',  'Gorakhpur Junction', 'Gorakhpur',   7),
('JAT',  'Jammu Tawi',         'Jammu',       1);

INSERT INTO TRAIN (Train_No, Train_Name, Type, Zone_Id) VALUES
(12301, 'Rajdhani Express',    'Rajdhani',  1),
(12951, 'Mumbai Rajdhani',     'Rajdhani',  4),
(12259, 'Duronto Express',     'Duronto',   1),
(11301, 'Udyan Express',       'Express',   5),
(12163, 'Chennai Express',     'Superfast', 2),
(12002, 'Bhopal Shatabdi',     'Shatabdi',  1),
(12476, 'Sarvodaya Express',   'Express',   8),
(12723, 'Telangana Express',   'Superfast', 2),
(22691, 'Rajdhani (Bangalore)','Rajdhani',  2),
(15001, 'Muzaffarpur Express', 'Express',   7),
(12424, 'Dibrugarh Rajdhani',  'Rajdhani',  1),
(12015, 'Ajmer Shatabdi',      'Shatabdi',  8),
(12245, 'Howrah Duronto',      'Duronto',   3),
(12626, 'Kerala Express',      'Superfast', 2),
(11019, 'Konark Express',      'Express',   5);

INSERT INTO COACH (Coach_No, Coach_Type, Train_No) VALUES
('A1',  'AC First Class',    12301),
('B1',  'AC 2 Tier',         12301),
('C1',  'AC 3 Tier',         12951),
('S1',  'Sleeper',           11301),
('S2',  'Sleeper',           12163),
('G1',  'General',           11301),
('A2',  'AC First Class',    12002),
('B2',  'AC 2 Tier',         12002),
('C2',  'AC 3 Tier',         12476),
('S3',  'Sleeper',           15001),
('A3',  'AC First Class',    12424),
('B3',  'AC 2 Tier',         12015),
('C3',  'AC 3 Tier',         12245),
('S4',  'Sleeper',           12626),
('G2',  'General',           11019);

INSERT INTO PASSENGER (Passenger_Id, Passenger_Name, DOB) VALUES
(1,  'Ravi Kumar',        '1995-03-14'),
(2,  'Sunita Sharma',     '1988-07-22'),
(3,  'Arjun Mehta',       '2000-11-05'),
(4,  'Priya Nair',        '1993-01-30'),
(5,  'Vikram Singh',      '1985-09-18'),
(6,  'Anjali Gupta',      '1998-06-12'),
(7,  'Rohit Verma',       '1991-04-25'),
(8,  'Neha Joshi',        '2002-12-08'),
(9,  'Sanjay Patel',      '1979-08-03'),
(10, 'Deepa Reddy',       '1996-02-17'),
(11, 'Kunal Kapoor',      '1994-05-19'),
(12, 'Pooja Hegde',       '1999-10-13'),
(13, 'Manish Pandey',     '1989-09-10'),
(14, 'Shruti Hassan',     '1992-01-28'),
(15, 'Aditya Roy',        '1997-11-16'),
(16, 'Aakash Varma',      '1993-04-18'),
(17, 'Bhavna Sen',        '1996-08-25'),
(18, 'Chetan Bhagat',     '1987-12-03'),
(19, 'Divya Nair',        '2001-07-14'),
(20, 'Eshwar Prasad',     '1982-03-29'),
(21, 'Farhan Akhtar',     '1995-10-11'),
(22, 'Gauri Shinde',      '1990-05-06'),
(23, 'Himanshu Kohli',    '1998-09-22'),
(24, 'Ishita Dutta',      '2003-01-17'),
(25, 'Jitendra Kumar',    '1991-11-30'),
(26, 'Kavya Madhavan',    '1994-06-15'),
(27, 'Lokesh Kanagaraj',  '1986-03-21'),
(28, 'Meera Jasmine',     '1990-12-09'),
(29, 'Naveen Polishetty', '1989-10-04'),
(30, 'Oviya Helen',       '1992-04-29');

INSERT INTO TICKET (Ticket_No, Journey_Date, Fare, Passenger_Id, Train_No, Coach_No) VALUES
(1001, '2026-11-05', 1800.00, 1,  12301, 'B1'),
(1002, '2026-11-06', 2500.00, 2,  12951, 'A1'),
(1003, '2026-11-07', 1200.00, 3,  11301, 'S1'),
(1004, '2026-11-08', 950.00,  4,  12163, 'S2'),
(1005, '2026-11-09', 1550.00, 5,  12002, 'A2'),
(1006, '2026-11-10', 780.00,  6,  12476, 'C2'),
(1007, '2026-11-11', 2100.00, 7,  22691, 'C1'),
(1008, '2026-11-12', 630.00,  8,  15001, 'S3'),
(1009, '2026-11-13', 1350.00, 9,  12259, 'B1'),
(1010, '2026-11-14', 870.00,  10, 12723, 'S2'),
(1011, '2026-11-15', 2250.00, 11, 12424, 'A3'),
(1012, '2026-11-16', 1450.00, 12, 12015, 'B3'),
(1013, '2026-11-17', 1650.00, 13, 12245, 'C3'),
(1014, '2026-11-18', 820.00,  14, 12626, 'S4'),
(1015, '2026-11-19', 450.00,  15, 11019, 'G2'),
(1016, '2026-11-20', 1950.00, 16, 12301, 'B1'),
(1017, '2026-11-21', 2600.00, 17, 12951, 'A1'),
(1018, '2026-11-22', 1150.00, 18, 11301, 'S1'),
(1019, '2026-11-23', 920.00,  19, 12163, 'S2'),
(1020, '2026-11-24', 1600.00, 20, 12002, 'A2'),
(1021, '2026-11-25', 750.00,  21, 12476, 'C2'),
(1022, '2026-11-26', 2150.00, 22, 22691, 'C1'),
(1023, '2026-11-27', 680.00,  23, 15001, 'S3'),
(1024, '2026-11-28', 1420.00, 24, 12259, 'B1'),
(1025, '2026-11-29', 890.00,  25, 12723, 'S2'),
(1026, '2026-11-30', 2300.00, 26, 12424, 'A3'),
(1027, '2026-12-01', 1480.00, 27, 12015, 'B3'),
(1028, '2026-12-02', 1700.00, 28, 12245, 'C3'),
(1029, '2026-12-03', 850.00,  29, 12626, 'S4'),
(1030, '2026-12-04', 500.00,  30, 11019, 'G2');

INSERT INTO EMPLOYEE (Eid, Ename, Designation, Zone_Id) VALUES
(1,  'Ramesh Yadav',     'Station Master',    1),
(2,  'Kavitha Iyer',     'Ticket Collector',  2),
(3,  'Suresh Bose',      'Loco Pilot',        3),
(4,  'Meena Pillai',     'Guard',             4),
(5,  'Arun Tiwari',      'Porter',            5),
(6,  'Geeta Chauhan',    'Booking Clerk',     1),
(7,  'Prakash Mishra',   'Station Master',    6),
(8,  'Lalitha Devi',     'Ticket Collector',  2),
(9,  'Mohit Sharma',     'Loco Pilot',        7),
(10, 'Sita Kumari',      'Booking Clerk',     8),
(11, 'Harish Rawat',     'Station Master',    12),
(12, 'Nandini Das',      'Ticket Collector',  10),
(13, 'Rajendra Chawla',  'Loco Pilot',        11),
(14, 'Preeti Deshmukh',  'Guard',             5),
(15, 'Vijay Raghavan',   'Booking Clerk',     9);

INSERT INTO PLATFORM (Platform_No, Capacity, Station_Code) VALUES
(1,  500, 'NDLS'),
(2,  450, 'NDLS'),
(3,  600, 'CST'),
(4,  550, 'HWH'),
(5,  400, 'MAS'),
(6,  350, 'BCT'),
(7,  300, 'BPL'),
(8,  250, 'ADI'),
(9,  200, 'SBC'),
(10, 180, 'JP'),
(11, 480, 'CNB'),
(12, 520, 'PUNE'),
(13, 380, 'BBS'),
(14, 420, 'GKP'),
(15, 310, 'JAT');

INSERT INTO PAYMENT (Payment_Id, Amount, Mode, Ticket_No) VALUES
(1,  1800.00, 'UPI',  1001),
(2,  2500.00, 'Card', 1002),
(3,  1200.00, 'Cash', 1003),
(4,  950.00,  'UPI',  1004),
(5,  1550.00, 'Card', 1005),
(6,  780.00,  'Cash', 1006),
(7,  2100.00, 'UPI',  1007),
(8,  630.00,  'Cash', 1008),
(9,  1350.00, 'UPI',  1009),
(10, 870.00,  'Card', 1010),
(11, 2250.00, 'UPI',  1011),
(12, 1450.00, 'Card', 1012),
(13, 1650.00, 'Cash', 1013),
(14, 820.00,  'UPI',  1014),
(15, 450.00,  'Cash', 1015),
(16, 1950.00, 'UPI',  1016),
(17, 2600.00, 'Card', 1017),
(18, 1150.00, 'Cash', 1018),
(19, 920.00,  'UPI',  1019),
(20, 1600.00, 'Card', 1020),
(21, 750.00,  'Cash', 1021),
(22, 2150.00, 'UPI',  1022),
(23, 680.00,  'Cash', 1023),
(24, 1420.00, 'UPI',  1024),
(25, 890.00,  'Card', 1025),
(26, 2300.00, 'UPI',  1026),
(27, 1480.00, 'Card', 1027),
(28, 1700.00, 'Cash', 1028),
(29, 850.00,  'UPI',  1029),
(30, 500.00,  'Card', 1030);

INSERT INTO CANCELLATION (Cancel_Id, Refund_Amount, Ticket_No) VALUES
(1,  1440.00, 1001),
(2,  2000.00, 1002),
(3,  960.00,  1003),
(4,  760.00,  1004),
(5,  1240.00, 1005),
(6,  1800.00, 1011),
(7,  1160.00, 1012),
(8,  1320.00, 1013),
(9,  656.00,  1014),
(10, 360.00,  1015);
