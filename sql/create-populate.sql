DROP DATABASE IF EXISTS ds;
CREATE DATABASE ds;
USE ds;

GRANT ALL ON user280.* TO user280@localhost IDENTIFIED BY 'psswrd';

CREATE TABLE Client(
ssn INT PRIMARY KEY NOT NULL,
name VARCHAR(60) DEFAULT ' ',
gender CHAR(8) NOT NULL,
dob DATE NOT NULL,
phone CHAR(11) NOT NULL,
eyecolor CHAR(15) NOT NULL,
weight INT NOT NULL,
height INT NOT NULL,
prior_marriage CHAR(3) NOT NULL,
interest CHAR(8) NOT NULL,
date_open DATE NOT NULL,
date_close DATE NULL,
status VARCHAR(120) NOT NULL
);

CREATE TABLE CriminalRecord(
ssn INT NOT NULL,
crime VARCHAR(60),
PRIMARY KEY(ssn, crime),
FOREIGN KEY(ssn) REFERENCES Client(ssn)
);

CREATE TABLE Children(
ssn INT NOT NULL,
childName VARCHAR(60) NOT NULL,
childDOB DATE NOT NULL,
childStatus VARCHAR(80) NOT NULL,
PRIMARY KEY(ssn, childName),
FOREIGN KEY(ssn) REFERENCES Client(ssn)
);

CREATE TABLE dates(
c1_ssn INT NOT NULL,
c2_ssn INT NOT NULL,
location VARCHAR(40) NOT NULL,
scheduled_date DATE NOT NULL,
occured CHAR(3) NULL,
interested CHAR(3) NULL,
see_again CHAR(3) NULL,
PRIMARY KEY(c1_ssn, c2_ssn),
FOREIGN KEY(c1_ssn) REFERENCES Client(ssn),
FOREIGN KEY(c2_ssn) REFERENCES Client(ssn)
);

CREATE TABLE Fees(
ssn INT NOT NULL,
date_incurred DATE NOT NULL,
fee_type CHAR(30) NOT NULL,
payment_amount INT NOT NULL,
status CHAR(8) NOT NULL,
PRIMARY KEY(ssn, date_incurred),
FOREIGN KEY(ssn) REFERENCES Client(ssn)
);


INSERT INTO Client( ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status)
VALUES (045783475, 'Jennie', 'female', '1991-07-19', '2028855700', 'green', 120, 64, 'n', 'male', '2017-04-06',NULL, 'active'),
		(123567823, 'John', 'male', '1990-10-21', '2028978394', 'blue',170, 70, 'n', 'female', '2017-02-25',NULL, 'active');
