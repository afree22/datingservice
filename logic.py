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
        height, prior_marriage, interest_in, date_open, date_close, status, interest_cat=None, interest_specific=None):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        # also insert into children and interest tables probably
        # check if user already signed up, don't insert if so
        sql = 'INSERT INTO Client (ssn, name, gender, DOB, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, gender, DOB, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status))

        # sql2 = "SHOW TABLES LIKE 'cooking'"
        # result2 = cur.execute(sql2)
        # print(result2)

        # do interests
        # can we have them sign up with just one interest and then edit in more later?
        # another view/function like with children

        # need this to keep changes between local and other
        self.conn.commit()

        return result

    def add_interests(self, ssn, interest_cat, interest_type):

        # test if interest table already exists
        test_sql = "SHOW TABLES LIKE '%s'"
        test_result = cur.execute(test_sql, (interest_cat))

        if not test_result:
            # should these have pks?
            new_interest_sql = "CREATE TABLE %s (type varchar(120))"
            new_interest_result = cur.execute(new_interest_sql, (interest_cat))

            # todo: verify this
            if not new_interest_result:
                return new_interest_result

        interest_sql = "INSERT INTO %s (ssn, interest, category) VALUES (%s, %s, %s)"
        interest_result = cur.execute(interest_sql, (ssn, interest_cat, interest_type))

        # todo: verify what to return here
        return interest_result


    def insert_child_(self, ssn, name, dob, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Children (ssn, childName, childDOB, childStatus) VALUES (%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, dob, status))
        self.conn.commit()

        return result

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

    def get_specialists(self):
        # is maintaining specialist info in schema?
        # no but maybe can tell from who has what permissions
        pass


    def get_interests(self):
        """Get comments for a venue"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT id, name FROM Interests ORDER BY sort_order;')

        return CursorIterator(cur)
