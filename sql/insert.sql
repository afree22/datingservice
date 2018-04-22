INSERT INTO Client( ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status) 
VALUES (123567823, 'John', 'male','1980-10-21','2028978394','blue', 170, 70, 'no', 'female', '2017-02-25', NULL, 'active'),
	   (234765283, 'Charles', 'male', '1975-08-09', '3059872634', 'green', 220, 68, 'no', 'female', '2016-08-16', '2016-08-19', 'criminal_closed'),
	   (103456987, 'Noah', 'male', '1982-03-14',  '2159872834', 'blue', 178, 72, 'yes', 'female', '2013-05-23', NULL, 'active'),
	   (553128394, 'Mason', 'male', '1988-02-23', '4135768490', 'brown', 176, 71, 'yes', 'female', '2015-09-15', '2015-09-18', 'criminal_closed'),
	   (333453243, 'Liam', 'male', '1982-10-12', '2155738492', 'green', 175, 72, 'no', 'female', '2017-08-14', NULL, 'active'),
	   (443453242, 'Jacob', 'male', '1984-07-18', '4136475849', 'brown', 148, 66, 'no', 'female', '2016-09-02', NULL, 'active'),
	   (101987923, 'Emily', 'female', '1984-01-19', '3150593849', 'brown', 128, 66, 'yes', 'male', '2016-11-16', NULL, 'active'),
	   (203948290, 'Ava', 'female', '1985-12-19', '2158837483', 'blue', 135, 67, 'yes', 'male', '2016-12-02', NULL, 'active'),
	   (465173892, 'Jerrica', 'female', '1982-04-02', '2059038044', 'blue', 120, 64, 'no', 'male', '2018-01-20', NULL, 'active'),
	   (758393228, 'Jill', 'female', '1978-07-19','2029362918', 'brown', 115, 63, 'yes', 'male', '2014-04-19', NULL, 'active'),
	   (145783475, 'Jennie', 'female', '1981-07-19', '2028855700', 'green', 120, 64, 'no', 'male', '2017-04-06', NULL, 'active');

INSERT INTO Children (ssn, childName, ChildDOB, childStatus)
VALUES(758393228, 'Henry', '2005-05-25', 'shared custody'), 
      (758393228, 'James', '2005-05-25', 'shared custody'),
      (103456987, 'Abbey', '2007-12-18', 'full custody');

		
INSERT INTO CriminalRecord(ssn, crime)
VALUES (234765283, 'drug possession'), (553128394, 'money laundering'), 
	   (553128394, 'burglary'), (553128394, 'drug possession'), (553128394, 'arson');


INSERT INTO Fees(ssn, date_incurred, fee_type, payment_amount, fee_status)
VALUES (123567823, '2017-02-25', 'registration fee', 100, 'paid'),
		(234765283, '2016-08-16', 'registration fee', 100, 'paid'),
		(103456987, '2013-05-23', 'registration fee', 100, 'paid'),
		(553128394, '2015-09-15', 'registration fee', 100, 'paid'),
		(333453243, '2017-08-14', 'registration fee', 100, 'paid'),
		(443453242, '2016-09-02', 'registration fee', 100, 'paid'),
		(101987923, '2016-11-16', 'registration fee', 100, 'paid'),
		(203948290, '2016-12-02', 'registration fee', 100, 'paid'),
		(465173892, '2018-01-20', 'registration fee', 100, 'overdue'),
		(758393228, '2014-04-19', 'registration fee', 100, 'paid'),
		(145783475, '2017-04-06', 'registration fee', 100, 'paid'),
		(443453242, '2017-04-10', 'match fee', 50, 'paid'),
		(443453242, '2018-01-20', 'match fee', 50, 'overdue');
		
		
INSERT INTO Dates(ssn, date_ssn, location, scheduled_date, occurred, interested, see_again)
VALUES (443453242, 101987923, "Curry and Pie", "2016-11-18", "yes", "yes", "yes"),
	   (101987923, 443453242, "Curry and Pie", "2016-11-18", "yes", "yes", "yes"),
	   (443453242, 101987923, "Zannchi", "2016-12-02", "yes", "no", "no"),
	   (101987923, 443453242, "Zannchi", "2016-12-02", "yes", "yes", "yes"),
	   (443453242, 203948290, "Mai Thai", "2016-12-10", "yes", "no", "no"),
	   (203948290, 443453242, "Mai Thai", "2016-12-10", "yes", "yes", "no"),
	   (443453242, 145783475, "Sequoia","2017-04-10", "yes", "yes", "yes"),
	   (145783475, 443453242, "Sequoia","2017-04-10", "yes", "no", "no"),
	   (465173892, 443453242, "Pizza Paradiso", "2018-01-28", "yes", "no", "no"),
	   (443453242, 465173892, "Pizza Paradiso", "2018-01-28", "yes", "yes", "yes");
	   
		
INSERT INTO interest_category(interest, category)
VALUES ('tennis', 'sports'), ('piano', 'music'), ('football', 'sports'), ('3D printing', 'creative arts'), 
	   ('stamp collecting', 'collecting'), ('flute', 'music'), ('guitar', 'music'), ('golf', 'sports'),
	   ('volleyball', 'sports'), ('coin collecting', 'collecting'), ('knitting', 'creative arts'),
	   ('sewing','creative arts'), ('woodwork','creative arts'), ('painting','creative arts');

INSERT INTO client_interests(ssn, interest)
VALUES (123567823, 'football'), (123567823, '3D printing'), (123567823, 'stamp collecting'),
	   (103456987, 'golf'),
	   (333453243, 'woodwork'), (333453243, 'coin collecting'),
	   (443453242, 'volleyball'), (443453242, 'painting'),
	   (145783475, 'tennis'), (145783475, 'golf'), (145783475, 'piano'), 
	   (758393228, 'sewing'), (758393228, 'painting'), (758393228, 'guitar');
	   
INSERT INTO OtherLogin(staffID, staff_type)
VALUES (1, 'entry level'), (2, 'upper level'), 
	   (3, 'specialist');