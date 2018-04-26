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
        sql = 'INSERT INTO Client (ssn, name, gender, DOB, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, gender, DOB, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status))
        # need this to keep changes between local and other
        self.conn.commit()
        return result
    
    def specialist_insert_person(self, ssn, name, gender, dob, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Client (ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, gender, dob, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status))
        self.conn.commit()
        return result

    def get_client_matches(self, gender, age, eye_color, weight, height, prev_marriage, interest_cat, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT DISTINCT name, c.ssn FROM client c left join client_interests i on c.ssn = i.ssn WHERE "
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
        sql = "{}{} AND status = 'active'".format(select, attrs)
        print(sql)

        cur.execute(sql)
        return CursorIterator(cur)

    def insert_date(self, user_ssn, date_ssn, location, date):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO dates (c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again) VALUES (%s, %s, %s, %s, NULL, NULL, NULL)"
        result = cur.execute(
            sql, (int(user_ssn), int(date_ssn), location, date))

        self.conn.commit()
        return result
    
    def add_interest(self, ssn, interest):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO client_interests (ssn, interest) VALUES (%s, %s)"
        result = cur.execute(sql,(ssn, interest))
        self.conn.commit()
        return result
    
    def check_interest_exists(self, interest, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT COUNT(interest) as c FROM interest_category WHERE interest = %s"
        cur.execute(sql, (interest))
        d = list(CursorIterator(cur))[0]
        return [ d[k] for k in d][0] == 1
    
    def add_interest_type(self, interest, interest_type):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO interest_category (interest, category) VALUES (%s, %s)"
        result = cur.execute(sql, (interest, interest_type))
        self.conn.commit()
        return result
    
    
    """
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
        return result"""

    def add_client_interest(self, ssn, interest_cat, interest_type=None):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO client_interests (ssn, interest) VALUES (%s, %s)"
        result = cur.execute(sql, (ssn, interest_cat))
        return result
    
    def delete_interest(self, ssn, interest):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM client_interests WHERE ssn = %s AND interest = %s"
        result = cur.execute(sql, (ssn, interest))
        self.conn.commit()
        return result
    """
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
        return result"""

    def insert_child_(self, ssn, name, dob, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Children (ssn, childName, childDOB, childStatus) VALUES (%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, dob, status))
        self.conn.commit()
        return result
    
    def delete_child(self, ssn, name):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM children WHERE ssn = %s AND childName = %s"
        result = cur.execute(sql, (ssn, name))
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

        print(user_ssn, date_ssn, date_date)

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
        # sql = 'select * from client, dates where (client.ssn = dates.ssn or client.ssn = dates.date_ssn) and client.ssn = %s and occurred is not null'

        sql = 'select * from dates where (c1_ssn = %s OR c2_ssn = %s) and occurred is not null'
        dates = cur.execute(sql, (user_ssn, user_ssn))
        return CursorIterator(cur)

    def get_future_dates(self, user_ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # i think this works, only want to get the name of the people who
        # aren't the current user
        # sql = 'SELECT * FROM client, dates where (client.ssn = dates.ssn OR client.ssn = dates.date_ssn) and client.ssn != %s AND occurred IS NULL'
        # sql = 'SELECT * FROM client, dates where (client.ssn = dates.ssn OR client.ssn = dates.date_ssn) and client.ssn != %s AND occurred IS NULL'


        sql = 'select * from dates where (c1_ssn = %s OR c2_ssn = %s) and occurred is null'
        dates = cur.execute(sql, (user_ssn, user_ssn))
        return CursorIterator(cur)

    def set_date_occurred(self, ssn, date_ssn, date):
        print(date, ssn, date_ssn)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "UPDATE dates set occurred = 'yes' WHERE ((c1_ssn = %s AND c2_ssn = %s) OR (c1_ssn = %s AND c2_ssn = %s)) AND scheduled_date = %s"
        print(ssn, date_ssn, date_ssn, ssn, date)
        result = cur.execute(sql, (ssn, date_ssn, date_ssn, ssn, date))
        self.conn.commit()
        
        return result

    def set_see_again(self, ssn1, ssn2, date_date, value):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "UPDATE dates set see_again = %s WHERE ((c1_ssn = %s and c2_ssn = %s) OR (c1_ssn = %s and c2_ssn = %s)) AND scheduled_date = %s"
        result = cur.execute(sql, (value, ssn1, ssn2, ssn2, ssn1, date_date))
        self.conn.commit()

        return result

    def get_dates_per_couple(self, ssn1, ssn2):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * from dates where (c1_ssn = %s and c2_ssn = %s) or (c1_ssn = %s and c2_ssn = %s)'
        result = cur.execute(sql, (ssn1, ssn2, ssn2, ssn1))
        return CursorIterator(cur)

    def update_date(self, ssn, date_ssn, orig_date, new_date, new_location):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        result1 = 1
        result2 = 1

        if new_date:
            sql = 'UPDATE dates set scheduled_date = %s WHERE scheduled_date = %s AND ((c1_ssn = %s AND c2_ssn = %s) OR (c1_ssn = %s AND c2_ssn = %s))'
            result1 = cur.execute(sql, (new_date, orig_date, ssn, date_ssn, date_ssn, ssn))
        if new_location:
            sql = 'UPDATE dates set location = %s WHERE ((c1_ssn = %s AND c2_ssn = %s) OR (c1_ssn = %s AND c2_ssn = %s)) AND scheduled_date = %s'
            result2 = cur.execute(sql, (new_location, ssn, date_ssn, date_ssn, ssn, orig_date))
        self.conn.commit()

        return result1 and result2

    def get_interested_dates(self, ssn):
        """ Get the dates for the user that the user wants to see again
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from dates where (c1_ssn = %s or c2_ssn = %s) and see_again = 'yes'"
        dates = cur.execute(sql, (ssn, ssn))
        return CursorIterator(cur)

    def get_most_recent_date(self, ssn, date_ssn):
        """ get the most recent date for any two users
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM dates WHERE ssn = %s AND date_ssn = %s ORDER BY scheduled_date LIMIT 1'
        date = cur.execute(sql, (ssn, date_ssn))
        return CursorIterator(cur)

    def get_date_count(self, ssn1, ssn2):
        """Get # of dates couple has successfully completed"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT COUNT(*) FROM dates where (c1_ssn = %s and c2_ssn = %s) or (c1_ssn = %s and c2_ssn = %s) and see_again = 'yes'"
        cur.execute(sql, (ssn1, ssn2, ssn2, ssn1))
        return CursorIterator(cur)

    def get_client_dates(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM dates where c1_ssn = %s or c2_ssn = %s"
        cur.execute(sql, (ssn, ssn))
        return CursorIterator(cur)

    def get_other_interested(self, ssn, date_date):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from dates where ssn = %s and scheduled_date = %s"
        response = cur.execute(sql, (ssn, date_date))
        return CursorIterator(cur)

    def get_client_by_ssn(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM client where ssn = %s'
        cur.execute(sql, (ssn))
        return CursorIterator(cur)

    def get_payments(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM fees where ssn = %s'
        cur.execute(sql, (ssn))
        return CursorIterator(cur)

    def charge_registration_fee(self, ssn):
        """ charge registration fee
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO fees (ssn, date_incurred, fee_type, payment_amount, fee_status) VALUES (%s, NOW(), 'registration fee', 100, 'unpaid')"
        result = cur.execute(sql, (ssn))
        self.conn.commit()
        return result

    def charge_match_fee(self, ssn):
        """ charge a match fee
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # sql = "INSERT INTO fees (ssn, date_incurred, fee_type, payment_amount, fee_status) VALUES (%s, NOW(), 'match fee', 50, 'overdue')"
        sql = "INSERT INTO fees (ssn, date_incurred, fee_type, payment_amount, fee_status) VALUES (%s, NOW(), 'match fee', 50, 'unpaid')"
        result = cur.execute(sql, (ssn))
        self.conn.commit()
        return result

    def get_five_recent_matches(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # sql = "SELECT * FROM dates WHERE (c1_ssn = %s or c2_ssn = %s) and occurred = 'yes' ORDER BY scheduled_date"
        sql = "select distinct c1_ssn, c2_ssn from dates where c1_ssn = %s or c2_ssn = %s"
        cur.execute(sql, (ssn, ssn))
        return CursorIterator(cur)

    def pay_fee(self, ssn, date_incurred):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "update fees set fee_status = 'paid' where ssn = %s and date_incurred = %s"
        result = cur.execute(sql, (ssn, date_incurred))
        return result

    def insert_credit(self, ssn, value):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        # sql = "INSERT INTO credit (ssn, amount) VALUES (%s, %s)"
        sql = "UPDATE credit SET amount = amount + %s WHERE ssn = %s"
        result = cur.execute(sql, (value, ssn))
        self.conn.commit()
        return result

    def get_credit(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT amount FROM credit WHERE ssn = %s"
        cur.execute(sql, (ssn))
        return CursorIterator(cur)

    def make_credit_entry(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO credit (ssn, amount) VALUES (%s, 100)"
        result = cur.execute(sql, (ssn))
        return result

    def outstanding_payment(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM fees WHERE fee_status = 'unpaid' AND ssn = %s"
        cur.execute(sql, (ssn))
        return CursorIterator(cur)

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
        result = cur.execute('SELECT COUNT(ssn) FROM ds.CLient WHERE ssn LIKE "%s";'.format(ssn))
        self.conn.commit()
        return result
    
    
    def entry_login(self, staffID):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute( 'SELECT COUNT(staffID) as c FROM ds.OtherLogin WHERE staffID = %s AND staff_type = "entry level";', (staffID))
        d = list(CursorIterator(cur))[0]
        return [ d[k] for k in d][0] == 1

    def upper_login(self, staffID):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute( 'SELECT COUNT(staffID) as c FROM ds.OtherLogin WHERE staffID = %s AND staff_type = "upper level";', (staffID))
        d = list(CursorIterator(cur))[0]
        return [ d[k] for k in d][0] == 1
    
    def specialist_login(self, staffID):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute( 'SELECT COUNT(staffID) as c FROM ds.OtherLogin WHERE staffID = %s AND staff_type = "specialist";', (staffID))
        d = list(CursorIterator(cur))[0]
        return [ d[k] for k in d][0] == 1
    

    """ Specialist Insert Client """
    def insert_client(self, ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Client (ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status))
        self.conn.commit()
        return result
    
    def insert_crime(self, ssn, crime):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO CriminalRecord (ssn, crime) VALUES (%s,%s)'
        result = cur.execute(sql, (ssn, crime))
        self.conn.commit()
        return result
    
    def delete_crime(self, ssn, crime):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM criminalrecord WHERE ssn = %s AND crime = %s"
        result = cur.execute(sql, (ssn,crime))
        self.conn.commit()
        return result
    
    
    
    def change_client_status(self,ssn,date_close,status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "UPDATE CLIENT set status = %s, date_close = %s WHERE ssn = %s"
        result = cur.execute(sql, (status, date_close, ssn))
        return result
    
    def client_no_crimes(self,ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT COUNT(ssn) as c FROM criminalRecord WHERE ssn =%s"
        cur.execute(sql, (ssn))
        d = list(CursorIterator(cur))[0]
        return [ d[k] for k in d][0] == 0
    
        
    
    """ Specialist Update Client """
    def modify_client(self, ssn, ssn_new, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        update = "UPDATE client set "
        rightClient = " WHERE ssn = '{}'".format(ssn)
        client_attrs = []
        
        if ssn_new:
            client_attrs.append("ssn = '{}'".format(ssn_new))
        if name:
            client_attrs.append("name = '{}'".format(self.conn.escape_string(name)))
            """ Do with all .format string """ 
        if gender:
            client_attrs.append("gender = '{}'".format(self.conn.escape_string(gender)))
        if dob:
            client_attrs.append("dob = '{}'".format(dob))
        if eyecolor:
            client_attrs.append("eyecolor = '{}'".format(self.conn.escape_string(eyecolor)))
        if weight:
            client_attrs.append("weight = {}".format(weight))
        if height:
            client_attrs.append("height = {}".format(height))
        if prior_marriage:
            client_attrs.append("prior_marriage = '{}'".format(self.conn.escape_string(prior_marriage)))
        if interest_in:
            client_attrs.append("interest_in = '{}'".format(self.conn.escape_string(interest_in)))
        if date_open:
            client_attrs.append("date_open = '{}'".format(date_open))
        if date_close:
            client_attrs.append("date_close = '{}'".format(date_close))
        if status:
            client_attrs.append("status = '{}'".format(self.conn.escape_string(status)))
        
        attrs = " , ".join(client_attrs)
        sql = "{}{}{}".format(update, attrs, rightClient)
        print(sql)
                    
        cur.execute(sql)
        
        self.conn.commit()
        return CursorIterator(cur)

    def update_specialist_child(self, ssn, name, new_name, dob, status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        update = "UPDATE children set "
        rightClient = " WHERE ssn = '{}' AND childName = '{}'".format(ssn, name)
        client_attrs = []
        if new_name:
            client_attrs.append("childName = '{}'".format(self.conn.escape_string(new_name)))
        if dob:
            client_attrs.append("childDOB = '{}'".format(dob))
        if status:
            client_attrs.append("childStatus = '{}'".format(self.conn.escape_string(status)))
        attrs = " , ".join(client_attrs)
        sql = "{}{}{}".format(update, attrs, rightClient)
        cur.execute(sql)
        self.conn.commit()
        return CursorIterator(cur)

    def update_specialist_fees(self, ssn, date_incurred, new_date_incurred, new_feetype, new_payment_amount, new_fee_status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        update = "UPDATE Fees set "
        rightFee = " WHERE ssn = '{}' AND date_incurred = '{}'".format(ssn, date_incurred)
        client_attrs = []
        if new_date_incurred:
            client_attrs.append("date_incurred = '{}'".format(new_date_incurred))
        if new_feetype:
            client_attrs.append("fee_type = '{}'".format(new_feetype))
        if new_payment_amount:
            client_attrs.append("payment_amount = '{}'".format(new_payment_amount))
        if new_fee_status:
            client_attrs.append("fee_status = '{}'".format(self.conn.escape_string(new_fee_status)))
        attrs = " , ".join(client_attrs)
        sql = "{}{}{}".format(update, attrs, rightFee)
        cur.execute(sql)
        self.conn.commit()
        return CursorIterator(cur)

    def update_specialist_dates(self, c1_ssn, c2_ssn, scheduled_date, updated_date, updated_scheduled_date, location, occurred, interested, see_again):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        update = "UPDATE dates set "
        rightDate = " WHERE c1_ssn = '{}' AND c2_ssn = '{}' OR c1_ssn = '{}' AND c2_ssn = '{}' AND scheduled_date = '{}'".format(c1_ssn, c2_ssn, c2_ssn, c1_ssn, scheduled_date)
        client_attrs = []
        
        if updated_date:
            client_attrs.append("c1_ssn = '{}'".format(c1_ssn))
            client_attrs.append("c2_ssn = '{}'".format(updated_date))
        if updated_scheduled_date:
            client_attrs.append("scheduled_date = '{}'".format(updated_scheduled_date))
        if location:
            client_attrs.append("location = '{}'".format(self.conn.escape_string(location)))
        if occurred:
            client_attrs.append("occurred = '{}'".format(self.conn.escape_string(occurred)))
        if interested:
            client_attrs.append("interested = '{}'".format(self.conn.escape_string(interested)))
        if see_again:
            client_attrs.append("see_again = '{}'".format(self.conn.escape_string(see_again)))

        attrs = " , ".join(client_attrs)
        sql = "{}{}{}".format(update, attrs, rightDate)
        cur.execute(sql)
        self.conn.commit()
        return CursorIterator(cur)

    def insert_fees(self, ssn, date_incurred, fee_type, payment_amount, fee_status):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO FEES (ssn, date_incurred, fee_type, payment_amount, fee_status) VALUES (%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (ssn, date_incurred, fee_type, payment_amount, fee_status))
        self.conn.commit()
        return result
    
    def insert_dates(self, c1_ssn, c2_ssn, scheduled_date, location, occurred, interested, see_again):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO dates (c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql, (c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again))
        self.conn.commit()
        return result

    def delete_fees(self, ssn, date_incurred):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM Fees WHERE ssn = %s AND date_incurred = %s"
        result = cur.execute(sql, (ssn, date_incurred))
        self.conn.commit()
        return result
    
    def delete_dates(self, c1_ssn, c2_ssn, scheduled_date):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM dates WHERE c1_ssn = %s AND c2_ssn = %s OR c2_ssn = %s AND c1_ssn = %s AND scheduled_date = %s"
        result = cur.execute(sql, (c1_ssn, c2_ssn, c2_ssn, c1_ssn, scheduled_date))
        self.conn.commit()
        return result

            
    """ Specialist Delete Client """
    def delete_client(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM CLIENT WHERE ssn = %s"
        result = cur.execute(sql, (ssn))
        self.conn.commit()
        return result
        
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
    
    def get_type_crime(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT distinct crime as c from criminalRecord"
        cur.execute(sql)
        return CursorIterator(cur)
    
    def get_num_dates_gender(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT AVG(count) as c, g FROM ( SELECT COUNT(c.ssn) as count, gender as g FROM Client c Left Join Dates d on c.ssn = d.c1_ssn or c.ssn = d.c2_ssn group by g) as P group by g "
        cur.execute(sql)
        return CursorIterator(cur)
    
    def num_dates_exactly(self, number):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT c.ssn as s, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status FROM Client c Left Join Dates on c.ssn = dates.c1_ssn or c.ssn = dates.c2_ssn  group by c.ssn Having Count(c.ssn) = %s"
    
        cur.execute(sql, (number))
        return CursorIterator(cur)
    
    def num_dates_atMost(self, number):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        """ Assuming you want to include people who have had no dates """
        sql = "SELECT c.ssn as s, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status FROM Client c Left Join Dates on c.ssn = dates.c1_ssn OR c.ssn = dates.c2_ssn GROUP BY c.ssn Having Count(c.ssn) <= %s"
        cur.execute(sql, (number))
        return CursorIterator(cur)
    
    def num_dates_atLeast(self, number):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT c.ssn as s, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status FROM Client c Left Join Dates on c.ssn = dates.c1_ssn or c.ssn = dates.c2_ssn group by c.ssn Having Count(c.ssn) >= %s"
        cur.execute(sql, (number))
        return CursorIterator(cur)
    
    def get_age_children(self, currentDate):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT AVG(count) as c FROM ( select DATEDIFF(%s, childDOB)/365.25 as count From Children) as P"
        cur.execute(sql, (currentDate))
        return CursorIterator(cur)
    
    def get_outstanding_balance(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT ssn, sum(payment_amount) as p FROM Fees WHERE fee_status = 'unpaid' OR fee_status = 'overdue' GROUP BY ssn"
        cur.execute(sql)
        return CursorIterator(cur)
    
    def display_interests(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT distinct(interest) as i FROM Client c LEFT JOIN client_interests on c.ssn = client_interests.ssn WHERE c.status = 'active' AND interest != 'NULL';"
        cur.execute(sql)
        return CursorIterator(cur)
    
    def average_dates_couple(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT AVG (COUNT) as c FROM (SELECT c1_ssn, c2_ssn, COUNT(*) count FROM dates GROUP BY c1_ssn, c2_ssn) as P"
        cur.execute(sql)
        return CursorIterator(cur)

    
    """ Specialist Search for Client """
    def fetch_allClients(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus, interest_category.interest, interest_category.category, date_incurred, fee_type, payment_amount, fee_status, c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn LEFT JOIN Children ON c.ssn = Children.ssn LEFT JOIN client_interests ON c.ssn = client_interests.ssn LEFT JOIN interest_category on client_interests.interest = interest_category.interest LEFT JOIN FEES ON c.ssn = FEES.ssn LEFT JOIN Dates ON c.ssn = Dates.c1_ssn or c.ssn = Dates.c2_ssn")
        return CursorIterator(cur)
    
    def fetch_potential_match(self, ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, crime, childName, childDOB, childStatus, interest, category, date_incurred, fee_type, payment_amount, fee_status, location, scheduled_date, occurred, interested, see_again):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus, interest_category.interest, interest_category.category, date_incurred, fee_type, payment_amount, fee_status, c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn LEFT JOIN Children ON c.ssn = Children.ssn LEFT JOIN client_interests ON c.ssn = client_interests.ssn LEFT JOIN interest_category on client_interests.interest = interest_category.interest LEFT JOIN FEES ON c.ssn = FEES.ssn LEFT JOIN Dates ON c.ssn = Dates.c1_ssn or c.ssn = Dates.c2_ssn WHERE "
        client_attrs = []

        if ssn:
            client_attrs.append("ssn = '{}'".format(ssn))
        if name:
            client_attrs.append("name = '{}'".format(self.conn.escape_string(name)))
        if gender:
            client_attrs.append("gender = '{}'".format(self.conn.escape_string(gender)))
        if dob:
            client_attrs.append("dob = '{}'".format(dob))
        if phone:
            client_attrs.append("phone = '{}'".format(phone))
        if eyecolor:
            client_attrs.append("eyecolor = '{}'".format(self.conn.escape_string(eyecolor)))
        if weight:
            client_attrs.append("weight = {}".format(weight))
        if height:
            client_attrs.append("height = {}".format(height))
        if prior_marriage:
            client_attrs.append("prior_marriage = '{}'".format(self.conn.escape_string(prior_marriage)))
        if interest_in:
            client_attrs.append("interest_in = '{}'".format(self.conn.escape_string(interest_in)))
        if date_open:
            client_attrs.append("date_open = '{}'".format(date_open))
        if date_close:
            client_attrs.append("date_close = '{}'".format(date_close))
        if status:
            client_attrs.append("status = '{}'".format(self.conn.escape_string(status)))
        if crime:
            client_attrs.append("crime = '{}'".format(self.conn.escape_string(crime)))
        if childName:
            client_attrs.append("childName = '{}'".format(self.conn.escape_string(childName)))
        if childDOB:
            client_attrs.append("childDOB = '{}'".format(childDOB))
        if childStatus:
            client_attrs.append("childStatus = '{}'".format(self.conn.escape_string(childStatus)))
        if interest:
            client_attrs.append("interest = '{}'".format(self.conn.escape_string(interest)))
        if category:
            client_attrs.append("category = '{}'".format(self.conn.escape_string(category)))
        if date_incurred:
            client_attrs.append("date_incurred = '{}'".format(date_incurred))
        if fee_type:
            client_attrs.append("fee_type = '{}'".format(self.conn.escape_string(fee_type)))
        if payment_amount:
            client_attrs.append("paymen_amount = '{}'".format(payment_amount))
        if fee_status:
            client_attrs.append("fee_status = '{}'".format(self.conn.escape_string(fee_status)))
        if location:
            client_attrs.append("location = '{}'".format(self.conn.escape_string(location)))
        if scheduled_date:
            client_attrs.append("scheduled_date = '{}'".format(scheduled_date))
        if occurred:
            client_attrs.append("occurred = '{}'".format(self.conn.escape_string(occurred)))
        if interested:
            client_attrs.append("interested = '{}'".format(self.conn.escape_string(interested)))
        if see_again:
            client_attrs.append("see_again = '{}'".format(self.conn.escape_string(see_again)))

        attrs = " AND ".join(client_attrs)
        sql = "{}{}".format(select, attrs)
        print(sql)
        
        cur.execute(sql)
        return CursorIterator(cur)

    
    
    

    """ Staff Search for Client """
    def fetch_staffClients(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus, interest_category.interest, interest_category.category, date_incurred, fee_type, payment_amount, fee_status, c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn LEFT JOIN Children ON c.ssn = Children.ssn LEFT JOIN client_interests ON c.ssn = client_interests.ssn LEFT JOIN interest_category on client_interests.interest = interest_category.interest LEFT JOIN FEES ON c.ssn = FEES.ssn LEFT JOIN Dates ON c.ssn = Dates.c1_ssn or c.ssn = Dates.c2_ssn;")
        return CursorIterator(cur)
    
    def fetch_staff_match(self, name, gender, dob, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, crime, childName, childDOB, childStatus, interest, category, date_incurred, fee_type, payment_amount, fee_status, location, scheduled_date, occurred, interested, see_again):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        select = "SELECT c.ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, CriminalRecord.crime, Children.childName, Children.childDOB, Children.childStatus, interest_category.interest, interest_category.category, date_incurred, fee_type, payment_amount, fee_status, c1_ssn, c2_ssn, location, scheduled_date, occurred, interested, see_again FROM CLient c LEFT JOIN CriminalRecord On c.ssn = CriminalRecord.ssn LEFT JOIN Children ON c.ssn = Children.ssn LEFT JOIN client_interests ON c.ssn = client_interests.ssn LEFT JOIN interest_category on client_interests.interest = interest_category.interest LEFT JOIN FEES ON c.ssn = FEES.ssn LEFT JOIN Dates ON c.ssn = Dates.c1_ssn or c.ssn = Dates.c2_ssn WHERE "
        client_attrs = []
        print(gender)
        
        if name:
            client_attrs.append("name = '{}'".format(self.conn.escape_string(name)))
        if gender:
            client_attrs.append("gender = '{}'".format(self.conn.escape_string(gender)))
        if dob:
            client_attrs.append("dob = '{}'".format(dob))
        if eyecolor:
            client_attrs.append("eyecolor = '{}'".format(self.conn.escape_string(eyecolor)))
        if weight:
            client_attrs.append("weight = {}".format(weight))
        if height:
            client_attrs.append("height = {}".format(height))
        if prior_marriage:
            client_attrs.append("prior_marriage = '{}'".format(self.conn.escape_string(prior_marriage)))
        if interest_in:
            client_attrs.append("interest_in = '{}'".format(self.conn.escape_string(interest_in)))
        if date_open:
            client_attrs.append("date_open = '{}'".format(date_open))
        if date_close:
            client_attrs.append("date_close = '{}'".format(date_close))
        if status:
            client_attrs.append("status = '{}'".format(self.conn.escape_string(status)))
        if crime:
            client_attrs.append("crime = '{}'".format(self.conn.escape_string(crime)))
        if childName:
            client_attrs.append("childName = '{}'".format(self.conn.escape_string(childName)))
        if childDOB:
            client_attrs.append("childDOB = '{}'".format(childDOB))
        if childStatus:
            client_attrs.append("childStatus = '{}'".format(self.conn.escape_string(childStatus)))
        if interest:
            client_attrs.append("interest = '{}'".format(self.conn.escape_string(interest)))
        if category:
            client_attrs.append("category = '{}'".format(self.conn.escape_string(category)))
        if date_incurred:
            client_attrs.append("date_incurred = '{}'".format(date_incurred))
        if fee_type:
            client_attrs.append("fee_type = '{}'".format(self.conn.escape_string(fee_type)))
        if payment_amount:
            client_attrs.append("paymen_amount = '{}'".format(payment_amount))
        if fee_status:
            client_attrs.append("fee_status = '{}'".format(self.conn.escape_string(fee_status)))
        if location:
            client_attrs.append("location = '{}'".format(self.conn.escape_string(location)))
        if scheduled_date:
            client_attrs.append("scheduled_date = '{}'".format(scheduled_date))
        if occurred:
            client_attrs.append("occurred = '{}'".format(self.conn.escape_string(occurred)))
        if interested:
            client_attrs.append("interested = '{}'".format(self.conn.escape_string(interested)))
        if see_again:
            client_attrs.append("see_again = '{}'".format(self.conn.escape_string(see_again)))

        attrs = " AND ".join(client_attrs)
        sql = "{}{}".format(select, attrs)
        print(sql)
        cur.execute(sql)
        return CursorIterator(cur)


