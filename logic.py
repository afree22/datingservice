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
        self.con.commit()
        return result

    def add_interest_type(self, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO Categories (category) VALUES (%s)"
        result = cur.execute(sql, (interest_type))
        self.con.commit()
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

    def get_dates(self, user_ssn, date_ssn, date_date):
        """ Display dates for a user
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # i think this works, only want to get the name of the people who
        # aren't the current user
        # sql = 'SELECT * FROM client, dates where (ssn = c1_ssn or ssn = c2_ssn) and ssn != %s'
        # dates = cur.execute(sql, (user_ssn))

        # sql = "SELECT * FROM dates WHERE scheduled_date = '%s' AND ((c1_ssn = %s AND c2_ssn = %s) OR (c1_ssn = %s AND c2_ssn = %s))"
        sql = "SELECT * FROM dates WHERE scheduled_date = '{}' AND (c1_ssn = {} AND c2_ssn = {}) OR (c1_ssn = {} AND c2_ssn = {})".format(date_date, user_ssn, date_ssn, date_ssn, user_ssn)
        # result = cur.execute(
        #     sql, (date_date, user_ssn, date_ssn, date_ssn, user_ssn))
        result = cur.execute(sql)
        return CursorIterator(cur)

    def get_prev_dates(self, user_ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # i think this works, only want to get the name of the people who
        # aren't the current user
        sql = 'SELECT * FROM client, dates where (ssn = c1_ssn OR ssn = c2_ssn) and ssn != %s AND occured IS NOT NULL'
        dates = cur.execute(sql, (user_ssn))
        return CursorIterator(cur)

    def get_future_dates(self, user_ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # i think this works, only want to get the name of the people who
        # aren't the current user
        sql = 'SELECT * FROM client, dates where (ssn = c1_ssn OR ssn = c2_ssn) and ssn != %s AND occured IS NULL'
        dates = cur.execute(sql, (user_ssn))
        return CursorIterator(cur)

    def set_date_occurred(self, c1_ssn, c2_ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        # todo double check schema for dates!!!
        # tod make this take an actual date as well
        sql = 'UPDATE dates set occured = "yes" WHERE (c1_ssn = %s AND c2_ssn = %s) OR (c1_ssn = %s AND c2_ssn = %s)'
        result = cur.execute(sql, (c1_ssn, c2_ssn, c2_ssn, c1_ssn))
        self.conn.commit()
        
        return result

    def set_see_again(self, c1_ssn, c2_ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE dates set see_again = "yes" WHERE (c1_ssn = %s AND c2_ssn = %s) OR (c1_ssn = %s AND c2_ssn = %s)'
        result = cur.execute(sql, (c1_ssn, c2_ssn, c2_ssn, c1_ssn))
        self.conn.commit()

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
    
    def login_staff(self, username, password):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
    
    def login_specialist(self, username, password):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
    

    """ Specialist Insert Client """
    def insert_client(self, ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Client (ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status))
        self.conn.commit()
        return result
    
    def insert_crime(self, ssn, crime):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO CriminalRecord (ssn, crime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, crime))
        self.conn.commit()
        return result
    
    """ Specialist Update Client """
    def modify_client(self, ssn, ssn_new, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, crime, childName, childDOB, childStatus):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        update = "UPDATE client set "
        rightClient = " WHERE ssn = '{}'".format(ssn)
        client_attrs = []
        
        if ssn_new:
            client_attrs.append("ssn = '{}'".format(ssn_new))
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
        if childName:
            client_attrs.append("childName = '{}'".format(childName))
        if childDOB:
            client_attrs.append("childDOB = '{}'".format(childDOB))
        if childStatus:
            client_attrs.append("childStatus = '{}'".format(childStatus))
        
        attrs = " , ".join(client_attrs)
        sql = "{}{}{}".format(update, attrs, rightClient)
        print(sql)
                    
        cur.execute(sql)
        return CursorIterator(cur)
            
            
    """ Specialist Delete Client """
    def delete_client(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE c, cr, ch FROM Client C LEFT JOIN CriminalRecord cr ON c.ssn = cr.ssn LEFT JOIN Children ch ON c.ssn = ch.ssn"
        cur.execute(sql,(ssn))
        
    """ Specialist Queries """
    def get_num_clients_married(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT COUNT(*) as married FROM CLIENT C WHERE prior_marriage = 'yes'"
        cur.execute(sql)
        return CursorIterator(cur)
    
    def get_num_clients_gender(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT COUNT(*) as num FROM CLIENT C group by gender"
        cur.execute(sql)
        return CursorIterator(cur)

    
    """ Specialist Search for Client """
    def fetch_allClients(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn LEFT JOIN Children ON c.ssn = Children.ssn")
        return CursorIterator(cur)
    
    def fetch_potential_match(self, ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, crime, childName, childDOB, childStatus):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn  LEFT JOIN Children ON c.ssn = Children.ssn WHERE "
        client_attrs = []

        if ssn:
            client_attrs.append("ssn = '{}'".format(ssn))
        if name:
            client_attrs.append("name = '{}'".format(name))
        if gender:
            client_attrs.append("gender = '{}'".format(gender))
        if dob:
            client_attrs.append("dob = '{}'".format(dob))
        if phone:
            client_attrs.append("phone = '{}'".format(phone))
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
        if childName:
            client_attrs.append("childName = '{}'".format(childName))
        if childDOB:
            client_attrs.append("childDOB = '{}'".format(childDOB))
        if childStatus:
            client_attrs.append("childStatus = '{}'".format(childStatus))


        
        # todo look into or querying
        attrs = " AND ".join(client_attrs)
        sql = "{}{}".format(select, attrs)
        print(sql)
        
        cur.execute(sql)
        return CursorIterator(cur)


        


    """ Staff Search for Client """
    def fetch_staffClients(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn  LEFT JOIN Children ON c.ssn = Children.ssn;")
        return CursorIterator(cur)
    
    def fetch_staff_match(self, name, gender, dob, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, crime, childName, childDOB, childStatus):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn  LEFT JOIN Children ON c.ssn = Children.ssn WHERE "
        client_attrs = []
        
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
        if childName:
            client_attrs.append("childName = '{}'".format(childName))
        if childDOB:
            client_attrs.append("childDOB = '{}'".format(childDOB))
        if childStatus:
            client_attrs.append("childStatus = '{}'".format(childStatus))

        
        # todo look into or querying
        attrs = " AND ".join(client_attrs)
        sql = "{}{}".format(select, attrs)
        print(sql)
        
        cur.execute(sql)
        return CursorIterator(cur)
