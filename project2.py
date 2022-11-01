import threading
import random
import time
from queue import Queue

## Customer Object ##
class Customers():
    def __init__(self, cid, transactionType):
        self.cid = cid
        self.transactionType = transactionType
    def __str__(self) :
        return ("Customer " + str(self.cid))
    def getTransactionType(self):
        return self.transactionType

## Teller Objects ##
class Tellers():
    def __init__(self, tid):
        print("teller object created")
        self.tid = tid
    def __str__(self):
        return ("Teller " + str(self.tid))


## NECESSARY SEMAPHORES ##
gLock = threading.Semaphore(1)
waitForTeller = threading.Semaphore(3)
waitForEnter = threading.Semaphore(2)
waitForSafe = threading.Semaphore(2)
waitForManager = threading.Semaphore(1)
waitForTransactionType = threading.Semaphore(3)

## GLOBAL VARIABLES ##
gCount = 0
TellerCount = 0
customerCount = 0

## Client actions ##
clientActionsList = ["withdraw", "deposit"]
timeOptions = [0.05, 0]

## queue for customers ##
bankLineQueue = Queue() ## Bank Line

# Lists to add customers too
customerList = []
tellerList = []

## Enter the bank ##
def goToBank(customer, bankLineQueue,waitForEnter):
    waitForEnter.acquire()
    print(str(customer) + " is entering the bank")
    bankLineQueue.put(customer)
    print(str(customer) + " is joining the line")
    waitForEnter.release()

## Teller-customer transactions
def bankTransactions(teller, waitForManager, waitForSafe, bankLineQueue):

    ## CUSTOMER - TELLER INTRODUCTIONS ##   
    customerT = bankLineQueue.get() # Get a customer from the line
    print(str(customerT) + " is deciding on a teller")
    waitForTeller.acquire() # Claims a teller
    print(str(customerT) + " goes to " + str(teller))
    print(str(customerT) + " introduces itself to " + str(teller))
    print(str(teller) + " is now serving " + str(customerT))
    waitForTransactionType.acquire()
    print(str(customerT) + " requests a " + customerT.getTransactionType())
    transaction = customerT.getTransactionType() #Customer transaction
    waitForTransactionType.release()

    ## BEGINNING TRANSACTIONS##

    if(transaction == "withdraw"):
        print(str(teller) + " is handling a withdrawal transaction")
        print(str(teller) + " is going to the manager")
        print(str(teller) + " is asking the manager")
        waitForManager.acquire()
        print(str(teller) + " is getting the manager's permission")
        time.sleep(random.uniform(.05, .30))
        print (str(teller) + " got the manager's permission")
        waitForManager.release()
    




## Creating the teller threads
for i in range(3):
    print("Making the Tellers")
    teller = Tellers(i)
    t = threading.Thread(target=bankTransactions, args=(teller, waitForManager, waitForSafe, bankLineQueue))
    t.start()
    tellerList.append(t)

## Create the customer threads   
for i in range(5):
    customer = Customers(i, random.choice(clientActionsList))
    #customer = Customers(i, "withdraw")
    c = threading.Thread(target=goToBank, args=(customer, bankLineQueue, waitForEnter))
    c.start()
    customerList.append(c) #Add to the list of customers



