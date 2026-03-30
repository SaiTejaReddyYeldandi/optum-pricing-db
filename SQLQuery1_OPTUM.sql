CREATE DATABASE PricingDB;
GO
USE PricingDB;
GO


USE PricingDB;
GO

CREATE TABLE Products (
  ProductID   INT PRIMARY KEY IDENTITY(1,1),
  ProductName NVARCHAR(200) NOT NULL,
  Category    NVARCHAR(100),
  BasePrice   DECIMAL(10,2),
  CreatedAt   DATETIME DEFAULT GETDATE()
);

CREATE TABLE Customers (
  CustomerID   INT PRIMARY KEY IDENTITY(1,1),
  CustomerName NVARCHAR(200) NOT NULL,
  Tier         NVARCHAR(50),
  Region       NVARCHAR(100),
  CreatedAt    DATETIME DEFAULT GETDATE()
);

CREATE TABLE Bids (
  BidID      INT PRIMARY KEY IDENTITY(1,1),
  ProductID  INT FOREIGN KEY REFERENCES Products(ProductID),
  CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
  BidAmount  DECIMAL(10,2),
  BidDate    DATETIME DEFAULT GETDATE(),
  Status     NVARCHAR(50)
);

CREATE TABLE Pricing (
  PricingID       INT PRIMARY KEY IDENTITY(1,1),
  ProductID       INT FOREIGN KEY REFERENCES Products(ProductID),
  CustomerID      INT FOREIGN KEY REFERENCES Customers(CustomerID),
  NegotiatedPrice DECIMAL(10,2),
  EffectiveDate   DATE,
  ExpiryDate      DATE
);

CREATE TABLE Transactions (
  TxnID      INT PRIMARY KEY IDENTITY(1,1),
  ProductID  INT FOREIGN KEY REFERENCES Products(ProductID),
  CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
  Quantity   INT,
  UnitPrice  DECIMAL(10,2),
  TxnDate    DATETIME DEFAULT GETDATE()
);


USE PricingDB;
GO

-- Insert Products
INSERT INTO Products (ProductName, Category, BasePrice) VALUES
('Lipitor 10mg',    'Cholesterol',  45.99),
('Metformin 500mg', 'Diabetes',     12.50),
('Lisinopril 5mg',  'Blood Pressure', 8.75),
('Atorvastatin',    'Cholesterol',  38.00),
('Amoxicillin',     'Antibiotic',   15.25),
('Omeprazole',      'Gastric',      22.00),
('Sertraline',      'Mental Health', 30.00),
('Amlodipine',      'Blood Pressure', 11.00);

-- Insert Customers
INSERT INTO Customers (CustomerName, Tier, Region) VALUES
('Cigna Health',      'Platinum', 'Northeast'),
('Aetna Insurance',   'Gold',     'Southeast'),
('BlueCross IL',      'Gold',     'Midwest'),
('Humana Plans',      'Silver',   'South'),
('UnitedHealth',      'Platinum', 'National'),
('CVS Caremark',      'Gold',     'National'),
('Express Scripts',   'Platinum', 'National'),
('Anthem Inc',        'Silver',   'West');

-- Insert Pricing
INSERT INTO Pricing (ProductID, CustomerID, NegotiatedPrice, EffectiveDate, ExpiryDate) VALUES
(1, 1, 38.00, '2025-01-01', '2025-12-31'),
(1, 2, 40.00, '2025-01-01', '2025-12-31'),
(2, 3, 10.00, '2025-01-01', '2025-12-31'),
(3, 4,  7.50, '2025-01-01', '2025-12-31'),
(4, 5, 30.00, '2025-01-01', '2025-12-31'),
(5, 6, 12.00, '2025-01-01', '2025-12-31'),
(6, 7, 18.00, '2025-01-01', '2025-12-31'),
(7, 8, 25.00, '2025-01-01', '2025-12-31');

-- Insert Transactions
INSERT INTO Transactions (ProductID, CustomerID, Quantity, UnitPrice, TxnDate) VALUES
(1, 1, 500,  38.00, '2025-03-01'),
(1, 2, 300,  40.00, '2025-03-05'),
(2, 3, 1000, 10.00, '2025-03-07'),
(3, 4, 750,   7.50, '2025-03-10'),
(4, 5, 400,  30.00, '2025-03-12'),
(5, 6, 600,  12.00, '2025-03-15'),
(6, 7, 200,  18.00, '2025-03-18'),
(7, 8, 350,  25.00, '2025-03-20'),
(1, 5, 450,  35.00, '2025-04-01'),
(2, 1, 800,   9.50, '2025-04-05');

-- Insert Bids
INSERT INTO Bids (ProductID, CustomerID, BidAmount, Status) VALUES
(1, 1, 36.00, 'Won'),
(1, 2, 41.00, 'Lost'),
(2, 3,  9.50, 'Won'),
(3, 4,  8.00, 'Lost'),
(4, 5, 29.00, 'Won'),
(5, 6, 13.00, 'Lost'),
(6, 7, 17.50, 'Won'),
(7, 8, 26.00, 'Lost');



USE PricingDB;
GO

-- 1. Basic: All products with their base price
SELECT ProductName, Category, BasePrice
FROM Products
ORDER BY BasePrice DESC;

-- 2. JOIN: Negotiated price vs base price per customer
SELECT 
  c.CustomerName, c.Tier,
  p.ProductName,
  p.BasePrice,
  pr.NegotiatedPrice,
  p.BasePrice - pr.NegotiatedPrice AS Discount
FROM Pricing pr
JOIN Products p  ON pr.ProductID  = p.ProductID
JOIN Customers c ON pr.CustomerID = c.CustomerID
ORDER BY Discount DESC;

-- 3. GROUP BY: Total revenue per product
SELECT 
  p.ProductName,
  SUM(t.Quantity * t.UnitPrice) AS TotalRevenue,
  COUNT(t.TxnID)                AS NumTransactions
FROM Transactions t
JOIN Products p ON t.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalRevenue DESC;

-- 4. WINDOW FUNCTION: Rank customers by total spend
SELECT 
  c.CustomerName,
  SUM(t.Quantity * t.UnitPrice) AS TotalSpend,
  RANK() OVER (ORDER BY SUM(t.Quantity * t.UnitPrice) DESC) AS SpendRank
FROM Transactions t
JOIN Customers c ON t.CustomerID = c.CustomerID
GROUP BY c.CustomerName
ORDER BY SpendRank;

-- 5. CTE: Customers spending above average
WITH CustomerSpend AS (
  SELECT 
    c.CustomerName,
    SUM(t.Quantity * t.UnitPrice) AS TotalSpend
  FROM Transactions t
  JOIN Customers c ON t.CustomerID = c.CustomerID
  GROUP BY c.CustomerName
)
SELECT *, 
  CASE WHEN TotalSpend > (SELECT AVG(TotalSpend) FROM CustomerSpend) 
       THEN 'Above Average' 
       ELSE 'Below Average' END AS SpendCategory
FROM CustomerSpend
ORDER BY TotalSpend DESC;




USE PricingDB;
GO

-- 1. Insert a new pricing record
CREATE PROCEDURE usp_InsertPricing
  @ProductID INT, @CustomerID INT,
  @Price DECIMAL(10,2), @Start DATE, @End DATE
AS BEGIN
  INSERT INTO Pricing(ProductID, CustomerID, NegotiatedPrice, EffectiveDate, ExpiryDate)
  VALUES(@ProductID, @CustomerID, @Price, @Start, @End)
  PRINT 'Pricing record inserted successfully'
END
GO

-- 2. Get top N bids by value
CREATE PROCEDURE usp_GetTopBids
  @TopN INT = 10
AS BEGIN
  SELECT TOP(@TopN)
    p.ProductName, c.CustomerName, c.Tier,
    b.BidAmount, b.Status, b.BidDate
  FROM Bids b
  JOIN Products  p ON b.ProductID  = p.ProductID
  JOIN Customers c ON b.CustomerID = c.CustomerID
  ORDER BY b.BidAmount DESC
END
GO

-- 3. Calculate discount for a customer+product
CREATE PROCEDURE usp_GetDiscount
  @ProductID INT, @CustomerID INT
AS BEGIN
  SELECT
    p.ProductName, c.CustomerName,
    p.BasePrice, pr.NegotiatedPrice,
    p.BasePrice - pr.NegotiatedPrice AS DiscountAmount,
    ROUND((p.BasePrice - pr.NegotiatedPrice) / p.BasePrice * 100, 2) AS DiscountPct
  FROM Pricing pr
  JOIN Products  p ON pr.ProductID  = p.ProductID
  JOIN Customers c ON pr.CustomerID = c.CustomerID
  WHERE pr.ProductID = @ProductID AND pr.CustomerID = @CustomerID
END
GO

-- 4. Get bid win rate per customer
CREATE PROCEDURE usp_BidWinRate
AS BEGIN
  SELECT
    c.CustomerName, c.Tier,
    COUNT(*) AS TotalBids,
    SUM(CASE WHEN b.Status = 'Won' THEN 1 ELSE 0 END) AS WonBids,
    ROUND(SUM(CASE WHEN b.Status = 'Won' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS WinRatePct
  FROM Bids b
  JOIN Customers c ON b.CustomerID = c.CustomerID
  GROUP BY c.CustomerName, c.Tier
  ORDER BY WinRatePct DESC
END
GO

-- 5. Audit log table + update price procedure
CREATE TABLE PriceAuditLog (
  AuditID    INT PRIMARY KEY IDENTITY(1,1),
  PricingID  INT, OldPrice DECIMAL(10,2),
  NewPrice   DECIMAL(10,2), ChangedAt DATETIME DEFAULT GETDATE()
);
GO

CREATE PROCEDURE usp_UpdatePrice
  @PricingID INT, @NewPrice DECIMAL(10,2)
AS BEGIN
  DECLARE @OldPrice DECIMAL(10,2)
  SELECT @OldPrice = NegotiatedPrice FROM Pricing WHERE PricingID = @PricingID
  UPDATE Pricing SET NegotiatedPrice = @NewPrice WHERE PricingID = @PricingID
  INSERT INTO PriceAuditLog(PricingID, OldPrice, NewPrice)
  VALUES(@PricingID, @OldPrice, @NewPrice)
  PRINT 'Price updated and audit log written'
END
GO

EXEC usp_GetTopBids 5;
EXEC usp_GetDiscount 1, 1;
EXEC usp_BidWinRate;


USE PricingDB;
GO

-- Speed up joins on foreign keys
CREATE INDEX IX_Pricing_ProductID    ON Pricing(ProductID);
CREATE INDEX IX_Pricing_CustomerID   ON Pricing(CustomerID);
CREATE INDEX IX_Transactions_Product ON Transactions(ProductID);
CREATE INDEX IX_Transactions_Customer ON Transactions(CustomerID);
CREATE INDEX IX_Bids_Status          ON Bids(Status);

-- Covering index for the discount query
CREATE INDEX IX_Pricing_Cover 
ON Pricing(ProductID, CustomerID) 
INCLUDE (NegotiatedPrice, EffectiveDate, ExpiryDate);
GO


-- Check your indexes were created
SELECT 
  i.name AS IndexName,
  t.name AS TableName,
  i.type_desc
FROM sys.indexes i
JOIN sys.tables t ON i.object_id = t.object_id
WHERE i.name IS NOT NULL
ORDER BY t.name;