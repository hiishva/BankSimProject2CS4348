###
## Name: Ishva Patel
## CS 4348.502
## Project 2 Bank Simulator 
###
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

    #Returns the transaction type of the user
    def getTransactionType(self):
        return self.transactionType

## Teller Objects ##
class Tellers():
    def __init__(self, tid):
        #print("teller object created")
        self.tid = tid
    def __str__(self):
        return ("Teller " + str(self.tid))

## NECESSARY SEMAPHORES ##
waitForTeller = threading.Semaphore(3) #Tellers
waitForEnter = threading.Semaphore(2) # Entry of the bank
waitForSafe = threading.Semaphore(2) #Entering the safe
waitForManager = threading.Semaphore(1) # talking to the manager

## Client actions ##
clientActionsList = ["withdraw", "deposit"]

## Queue for customers ##
bankLineQueue = Queue() ## Bank Line

# Lists to add customers too ##
customerList = []
tellerList = []

## Customers enter the bank ##
def goToBank(customer, bankLineQueue,waitForEnter):

    # Enter the bank#
    waitForEnter.acquire() 
    print(str(customer) + " is entering the bank")
    bankLineQueue.put(customer)
    print(str(customer) + " is joining the line")
    waitForEnter.release() # Release the bank

## Teller-customer transactions
def bankTransactions(teller, waitForManager, waitForSafe, bankLineQueue):
    ## Keep going until the line is empty 
    while (bankLineQueue.empty() == False):

        ## CUSTOMER - TELLER INTRODUCTIONS ## 
        customerT = bankLineQueue.get() # Get a customer from the line
        print(str(customerT) + " is deciding on a teller")
        waitForTeller.acquire() # Claims a teller
        print(str(customerT) + " goes to " + str(teller))
        print(str(customerT) + " introduces itself to " + str(teller))
        print(str(teller) + " is now serving " + str(customerT))
        print(str(customerT) + " requests a " + customerT.getTransactionType())
        transaction = customerT.getTransactionType() #Customer transaction
        
        ## BEGINNING TRANSACTIONS##
        #The transaction is withdraw
        if(transaction == "withdraw"):
            print(str(teller) + " is handling a withdrawal transaction")
            # Getting manager's permission
            print(str(teller) + " is going to the manager")
            print(str(teller) + " is asking the manager")
            waitForManager.acquire() # get the manager
            print(str(teller) + " is getting the manager's permission")
            time.sleep(random.uniform(.005, .030)) # waiting for manager's permissions Selecting random time between (.05s and .3s)
            print (str(teller) + " got the manager's permission")
            waitForManager.release() # release the manager
        elif(transaction == "deposit"):  # if the transaction is deposit
            print (str(teller) + " is handling a deposit transaction")
        
        ## GO TO THE SAFE ##
        print(str(teller) + " is going to the safe")
        waitForSafe.acquire()
        print(str(teller) + " is in the safe")
        time.sleep(random.uniform(.01, .05)) #Working in the safe (.01s to 0.05s)
        print(str(teller) + " is leaving the safe")
        waitForSafe.release()
        print (str(teller) + " is back from the safe")

        ## FINISH THE TRANSACTIONS ##
        print(str(teller) + " is finished handling " + str(customerT) + "'s transaction.")
        waitForTeller.release()
        print(str(customerT) + " is leaving the bank")

## CREATING THREADS ## 
## Create the customer threads   
for i in range(50):
    customer = Customers(i, random.choice(clientActionsList))
    c = threading.Thread(target=goToBank, args=(customer, bankLineQueue, waitForEnter))
    c.start()
    customerList.append(c) #Add to the list of customers

## Creating the teller threads
for i in range(3):
    teller = Tellers(i)
    t = threading.Thread(target=bankTransactions, args=(teller, waitForManager, waitForSafe, bankLineQueue))
    t.start()
    tellerList.append(t) #Add the to list of tellers

## CLOSING THE THREADS ##
#Close the customer threads
for custs in customerList:
    custs.join()

#Close the teller threads
for tells in tellerList:
    tells.join()

print("The line is empty, the bank is now closed")
