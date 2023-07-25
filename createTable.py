import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Youshallnotpass!", # Change accordingly
    database = "NoPorkKitchenDB"
)

mycursor = mydb.cursor()

#------------------------------Drop TABLES------------------------------------
mycursor.execute("DROP TABLE IF EXISTS SystemLog")
mycursor.execute("DROP TABLE IF EXISTS Merit")
mycursor.execute("DROP TABLE IF EXISTS OrderItems")
mycursor.execute("DROP TABLE IF EXISTS Orders")
mycursor.execute("DROP TABLE IF EXISTS Food")
mycursor.execute("DROP TABLE IF EXISTS Discussions")
mycursor.execute("DROP TABLE IF EXISTS Users")
mycursor.execute("DROP TABLE IF EXISTS Managers")
mycursor.execute("DROP TABLE IF EXISTS Chefs")
mycursor.execute("DROP TABLE IF EXISTS Delivery")
mycursor.execute("DROP TABLE IF EXISTS Customers")
mycursor.execute("DROP TABLE IF EXISTS Accumulator")

#------------------------------USERS TABLE------------------------------------
Attributes = """(userID INT PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    username VARCHAR(32) UNIQUE NOT NULL,
                    password VARCHAR(32) NOT NULL,
                    userType VARCHAR(20) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    flag INT)"""
mycursor.execute("CREATE TABLE Users " + Attributes)
#MANAGER TABLE
Attributes = """(userID INT PRIMARY KEY,
                    salary DECIMAL(10,2) NOT NULL,
                    hours_worked INT NOT NULL)"""
mycursor.execute("CREATE TABLE Managers " + Attributes)
#CHEF TABLE
Attributes = """(userID INT PRIMARY KEY,
                    salary DECIMAL(10,2) NOT NULL,
                    hours_worked INT NOT NULL)"""
mycursor.execute("CREATE TABLE Chefs " + Attributes)
#DELIVERY TABLE
Attributes = """(userID INT PRIMARY KEY,
                    distance DECIMAL(10,2) NOT NULL, 
                    earnings DECIMAL(10,2) NOT NULL,
                    no_deliveries INT NOT NULL)"""
mycursor.execute("CREATE TABLE Delivery " + Attributes)
#CUSTOMER TABLE
Attributes = """(userID INT PRIMARY KEY,
                    balance DECIMAL(10,2) NOT NULL, 
                    address VARCHAR(100),
                    VIP_STATUS INT NOT NULL)"""
mycursor.execute("CREATE TABLE Customers " + Attributes)


#------------------------------FOOD TABLE------------------------------------
Attributes = """(item_no INT PRIMARY KEY,
                    price DECIMAL(10,2) NOT NULL, 
                    name VARCHAR(100) UNIQUE NOT NULL,
                    description VARCHAR(200),
                    itemtype VARCHAR(20),
                    rating FLOAT,
                    no_sold INT,
                    chefID INT,
                    FOREIGN KEY (chefID) references Chefs(userID),
                    image VARCHAR(2083))"""
mycursor.execute("CREATE TABLE Food " + Attributes)

#------------------------------Orders TABLE------------------------------------
Attributes = """(order_no INT PRIMARY KEY,
                    customerID INT NOT NULL,
                    deliveryID INT,
                    total_price DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    delivery_rating INT,
                    delivery_review VARCHAR(1000),
                    FOREIGN KEY (customerID) references Customers(userID),
                    FOREIGN KEY (deliveryID) references Delivery(userID))"""
mycursor.execute("CREATE TABLE Orders " + Attributes)

#------------------------------OrderItems TABLE-------------------------------
Attributes = """(order_no INT,
                    item_no INT,
                    price DECIMAL(10,2) NOT NULL,
                    quantity INT NOT NULL,
                    status VARCHAR(20),
                    item_rating INT,
                    item_review VARCHAR(1000),
                    PRIMARY KEY (order_no,item_no),
                    FOREIGN KEY (order_no) references Orders(order_no) ON DELETE CASCADE)"""
mycursor.execute("CREATE TABLE OrderItems " + Attributes)

#------------------------------Forum TABLE------------------------------------
Attributes = """(post_no INT AUTO_INCREMENT PRIMARY KEY,
                    id INT NOT NULL,
                    title VARCHAR(20) NOT NULL, 
                    body TEXT NOT NULL,
                    replies TEXT,
                    FOREIGN KEY (id) references Users(userID))"""
mycursor.execute("CREATE TABLE Discussions " + Attributes)

#------------------------------System TABLE------------------------------------
Attributes = """(entry_no INT PRIMARY KEY,
                    id INT NOT NULL,
                    reviewer INT NOT NULL,
                    reviewtype INT NOT NULL,
                    critique VARCHAR(1000) NOT NULL, 
                    verdict VARCHAR(1000),
                    status INT NOT NULL,
                    FOREIGN KEY (id) references Users(userID),
                    FOREIGN KEY (reviewer) references Users(userID))"""
mycursor.execute("CREATE TABLE SystemLog " + Attributes)

#------------------------------Merit TABLE------------------------------------
Attributes = """(id INT PRIMARY KEY,
                    merit INT NOT NULL,
                    FOREIGN KEY (id) references Users(userID))"""
mycursor.execute("CREATE TABLE Merit " + Attributes)

#------------------------------ACCUMULATOR TABLE------------------------------
Attributes = """(currentcus INT PRIMARY KEY,
                    currentord INT NOT NULL)"""
mycursor.execute("CREATE TABLE Accumulator " + Attributes)

mycursor.execute("INSERT INTO ACCUMULATOR (`currentcus`, `currentord`) VALUES ('2', '1');")
mycursor.execute("INSERT INTO Users ('userID', 'name', 'username', 'password', 'userType', 'status', flag') VALUES ('1', 'admin', 'admin', 'pass', 'Manager', '-', '0');")
mydb.commit()


#mycursor.execute("SHOW TABLES")
#for table in mycursor:
#    print (table)

mycursor.close()
mydb.close()
