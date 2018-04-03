INSERT INTO categories(category)
VALUES ('sports'), ('music'), ('creative arts'), ('collecting');

INSERT INTO interests(interest)
VALUES ('tennis'), ('piano'), ('football'), ('3D printing'), ('stamp collecting'), 
		('cooking'), ('reading'), ('flute'), ('guitar'), ('golf'), ('volleyball'), 
		('coin collecting'), ('knitting'), ('sewing'), ('woodwork'), ('painting');

INSERT INTO interest_category(interest, category)
VALUES ('tennis', 'sports'), ('piano', 'music'), ('football', 'sports'), ('3D printing', 'creative arts'), 
('stamp collecting', 'collecting'), ('flute', 'music'), ('guitar', 'music'), ('golf', 'sports'),
('volleyball', 'sports'), ('coin collecting', 'collecting'), ('knitting', 'creative arts'),
('sewing','creative arts'), ('woodwork','creative arts'), ('painting','creative arts');

INSERT INTO Client( ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status)
VALUES (045783475, 'Jennie', 'female', '1981-07-19', '2028855700', 'green', 120, 64, 'no', 'male', '2017-04-06',NULL, 'active'),
	   (123567823, 'John', 'male', '1980-10-21', '2028978394', 'blue',170, 70, 'no', 'female', '2017-02-25',NULL, 'active'),
	   (758393228, 'Jill', 'female', '1978-07-19','2029362918', 'brown', 115, 63, 'yes', 'male', '2014-04-19', NULL, 'active'),
	   (234765283, 'Charles', 'male', '1975-08-09', '3059872634', 'green', 220, 68, 'no', 'female', '2016-08-16', '2016-08-19', 'criminal_closed');

INSERT INTO Children (ssn, childName, ChildDOB, childStatus)
VALUES(758393228, 'Henry', '2005-05-25', 'shared custody');
		
INSERT INTO CriminalRecord(ssn, crime)
VALUES (234765283, 'drug possession');


INSERT INTO Fees(ssn, date_incurred, fee_type, payment_amount, status)
VALUES (045783475, '2017-04-06', 'registration fee', 100, 'paid'),
		(123567823, '2017-02-25', 'registration fee', 100, 'paid'),
		(758393228, '2014-04-19', 'registration fee', 100, 'paid'),
		(234765283, '2016-08-16', 'registration fee', 100, 'paid');


INSERT INTO client_interests(ssn, interest)
VALUES (045783475, 'tennis'), (045783475, 'cooking'), (045783475, 'piano'), 
	   (123567823, 'football'), (123567823, '3D printing'), (123567823, 'stamp collecting'),
	   (758393228, 'cooking'), (758393228, 'painting'), (758393228, 'guitar');