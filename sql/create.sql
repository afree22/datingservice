DROP DATABASE IF EXISTS ds;
CREATE DATABASE ds;
USE ds;

GRANT ALL ON ds.* TO 'user280'@'localhost' IDENTIFIED BY 'psswrd' WITH GRANT OPTION;
flush privileges;


CREATE TABLE Client(
ssn INT PRIMARY KEY NOT NULL,
name VARCHAR(60) DEFAULT ' ',
gender ENUM('male', 'female') NOT NULL,
dob DATE NOT NULL,
phone CHAR(11) NOT NULL,
eyecolor CHAR(15) NOT NULL,
weight INT NOT NULL,
height INT NOT NULL,
prior_marriage ENUM('yes','no') NOT NULL,
interest ENUM('male', 'female') NOT NULL,
date_open DATE NOT NULL,
date_close DATE NULL,
status VARCHAR(120) NOT NULL
);

CREATE TABLE CriminalRecord(
ssn INT NOT NULL,
crime VARCHAR(60),
PRIMARY KEY(ssn, crime),
FOREIGN KEY(ssn) REFERENCES Client(ssn)
ON DELETE CASCADE
);

CREATE TABLE Children(
ssn INT NOT NULL,
childName VARCHAR(60) NOT NULL,
childDOB DATE NOT NULL,
childStatus VARCHAR(80) NOT NULL,
PRIMARY KEY(ssn, childName),
FOREIGN KEY(ssn) REFERENCES Client(ssn)
ON DELETE CASCADE
);

CREATE TABLE dates(
c1_ssn INT NOT NULL,
c2_ssn INT NOT NULL,
location VARCHAR(40) NOT NULL,
scheduled_date DATE NOT NULL,
occured ENUM('yes','no') NULL,
interested ENUM('yes','no') NULL,
see_again ENUM('yes','no') NULL,
PRIMARY KEY(c1_ssn, c2_ssn),
FOREIGN KEY(c1_ssn) REFERENCES Client(ssn),
FOREIGN KEY(c2_ssn) REFERENCES Client(ssn)
ON DELETE CASCADE
);

CREATE TABLE Fees(
ssn INT NOT NULL,
date_incurred DATE NOT NULL,
fee_type CHAR(30) NOT NULL,
payment_amount INT NOT NULL,
status CHAR(8) NOT NULL,
PRIMARY KEY(ssn, date_incurred),
FOREIGN KEY(ssn) REFERENCES Client(ssn)
ON DELETE CASCADE
);

CREATE TABLE OtherLogin(
username VARCHAR(15) NOT NULL,
password VARCHAR(15) NOT NULL,
use_type ENUM('specialist','entry level', 'upper level') NOT NULL,
PRIMARY KEY(username)
);

CREATE TABLE interest_category(
interest VARCHAR(30) NOT NULL,
category VARCHAR(60) NOT NULL,
PRIMARY KEY(interest)
);

CREATE TABLE client_interests(
ssn INT NOT NULL,
interest VARCHAR(30) NOT NULL,
PRIMARY KEY(ssn, interest),
FOREIGN KEY(ssn) REFERENCES Client(ssn),
FOREIGN KEY(interest) REFERENCES interest_category(interest)
ON DELETE CASCADE);


