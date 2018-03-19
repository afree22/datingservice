DROP DATABASE IF EXISTS project280;
CREATE DATABASE project280;
USE project280;
GRANT ALL ON project280.* TO user280@localhost IDENTIFIED BY 'p4ssw0rd';

CREATE TABLE Venues (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(120) NOT NULL,
    type VARCHAR(30) NOT NULL,
    phone CHAR(11) NOT NULL,
    address VARCHAR(255) NOT NULL,
    lat FLOAT(10, 6) NOT NULL,
    lng FLOAT(10, 6) NOT NULL,
    pic_id CHAR(21) DEFAULT '',
    has_reservations ENUM('Yes', 'No', 'Unknown') NOT NULL,
    has_credit_card ENUM('Yes', 'No', 'Unknown') NOT NULL,
    has_wheelchair ENUM('Yes', 'No', 'Unknown') NOT NULL,
    has_wifi ENUM('Free', 'Paid', 'No', 'Unknown') NOT NULL,
    has_kids ENUM('Yes', 'No', 'Unknown') NOT NULL
);

CREATE TABLE Users(
    id INT PRIMARY KEY NOT NULL,
    username VARCHAR(60) NOT NULL,
    first_name VARCHAR (60) DEFAULT '',
    last_name VARCHAR (60) DEFAULT '',
    city VARCHAR (30) DEFAULT ''
);

CREATE TABLE Comments(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    venue_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    CONSTRAINT exists_venue
        FOREIGN KEY (venue_id)
        REFERENCES Venues(id)
        ON DELETE CASCADE,
    CONSTRAINT exists_user
        FOREIGN KEY (user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
);


INSERT INTO Venues(name, type, phone,
                   address, lat, lng,
                   pic_id,
                   has_reservations, has_credit_card, has_wheelchair, has_wifi, has_kids)
VALUES ('2 Amys Neapolitan Pizzeria', 'Pizzeria', '2028855700',
        '3715 Macomb St NW Washington, DC 20016', 38.933705, -77.073078,
        'c4ca4238',
        'No', 'Yes', 'Yes', 'No', 'Yes');
INSERT INTO Venues(name, type, phone,
                   address, lat, lng,
                   pic_id,
                   has_reservations, has_credit_card, has_wheelchair, has_wifi, has_kids)
VALUES ('The Bier Baron Tavern', 'Bar', '2022931887',
        '1523 22nd St NW Washington, DC 20037', 38.910313, -77.048455,
        'c81e728d',
        'No', 'Yes', 'Yes', 'No', 'No');
INSERT INTO Venues(name, type, phone,
                   address, lat, lng,
                   pic_id,
                   has_reservations, has_credit_card, has_wheelchair, has_wifi, has_kids)
VALUES ('Tryst', 'Coffee shop', '2022325500',
        '2459 18th St NW Washington, DC 20009', 38.921977, -77.042091,
        'eccbc87e',
        'No', 'Yes', 'Yes', 'Free', 'Yes');
INSERT INTO Venues(name, type, phone,
                   address, lat, lng,
                   pic_id,
                   has_reservations, has_credit_card, has_wheelchair, has_wifi, has_kids)
VALUES ('Pho 75', 'Vietnamese restaurant', '7035257355',
        '1721 Wilson Blvd Arlington, VA 22209', 38.894000, -77.078477,
        'cfcd2084',
        'No', 'No', 'Yes', 'No', 'Yes');
INSERT INTO Venues(name, type, phone,
                   address, lat, lng,
                   pic_id,
                   has_reservations, has_credit_card, has_wheelchair, has_wifi, has_kids)
VALUES ('Farmers Fishers Bakers', 'American restaurant', '2022988783',
        '3000 K St NW Washington, DC 20007', 38.901287, -77.059815,
        'a87ff679',
        'Yes', 'Yes', 'Yes', 'Free', 'Yes');

INSERT INTO Users(id, username, first_name, last_name, city)
VALUES(220213,
       'jd93',
       'John',
       'Doe',
       'Washington, D.C.');
INSERT INTO Users(id, username, first_name)
VALUES(93181,
       'mmjane',
       'Jane');

INSERT INTO Comments(venue_id, user_id, rating, comment)
VALUES(1, 220213, 4, "3.5 stars for me but I'd give them 4 stars if I was married with children! we just had a great dinner at 2 amys. We didn't expect the vibe of the place to be all screaming children and loud big families, so just to give you a heads up... that's what it is :) there is a sizable dining area with a bar area off to the side and a patio out back... very informal setting and probably not the best for a romantic date but more of a casual dinner on a low key night.");
INSERT INTO Comments(venue_id, user_id, rating, comment)
VALUES(4, 220213, 5, "Have a head cold? Get pho. Having a bad day? Get pho. Just need something good in your tummy? Get pho. Need the best pho in the area? Come here.");
INSERT INTO Comments(venue_id, user_id, rating, comment)
VALUES(4, 93181, 5, "Pho 75 is amazing! I could smell the pho from the parking lot! I usually get the pho with uncooked eye of round. The meat and broth had a lot of flavor and the noodles were really good. This place was packed! Seating took about 15 minutes but once we ordered, our food came out within minutes. ");
