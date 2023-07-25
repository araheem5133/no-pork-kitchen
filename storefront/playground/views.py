from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib import messages
# Create your views here.

from playground.backend import *

currentcus = currentCus()
userID = 0
name = ""
address = ""
warnings = 0
balance = 0
userType = "Guest"
userName = ""
vip_status = 0

distance = 0
earnings = 0
deliveries = 0

salary = 0
hours = 0

orders = []


items = []
nums = []
cart = ShoppingCart(items, nums, userID)

pendingOrder = False
isDelivering = False

bids = {}

isChef = False
isCustomer = False
isDelivery = False
isManager = False

def base(request):
    return render(request, 'base.html')

def guest(request):
    return render(request, 'guest.html')

def food(request):
    return render(request, 'food.html')

def forum(request):
    return render(request, 'forum.html')

def chefd(request):
    global isChef  
    global isDelivery
    global isCustomer
    global isManager 
    global userID
    global userName

    global salary

    global bids

    if 'chefrevs' in request.POST:
        a = request.POST.get('orderCNo')
        b = request.POST.get('itemCNo')
        c = request.POST.get('crating')
        d = request.POST.get('creview')
        giveReview(a, b, c, d)

    if 'devrevs' in request.POST:
        a = request.POST.get('orderDNo')
        b = request.POST.get('drating')
        c = request.POST.get('dreview')
        print(a)
        print(b)
        print(c)
        giveDReview(a, b, c)

    if 'delivered' in request.POST:
        i = request.POST.get('orderNod')
        setDelivered(int(i))

    if 'changeSalary' in request.POST:
        changeSalary(request.POST.get('chefs')[9], request.POST.get('salary'))
    
    if 'changeHours' in request.POST:
        changeHours(request.POST.get('chefs2')[9], request.POST.get('hours'))

    if 'acceptBid' in request.POST:
        txt = request.POST.get('bidselect')
        num = request.POST.get('ordernum')
        start = txt.index("d: ")
        end = txt.index(')', start+1)

        cost = txt[start+4:end]
        start = txt.index('(')
        end = txt.index(')', start+1)
        driverID = txt[start+1:end]

        setDriver(num, driverID)
        removeBid(bids, num)
        addEarnings(driverID, cost)

    if 'bidding' in request.POST:
        x = request.POST.get('orderNo')
        y = request.POST.get('val')
        addToBids(bids, x, userID, y)
    if 'finish' in request.POST:
        x = request.POST.get('orderNo')
        y = request.POST.get('itemID')
        setCookedItem(x, y)
        if(allItemsDone(x)):
            setCooked(x)
            bids[x] = Bids(x, [])
    return render(request, 'chefd.html', {  'isChef': isChef, 
                                            'userName': userName, 
                                            'isDelivery': isDelivery,
                                            'isManager': isManager,
                                            'isCustomer': isCustomer, 
                                            'deliveries': findReadyOrders(),
                                            'chefs': getChefAdmin(),
                                            'bids': bidsAdminDisplay(bids),
                                            'orders': returnPending(returnChefFood(userID)),
                                            'cookeds': getUnreviewedC(userID),
                                            'delivereds': getUnreviewedD(userID),
                                            'accepted': returnDeliveryAddresses(onGoingDelivery(userID))})

def checkout(request):
    global cart
    global name
    global balance
    global userID

    global items
    global nums
    global pendingOrder
    str = ""

    if 'delete' in request.POST:
        print(request.POST.get('itemID'))
        cart.removeItem( int(request.POST.get('itemID')) )
        str = "Item removed successfully!"
    if 'checkout' in request.POST:
        if cart:
            #try:
                i = cart.executeOrder(None)
                balance = float(balance) - float(i)
                addBalance(userID, balance)
                items = []
                nums = []
                #str = "Order executed successfully!"
                pendingOrder = True
            #except:
                #str = "Order failed..."
    #messages.success(request, str)
    return render(request, 'checkout.html', {'items': cart.fillTable, 'name': name, 'balance' : balance, 'total_price': cart.calculateTotal})


def menu(request):
    global cart
    global items
    global nums
    global userID
    ret = returnItems()
    cart = ShoppingCart(items, nums, userID)
    str = ""
    if 'checkout' in request.POST:
        try:
            i = cart.addItem(request.POST.get('itemID'), request.POST.get('quantity'))
            if i:
                str = "Item added successfully!"
            else:
                str = "Duplicate item chosen, item was not added to the cart!"
        except:
            str = "Item could not be added!"
    messages.success(request, str)
    return render(request, 'menu.html', {'menu': ret})

def homepage(request):
    return render(request, 'homepage.html')

def profile(request):
    global userID 
    global balance
    global orders
    if 'bal' in request.POST:
        try:
            temp = int(balance)
            temp += int(request.POST.get('addedBalance'))
            addBalance(userID, temp)
        except:
            print("Doesn't work.")

    if(userType=="Customer"):
                y = getCustomerData(userID)
                address = y[0]
                balance = y[1]
                vip_status = y[2]
                try:
                    orders = populateTable(returnOrders(userID))
                except:
                    pass
                return render(request, 'profile.html', {'name': name, 
                                                    'role': userType, 
                                                    'isCustomer': True,
                                                    'isDelivery': False,
                                                    'isChef': False,
                                                    'isManager': False,  
                                                    'balance': balance,
                                                    'address': address,
                                                    'VIP': vip_status,
                                                    'username': userName,
                                                    'orders': orders} )
    elif(userType=="Delivery"):
        y = getDeliveryData(userID)
        distance = y[0]
        earnings = y[1]
        deliveries = y[2]

        return render(request, 'profile.html', {'name': name, 
                                                    'role': userType, 
                                                    'isCustomer': False,
                                                    'isDelivery': True,
                                                    'isChef': False,
                                                    'isManager': False,  
                                                    'distance': distance,
                                                    'earnings': earnings,
                                                    'deliveries': deliveries,
                                                    'username': userName,
                                                    'dreviews': findDReviews(userID)} )
    elif(userType=="Chef"):
        z = getChefData(userID)
        salary = z[0]
        hours = z[1]
        return render(request, 'profile.html', {'name': name, 
                                                'role': userType, 
                                                'isCustomer': False,
                                                'isDelivery': False,
                                                'isChef': True,
                                                'isManager': False, 
                                                'salary': salary,
                                                'hours': hours,
                                                'username': userName,
                                                'creviews': findCReviews(userID)})
    elif(userType=="Manager"):
        e = getManagerData(userID)
        salary = e[0]
        hours = e[1]
        return render(request, 'profile.html', {'name': name, 
                                                'role': userType, 
                                                'isCustomer': False,
                                                'isDelivery': False,
                                                'isChef': False,
                                                'isManager': True,
                                                'salary': salary,
                                                'hours': hours,
                                                'username': userName})
    return render(request, 'profile.html')

def chef(request):
    return render(request, 'chef.html')

def login(request):
    global userID
    global userType
    global name
    global userName

    global address
    global balance
    global vip_status

    global distance
    global earnings
    global deliveries

    global hours
    global salary

    global orders

    global isChef
    global isCustomer
    global isDelivery
    global isManager

    str = ""
    if 'bal' in request.POST:
        try:
            print(request.POST.get('addedBalance'))
        except:
            print("Doesn't work.")

    if 'login' in request.POST:

        i = checkCredentials(request.POST.get('username'),
                             request.POST.get('password'))
        if i == 1: 
            x = loginSQL(request.POST.get('username'), 
                        request.POST.get('password'))
            userID = x[0]
            userType = x[1]
            name = x[2]
            userName = request.POST.get('username')

            if(userType=="Customer"):
                isCustomer = True
                isChef = False
                isDelivery = False
                isManager = False
                y = getCustomerData(userID)
                address = y[0]
                balance = y[1]
                vip_status = y[2]
                try:
                    orders = populateTable(returnOrders(userID))
                except:
                    pass
                return render(request, 'profile.html', {'name': name, 
                                                    'role': userType, 
                                                    'isCustomer': True,
                                                    'isDelivery': False,
                                                    'isChef': False,
                                                    'isManager': False,  
                                                    'balance': balance,
                                                    'address': address,
                                                    'VIP': vip_status,
                                                    'username': userName,
                                                    'orders': orders} )
            elif(userType=="Delivery"):
                isCustomer = False
                isChef = False
                isDelivery = True
                isManager = False
                y = getDeliveryData(userID)
                distance = y[0]
                earnings = y[1]
                deliveries = y[2]

                return render(request, 'profile.html', {'name': name, 
                                                    'role': userType, 
                                                    'isCustomer': False,
                                                    'isDelivery': True,
                                                    'isChef': False,
                                                    'isManager': False,  
                                                    'distance': distance,
                                                    'earnings': earnings,
                                                    'deliveries': deliveries,
                                                    'username': userName,
                                                    'dreviews': findDReviews(userID)} )
            elif(userType=="Chef"):
                isCustomer = False
                isChef = True
                isDelivery = False
                isManager = False
                z = getChefData(userID)
                salary = z[0]
                hours = z[1]
                return render(request, 'profile.html', {'name': name, 
                                                    'role': userType, 
                                                    'isCustomer': False,
                                                    'isDelivery': False,
                                                    'isChef': True,
                                                    'isManager': False, 
                                                    'salary': salary,
                                                    'hours': hours,
                                                    'username': userName,
                                                    'creviews': findCReviews(userID)} )
            elif(userType=="Manager"):
                isCustomer = False
                isChef = False
                isDelivery = False
                isManager = True
                e = getManagerData(userID)
                salary = e[0]
                hours = e[1]
                return render(request, 'profile.html', {'name': name, 
                                                    'role': userType, 
                                                    'isCustomer': False,
                                                    'isDelivery': False,
                                                    'isChef': False,
                                                    'isManager': True, 
                                                    'salary': salary,
                                                    'hours': hours,
                                                    'username': userName} )


        else:
            str = "Login failed. Please check your username or password."
    messages.success(request, str)
    return render(request, 'login.html')

def register(request):
    global currentcus
    str = ""
    if 'register' in request.POST:
        if request.POST.get('new_pswd') == request.POST.get('re_pswd'):
            try:
                i = registerSQL(currentcus,
                    request.POST.get('name'),
                    request.POST.get('address'),
                    request.POST.get('new_user'),
                    request.POST.get('re_pswd'),
                    request.POST.get('role'))
                currentcus = currentCus()
                if i == 1:
                    str = "Registered successfully!"
                elif i == 0:
                    str = "Username already in use."
            except:
                str = "Database error."
        else:
            str = "Passwords do not match. Please try again."
    messages.success(request, str)
    return render(request, 'register.html')