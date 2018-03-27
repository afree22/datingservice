# original author: Luca Soldaini

import pymysql


class CursorIterator(object):
    """Iterator for the cursor object."""

    def __init__(self, cursor):
        """ Instantiate a cursor object"""
        self.__cursor = cursor

    def __iter__(self):
        elem = self.__cursor.fetchone()
        while elem:
            yield elem
            elem = self.__cursor.fetchone()
        self.__cursor.close()


class Database(object):
    """Database object"""

    def __init__(self, opts):
        """Initalize database object"""
        super(Database, self).__init__()
        self.opts = opts
        self.__connect()

    def __connect(self):
        """Connect to the database"""
        self.conn = pymysql.connect(self.opts.DB_HOST, self.opts.DB_USER,
                                    self.opts.DB_PASSWORD, self.opts.DB_NAME)

    def insert_person_(self, ssn, name, gender, DOB, phone, eye_color, weight,
        height, prior_marriage, interest_in, date_open, date_close, status, child_name, child_DOB, child_status):
        """Search for a venue in the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        # also insert into children and interest tables probably

        # multiple children????

        sql = 'INSERT INTO Client (ssn, name, gender, DOB, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())'
        result = cur.execute(sql, (ssn, name, gender, DOB, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status))
        sql2 = 'INSERT INTO children (pssn, name, dob, status) VALUES (%s,%s,%s,%s, NOW())'
        result2 = cur.execute(sql, (ssn, child_name, child_DOB, child_status))

        return result and result2

    def insert_person(self, firstname, lastname, phone, age):
        """Search for a venue in the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO People (first_name, last_name, phone, age, time_added) VALUES (%s, %s, %s, %s, NOW())'
        result = cur.execute(sql, (firstname, lastname, phone, age))
        return result

    def get_people(self):
        """Fetch a veuw from the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT name FROM Client;')

        return CursorIterator(cur)


    def get_interests(self):
        """Get comments for a venue"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT id, name FROM Interests ORDER BY sort_order;')

        return CursorIterator(cur)
