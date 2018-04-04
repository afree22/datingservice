
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

        # remember to test for duplicates????

        # test if interest already exists
        test_sql = "SELECT * FROM interests WHERE interest = %s"
        test_result = cur.execute(test_sql, (interest_cat))

        if not test_result:
            new_interest_sql = "INSERT INTO interests (interest) VALUES (%s)"
            new_interest_result = cur.execute(new_interest_sql, (interest_cat))
            new_type_sql = "INSERT INTO categories (category) VALUES (%s)"
            new_type_result = cur.execute(new_type_sql, (interest_type))

        # just a new type

    def add_interest(self, interest):
        sql = "INSERT INTO Interests (interest) VALUES (%s)"
        result = cur.execute(sql, (interest))
        return result

    def add_interest_type(self, interest_type):
        sql = "INSERT INTO Categories (category) VALUES (%s)"
        result = cur.execute(sql, (interest_type))
        return result

    def add_client_interest(self, ssn, interest_cat, interest_type=None):
        sql = "INSERT INTO client_interests (ssn, interest) VALUES (%s, %s)"
        result = cur.execute(sql, (ssn, interest_cat))
        return result

    def check_interest(self, interest):
        sql = "SELECT * FROM interests WHERE interest = %s"
        result = cur.execute(sql, (interest))
        # todo check how this works with error handling
        return result

    def check_interest_type(self, interest_type):
        sql = "SELECT * FROM types WHERE type = %s"
        result = cur.execute(sql, (interest_type))
        # todo check how this works with error handling
        return result

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
    
    """ This isn't finished yet"""
    def login_client(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        return 'SELECT COUNT(ssn) FROM ds.CLient WHERE ssn LIKE "%s";'.format(ssn)


    """ NEED TO FINISH LOG IN STUFF """ 
    def login_other(self, username, password, use_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        return ('SELECT ssn FROM ds.Client WHERE ssn IN (SELECT ssn from ds.CLient WHERE ssn LIKE "%s");'.format(ssn))
    
    

    def fetch_allClients(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM ds.Client;')
        return CursorIterator(cur)
    
    def fetch_potential_match(self, ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, crime):
        """Fetch matches from database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM ds.Client AS clients INNER JOIN CriminalRecord ON clients.ssn = CriminalRecord.ssn WHERE clients.ssn LIKE "%s" OR clients.name LIKE "%s" OR clients.gender LIKE "%s" OR  clients.dob LIKE "%s" OR clients.phone LIKE "%s" OR clients.eyecolor LIKE "%s" OR clients.weight LIKE "%s" OR clients.height LIKE "%s" OR clients.prior_marriage LIKE "%s" OR clients.interest LIKE "%s" OR clients.date_open LIKE "%s" OR clients.date_close LIKE "%s" OR clients.status LIKE "%s" OR CriminalRecord.crime LIKE "%s";'.format(ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, crime))
        """cur.execute('SELECT * FROM ds.Client AS clients, CriminalRecord as crimeRec, WHERE clients.ssn = CriminalRecord.ssn AND clients.ssn LIKE "%%{0}%%" AND clients.name LIKE "%%{1}%%" AND clients.gender LIKE "%%{2}%%" AND  clients.dob LIKE "%%{3}%%" AND clients.phone LIKE "%%{4}%%" AND clients.eyecolor LIKE "%%{5}%%" AND clients.weight LIKE "%%{6}%%" AND clients.height LIKE "%%{7}%%" AND clients.prior_marriage LIKE "%%{8}%%" AND clients.interest LIKE "%%{9}%%" AND clients.date_open LIKE "%%{10}%%" AND clients.date_close LIKE "%%{11}%%" AND clients.status LIKE "%%{12}%%" AND crimeRec.crime LIKE "%%{13}"";'.format(ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status,crime))"""
        return CursorIterator(cur)
