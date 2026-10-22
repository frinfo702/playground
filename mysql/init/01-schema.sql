CREATE TABLE users (
  id         INT PRIMARY KEY AUTO_INCREMENT,
  name       VARCHAR(50)  NOT NULL,
  email      VARCHAR(100) NOT NULL,
  country    CHAR(2)      NOT NULL,
  created_at DATETIME     NOT NULL
);

-- Only user_id is indexed on purpose: experiments add/drop others.
CREATE TABLE orders (
  id         BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id    INT NOT NULL,
  amount     DECIMAL(10,2) NOT NULL,
  status     ENUM('pending','paid','shipped','cancelled') NOT NULL,
  created_at DATETIME NOT NULL,
  KEY idx_user (user_id)
);

-- Tiny table for transaction / locking experiments.
CREATE TABLE accounts (
  id      INT PRIMARY KEY,
  owner   VARCHAR(20) NOT NULL,
  balance INT NOT NULL
);
