import sqlite3
from DAO import *
import atexit


class _Repository:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.vaccines = Vaccines(self.conn)
        self.suppliers = Suppliers(self.conn)
        self.clinics = Clinics(self.conn)
        self.logistics = Logistics(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def createTables(self):
        self.conn.executescript("""
        CREATE TABLE logistics(
        id             INTEGER          PRIMARY KEY,
        name           TEXT         NOT NULL,
        count_sent     INTEGER          NOT NULL,
        count_received INTEGER          NOT NULL
        );
        CREATE TABLE suppliers(
        id        INTEGER         PRIMARY KEY,
        name      TEXT        NOT NULL,
        logistic  INTEGER         NOT NULL,
        
        FOREIGN KEY(logistic) REFERENCES Logistics(id)
        );
        CREATE TABLE clinics(
        id        INTEGER         PRIMARY KEY,
        location  TEXT        NOT NULL,
        demand    INTEGER         NOT NULL,
        logistic  INTEGER         NOT NULL,
        
        FOREIGN KEY(logistic) REFERENCES Logistics(id)
        );
        CREATE TABLE vaccines (
        id        INTEGER         PRIMARY KEY,
        date      DATE        NOT NULL,
        supplier  INTEGER         NOT NULL,
        quantity  INTEGER         NOT NULL,
        
        FOREIGN KEY(supplier) REFERENCES Suppliers(id)
        )         
        """)

    def recShip(self, supName, amount, date):
        newId = self.vaccines.getId()
        supId = self.suppliers.getId(supName)
        self.vaccines.insert(Vaccine(newId, date, supId, amount))
        self.logistics.recShip(self.suppliers.getLogisticId(supName), amount)

    def sendShip(self, location, amountStr):
        amount = int(amountStr)
        clin = self.clinics.getByLocation(location)
        self.logistics.sendShip(clin.logistic, amount)
        self.clinics.decreseDemand(location, amount)
        while amount > 0:
            vac = self.vaccines.getOldest()
            if amount >= vac.quantity:
                amount -= vac.quantity
                self.vaccines.remove(vac.id)
            else:
                self.vaccines.updateQuantity(vac.id, vac.quantity - amount)
                amount = 0

    def sumFile(self):
        quantities = 0
        demands = 0
        received = 0
        sent = 0
        for line in self.vaccines.getQuantities():
            quantities += line[0]
        for line in self.clinics.getDemands():
            demands += line[0]
        for line in self.logistics.getCounts():
            sent += line[0]
            received += line[1]
        return [str(quantities), str(demands), str(received), str(sent)]

repo = _Repository()
atexit.register (repo.close)

