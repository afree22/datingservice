
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

        # need this to keep changes between local and other
        self.conn.commit()

        return result

    def get_client_matches(self, gender, age, eye_color, weight, height, prev_marriage, interest_cat, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT DISTINCT name, c.ssn FROM client c, client_interests i WHERE c.ssn = i.ssn AND "
        client_attrs = []
        if gender:
            client_attrs.append("gender = '{}'".format(gender))
        if age:
            # todo deal with age
            pass
        if eye_color:
            client_attrs.append("eyecolor = '{}'".format(eye_color))
        if weight:
            client_attrs.append("weight = {}".format(weight))
        if height:
            client_attrs.append("height = {}".format(height))
        if prev_marriage:
            client_attrs.append("prior_marriage = '{}'".format(prev_marriage))
        if interest_cat:
            client_attrs.append("interest = '{}'".format(interest_cat))
        # todo remember interest_type

        # todo look into or querying
        attrs = " AND ".join(client_attrs)
        sql = "{}{}".format(select, attrs)
        print(sql)

        cur.execute(sql)
        return CursorIterator(cur)

    def insert_date(self, user_ssn, date_ssn, location, date):

        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO dates (c1_ssn, c2_ssn, location, scheduled_date, occured, interested, see_again) VALUES (%s, %s, %s, %s, NULL, NULL, NULL)"
        result = cur.execute(
            sql, (int(user_ssn), int(date_ssn), location, date))

        self.conn.commit()
        return result

    def add_interest(self, interest):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO Interests (interest) VALUES (%s)"
        result = cur.execute(sql, (interest))
        return result

    def add_interest_type(self, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO Categories (category) VALUES (%s)"
        result = cur.execute(sql, (interest_type))
        return result

    def add_client_interest(self, ssn, interest_cat, interest_type=None):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO client_interests (ssn, interest) VALUES (%s, %s)"
        result = cur.execute(sql, (ssn, interest_cat))
        return result

    def check_interest(self, interest):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM interests WHERE interest = %s"
        result = cur.execute(sql, (interest))
        # todo check how this works with error handling
        return result

    def check_interest_type(self, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
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

    def get_dates(self, user_ssn):
        """ Display dates for a user
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM dates WHERE c1_ssn = %s OR c2_ss = %s'
        dates = cur.execute(sql, (user_ssn, user_ssn))
        return CursorIterator(curr)

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
    
    def login_staff(self, username, password):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
    
    def login_specialist(self, username, password):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
    

    
    

    def fetch_allClients(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM ds.Client;')
        return CursorIterator(cur)
    
    def fetch_potential_match(self, ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, crime):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT c.ssn, name, gender, dob, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn WHERE "
        client_attrs = []

        if ssn:
            client_attrs.append(ssn = "{}".format(ssn))
        if name:
            client_attrs.append("name = '{}'".format(name))
        if gender:
            client_attrs.append("gender = '{}'".format(gender))
        if dob:
            client_attrs.append("dob = '{}'".format(dob))
        if eyecolor:
            client_attrs.append("eyecolor = '{}'".format(eyecolor))
        if weight:
            client_attrs.append("weight = {}".format(weight))
        if height:
            client_attrs.append("height = {}".format(height))
        if prior_marriage:
            client_attrs.append("prior_marriage = '{}'".format(prior_marriage))
        if interest:
            client_attrs.append("interest = '{}'".format(interest))
        if date_open:
            client_attrs.append("date_open = '{}'".format(date_open))
        if date_close:
            client_attrs.append("date_close = '{}'".format(date_close))
        if status:
            client_attrs.append("status = '{}'".format(status))
        if crime:
            client_attrs.append("crime = '{}'".format(crime))
        
        # todo look into or querying
        attrs = " AND ".join(client_attrs)
        sql = "{}{}".format(select, attrs)
        print(sql)
        
        cur.execute(sql)
        return CursorIterator(cur)
