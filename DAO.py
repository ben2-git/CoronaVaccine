from DTO import *


class Vaccines:
    def __init__(self, conn):
        self.maxId = 0
        self.conn = conn

    def insert(self, vaccine):
        self.conn.execute("""
        INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
                          """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def getId(self):
        self.maxId = self.maxId + 1
        return self.maxId - 1

    def setId(self, maxId):
        self.maxId = maxId+1

    def getOldest(self):
        c = self.conn.cursor()
        c.execute("""
           SELECT * FROM vaccines ORDER BY date ASC 
           """)
        return Vaccine(*c.fetchone())

    def remove(self, vacId):
        self.conn.execute("""
        DELETE FROM vaccines WHERE id = ?
        """, [vacId])

    def updateQuantity(self, vacId, quantity):
        self.conn.execute("""
               UPDATE vaccines SET quantity = (?) WHERE id = (?)
               """, [quantity, vacId])

    def getQuantities(self):
        c = self.conn.cursor()
        c.execute("""
                   SELECT quantity FROM vaccines 
                   """)
        return c.fetchall()


class Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute("""
           INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)
                          """, [supplier.id, supplier.name, supplier.logistic])

    def getLogisticId(self, name):
        c = self.conn.cursor()
        c.execute("""
           SELECT logistic FROM suppliers WHERE name = ?
           """, [name])
        return c.fetchone()[0]

    def getId(self, name):
        c = self.conn.cursor()
        c.execute("""
                   SELECT id FROM suppliers WHERE name = ?
                   """, [name])
        return c.fetchone()[0]


class Logistics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, logistic):
        self.conn.execute("""
                   INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
                          """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def getById(self, logId):
        c = self.conn.cursor()
        c.execute("""
        SELECT * FROM logistics WHERE id = ?
        """, [logId])
        return Logistic(*c.fetchone())

    def recShip(self, logId, amountStr):
        log = self.getById(logId)
        amount = int(amountStr)
        amount += log.count_received
        self.conn.execute("""
        UPDATE logistics SET count_received = (?) WHERE id = (?)
        """, [amount, logId])

    def sendShip (self, logId, amount):
        log = self.getById(logId)
        amount += log.count_sent
        self.conn.execute("""
                UPDATE logistics SET count_sent = (?) WHERE id = (?)
                """, [amount, logId])

    def getCounts(self):
        c = self.conn.cursor()
        c.execute("""
            SELECT count_sent, count_received FROM logistics 
            """)
        return c.fetchall()


class Clinics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, clinic):
        self.conn.execute("""
                    INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
                    """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def getByLocation(self, location):
        c = self.conn.cursor()
        c.execute("""
        SELECT * FROM clinics WHERE location = ?
        """, [location])
        return Clinic(*c.fetchone())

    def decreseDemand(self, location, amountStr):
        amount = int(amountStr)
        demand = self.getByLocation(location).demand - amount
        if demand < 0:
            demand = 0
        self.conn.execute("""
               UPDATE clinics SET demand = (?) WHERE location = (?)
               """, [demand, location])

    def getDemands(self):
        c = self.conn.cursor()
        c.execute("""
                      SELECT demand FROM clinics 
                      """)
        return c.fetchall()
