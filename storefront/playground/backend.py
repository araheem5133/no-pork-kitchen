from ast import Slice
from re import S
import mysql.connector
import collections

from mysqlx import RowResult

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="NPK")
location = geolocator.geocode("20 W 34th St NYC") 

lat = location.latitude
long = location.longitude
coord1 = (location.latitude, location.longitude)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Youshallnotpass!", # Change accordingly
    database = "noporkkitchendb"
)

cur = mydb.cursor()

def getDistance(address):
    global geolocator
    global coord1
    location = geolocator.geocode(address)
    coord2 = (location.latitude, location.longitude)

    return geodesic(coord1, coord2)

def addEarnings(driverID, earnings):
    sql = "SELECT earnings, no_deliveries FROM Delivery WHERE userID =" + str(driverID) + ";"
    cur.execute(sql)
    rows = cur.fetchall()
    ret = 0
    for row in rows:
        val = row[0]
        val2 = row[1]
    ret = float(val) + float(earnings)
    val2 = int(val2) + 1
    sql = "UPDATE Delivery SET earnings = %s AND no_deliveries = %s WHERE userID = %s"
    val = (ret, val2,driverID)
    cur.execute(sql, val)
    mydb.commit()


def currentCus():
        sql = "SELECT currentcus FROM Accumulator;"
        cur.execute(sql)
        rows = [x[0] for x in cur.fetchall()]
        for row in rows:
                return row

def currentOrd():
        sql = "SELECT currentord FROM Accumulator;"
        cur.execute(sql)
        rows = [x[0] for x in cur.fetchall()]
        for row in rows:
                return row

def onGoingDelivery(deliveryID):
    sql = "SELECT order_no, customerID FROM Orders WHERE deliveryID =" + str(deliveryID) + " AND status = 'cooked';"
    cur.execute(sql)
    rows = cur.fetchall()
    ret = []
    for row in rows:
        ret.append([row[0], row[1]])
    return ret

def returnDeliveryAddresses(order_nums):
    ret = []
    print(order_nums)
    for x, y in order_nums:
        sql = "SELECT address FROM Customers WHERE userID=" + str(y) + ";"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            ret.append([x, row[0]])
    return ret


currcus = currentCus()
currord = currentOrd()

def createManager():
    global currcus
    sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (1, "admin", "admin", "pass", "manager", "-", 0)
    cur.execute(sql, val)
    sql = "INSERT INTO Managers (userID, salary, hours_worked) VALUES (%s, %s, %s)"
    val = (1, 100, 0)
    cur.execute(sql, val)
    sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
    cur.execute(sql)
    currcus += 1
    mydb.commit()

def checkCredentials(username, password):
    sql = "SELECT userID, userType FROM Users WHERE username = %s and password = %s;"
    val = (username, password)
    cur.execute(sql,val)
    rows = cur.fetchall()
    if len(rows)==0:
        return 0
    else:
        return 1

def setCooked(orderNo):
    sql = "UPDATE Orders SET status = 'cooked' WHERE order_no = " + str(orderNo) + ";"
    cur.execute(sql)
    mydb.commit()

def setDelivered(orderNo):
    sql = "UPDATE Orders SET status = 'delivered' WHERE order_no = " + str(orderNo) + ";"
    cur.execute(sql)
    mydb.commit()

def allItemsDone(orderNo):
    sql = "SELECT * FROM OrderItems WHERE order_no = %s AND status = %s"
    val = (orderNo, "pending")
    cur.execute(sql, val)
    rows = cur.fetchall()
    if(len(rows)>0):
        return False
    else:
        return True

def loginSQL(username, password):
    sql = "SELECT userID, userType, name FROM Users WHERE username = %s and password = %s;"
    val = (username, password)
    cur.execute(sql,val)
    rows = cur.fetchall()
    for x in rows:
        return x

def getCustomerData(userID):
    sql = "SELECT address, balance, VIP_STATUS FROM Customers WHERE userID = " + str(userID) +";"
    cur.execute(sql)
    rows = cur.fetchall()
    for x in rows:
        return x

def getDeliveryData(userID):
    sql = "SELECT distance, earnings, no_deliveries FROM Delivery WHERE userID = " + str(userID) +";"
    cur.execute(sql)
    rows = cur.fetchall()
    for x in rows:
        return x

def getChefData(userID):
    sql = "SELECT salary, hours_worked FROM Chefs WHERE userID = " + str(userID) +";"
    cur.execute(sql)
    rows = cur.fetchall()
    for x in rows:
        return x

def getManagerData(userID):
    sql = "SELECT salary, hours_worked FROM Managers WHERE userID = " + str(userID) +";"
    cur.execute(sql)
    rows = cur.fetchall()
    for x in rows:
        return x

def addBalance(userID, bal):
    sql = "UPDATE Customers SET balance =%s WHERE userID = %s"
    val = (bal, userID)
    cur.execute(sql, val)
    mydb.commit()

def giveiOrder(ordernum, itemno, price, quantity):
    sql = "INSERT INTO OrderItems (order_no, item_no, price, quantity, status) VALUES (%s, %s, %s, %s, %s)"
    val = (ordernum, itemno, price, quantity, "pending")
    cur.execute(sql, val)
    mydb.commit()

def setCookedItem(orderno, itemno):
    sql = "UPDATE OrderItems SET status = %s WHERE order_no = %s AND item_no = %s"
    val = ("cooked", orderno, itemno)
    cur.execute(sql, val)
    mydb.commit()

def giveOrder(ordernum, customerID, deliveryID, total_price, status):
    sql = "INSERT INTO Orders (order_no, customerID, deliveryID, total_price, status) VALUES (%s, %s, %s, %s, %s)"
    val = (ordernum, customerID, deliveryID, total_price, status)
    cur.execute(sql, val)
    mydb.commit()

def returnPrice(itemno):
    sql = "SELECT Price FROM Food WHERE item_no = " + str(itemno) + ";"
    cur.execute(sql)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def returnName(userID):
    sql = "SELECT name FROM Users WHERE userID= " + str(userID) + ";"
    cur.execute(sql)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def returnOrders(userID):
    sql = "SELECT order_no, total_price, deliveryID FROM Orders WHERE customerID= " + str(userID) + " AND deliveryID IS NOT NULL;"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def populateTable(orders):
    ret = []
    for x in orders:
        ret.append( [x[0], x[1], returnName(x[2])] )
    return ret

def returnItems():
    sql = "SELECT image, item_no, name, price, description FROM Food;"
    cur.execute(sql)
    rows = cur.fetchall()
    ret = []
    for x in rows:
        ret.append([x[0], x[1], x[2], x[3], x[4]] )
    return ret

def getFoodName(id):
    sql = "SELECT name FROM Food WHERE item_no=" + str(id) + ";"
    cur.execute(sql)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def returnChefFood(id):
    sql = "SELECT item_no FROM Food WHERE chefID = " + str(id) + ";"
    cur.execute(sql)
    rows = cur.fetchall()
    ret = []
    for row in rows:
        ret.append(row[0])
    return ret

def returnFoodName(item):
    sql = "SELECT name FROM Food WHERE item_no= " + str(item) + ";"
    cur.execute(sql)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def returnPending(items):
    ret = []
    ret2 = []
    emptySet = set()
    for x in items:
        sql = "SELECT order_no FROM OrderItems WHERE item_no =" + str(x) + ";"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            emptySet.add(row[0])
    for x in emptySet:
        sql = "SELECT order_no FROM Orders WHERE order_no = " + str(x) + " AND status = 'pending';"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            ret.append(row[0])
    for x in ret:
        for y in items:
            sql = "SELECT item_no, quantity FROM OrderItems WHERE order_no = %s AND item_no = %s AND status = %s;"
            val = (x, y, "pending")
            cur.execute(sql, val)
            rows = cur.fetchall()
            for row in rows:
                ret2.append( [x, returnFoodName(row[0]), row[1], y] )
    return ret2

class ShoppingCart:
    global currord
    def __init__(self, num, quantity, userID):
        self.num = num
        self.quantity = quantity
        self.userID = userID

    def returnNum(self):
        return self.num

    def returnQuantity(self):
        return self.quantity

    def findDuplicates(self):
        if len(self.num) == len(set(self.num)):
            return False
        else:
            return True
    
    def addItem(self, itemno, itemq):
        self.num.append(itemno)
        self.quantity.append(itemq)
        if(self.findDuplicates()):
            self.num.pop()
            self.quantity.pop()
            return False
        return True

    def calculateTotal(self):
        total = 0
        for i in range(len(self.num)):
            total += (float(returnPrice(self.num[i]))*float(self.quantity[i]))
        return total
    
    def calculateComponent(self, i):
        return (float(returnPrice(self.num[i])) * float(self.quantity[i]))

    def fillTable(self):
        ret = []
        for i in range(len(self.num)):
            ret.append( [getFoodName(self.num[i]), self.quantity[i], self.calculateComponent(i), i] )
        print(ret)
        return ret

    def removeItem(self, i):
        self.num.pop(i)
        self.quantity.pop(i)

    def executeOrder(self, driverID):
        global currord
        total = self.calculateTotal()
        try:
            giveOrder(currord, self.userID, driverID, total, "pending")
            for i in range(len(self.num)):
                giveiOrder(currord, self.num[i], returnPrice(self.num[i]), self.quantity[i])
            sql = "UPDATE Accumulator SET currentord = " + str(currentOrd()+1) + ";"
            cur.execute(sql)
            currord+=1
            self.num = []
            self.quantity =[]
            return total
        except:
            print("Order number already pending")
            return 0



def registerSQL(userID, name, address, username, password, usertype):
    global currcus
    sql = "Select %s FROM Users WHERE username = %s;"
    val = (username, "userID")
    cur.execute(sql, val)
    if len(cur.fetchall())==0:
        if(usertype=="Customer"):
            sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userID, name, username, password, usertype, "nil", 0)
            cur.execute(sql, val)
            sql = "INSERT INTO Customers (userID, balance, address, VIP_Status) VALUES (%s, %s, %s, %s)"
            val = (userID, 0, address, 0)
            cur.execute(sql, val)
            sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
            cur.execute(sql)
            currcus += 1
            mydb.commit()
            return 1
        elif (usertype=="Chef"):
            sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userID, name, username, password, usertype, "nil", 0)
            cur.execute(sql, val)
            sql = "INSERT INTO Chefs (userID, salary, hours_worked) VALUES (%s, %s, %s)"
            val = (userID, 20, 0)
            cur.execute(sql, val)
            sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
            cur.execute(sql)
            currcus += 1
            mydb.commit()
            return 1
        elif (usertype=="Delivery"):
            sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userID, name, username, password, usertype, "nil", 0)
            cur.execute(sql, val)
            sql = "INSERT INTO Delivery (userID, distance, earnings, no_deliveries) VALUES (%s, %s, %s, %s)"
            val = (userID, 0, 0, 0)
            cur.execute(sql, val)
            sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
            cur.execute(sql)
            currcus += 1
            mydb.commit()
            return 1
    else:
        print("Username already in use.")
        return 0

def findAddress(userID):
    sql = "SELECT address FROM Customers WHERE userID = " + str(userID) + ";"
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        return r[0]

def findReadyOrders():
    ret = []
    sql = "SELECT order_no, customerID FROM Orders WHERE deliveryID IS NULL AND status = 'cooked';"
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        ret.append([r[0], findAddress(r[1])])

    return ret

def setDriver(orderNo, driverID):
    sql = "UPDATE Orders SET deliveryID = %s WHERE order_no = %s;"
    val = (driverID, orderNo)
    cur.execute(sql, val)
    mydb.commit()


def removeBid(dict, accepted):
    del dict[accepted]
    return dict

class Bids:
    def __init__(self, orderNo, bids):
        self.orderNo = orderNo
        self.bids = bids

    def addBid(self, bid):
        self.bids.append(bid)
    
    def returnBids(self):
        return self.bids

    def printAllBids(self):
        print (self.bids)

    def acceptBid(self, ID):
        ret = []
        for a, b in self.bids:
            if(a==ID):
                setDriver(self.orderNo, ID)
                ret.append([a, b, self.orderNo])
                return ret

def addToBids(dict, orderNo, driverNo, num):
        temp = dict.get(orderNo)
        try:
            temp.addBid([driverNo, num])
        except:
            s = Bids(orderNo, [])
            s.addBid([driverNo, num])
            dict[orderNo] = s
            return  
        dict[orderNo] = temp

def getChefAdmin():
    ret = []
    sql = "SELECT userID, salary, hours_worked FROM Chefs"
    cur.execute(sql)
    row = cur.fetchall()
    for rows in row:
        ret.append([rows[0], returnName(rows[0]), rows[1], rows[2]])
    return ret

def chefAdminDisplay(chefs):
    ret = []
    stri = ""
    for a, b, c, d in chefs:
        stri = stri + str(a) + ". " + str(b) + " Salary = " + str(c) + " Hours Worked = " + str(d)
        ret.append(stri)
        stri = ""
    return ret

def changeSalary(userID, num):
    sql = "UPDATE Chefs SET salary = %s WHERE userID = %s"
    val = (num, userID)
    cur.execute(sql, val)
    mydb.commit()

def changeHours(userID, num):
    sql = "UPDATE Chefs SET hours_worked = %s WHERE userID = %s"
    val = (num, userID)
    cur.execute(sql, val)
    mydb.commit()

def bidsAdminDisplay(dict):
    ret = []
    ret2 = []
    for i in dict:
        for x in dict[i].returnBids():
            ret2.append([x[0],returnName(x[0]),x[1]])
        ret.append([i,ret2])
        ret2 = []
    return ret

def setDelivered(orderNo):
    sql = "UPDATE Orders SET status = 'delivered' WHERE order_no = " + str(orderNo) + ";"
    cur.execute(sql)
    mydb.commit()

def getUnreviewedD(id):
    ret = []
    sql = "SELECT order_no FROM Orders WHERE customerID = " + str(id) + " AND delivery_rating IS NULL AND delivery_review IS NULL;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        ret.append(row[0])
    return ret

def getUnreviewedC(id):
    ret = []
    ret2 = []
    sql = "SELECT order_no FROM Orders WHERE customerID = " + str(id) + ";"
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        ret2.append(row[0])
    for i in ret2:
        sql = "SELECT item_no FROM OrderItems WHERE order_no = " + str(i) + " AND item_rating IS NULL AND item_review IS NULL;;"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            ret.append([i, row[0], returnFoodName(row[0])])
    return ret

def giveReview(orderNo, itemNo, rating, review):
    sql = "UPDATE OrderItems SET item_rating = %s WHERE order_no = %s AND item_no = %s;"
    val = (rating, orderNo, itemNo)
    cur.execute(sql, val)
    sql = "UPDATE OrderItems SET item_review = %s WHERE order_no = %s AND item_no = %s;"
    val = (review, orderNo, itemNo)
    cur.execute(sql, val)
    mydb.commit()

def giveDReview(orderNo, rating, review):
    sql = "UPDATE Orders SET delivery_rating = %s WHERE order_no = %s;"
    val = (rating, orderNo)
    cur.execute(sql, val)
    sql = "UPDATE Orders SET delivery_review = %s WHERE order_no = %s;"
    val = (review, orderNo)
    cur.execute(sql, val)
    mydb.commit()

def findDReviews(driverID):
    ret = []
    sql = "SELECT order_no, delivery_rating, delivery_review FROM Orders WHERE deliveryID = " + str(driverID) + " AND (delivery_rating IS NOT NULL OR delivery_review IS NOT NULL);"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        ret.append([row[0], row[1], row[2]])
    return ret

def findCReviews(chefID):
    ret = returnChefFood(chefID)
    ret2 = []
    for i in ret:
        sql = "SELECT order_no, item_no, item_rating, item_review FROM OrderItems WHERE item_no = " + str(i) + " AND (item_rating IS NOT NULL OR item_review IS NOT NULL);"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            ret2.append([row[0], returnFoodName(row[1]), row[2], row[3]])
    return ret2