# BankSim-Project2-CS4348
You will write a simulation of a certain bank. There are three tellers, and the bank opens
when all three are ready. No customers can enter the bank before it is open. Throughout
the day, customers will visit the bank to either make a withdraw or make a deposit. If there
is a free teller, a customer entering the bank can go to that teller to be served. Otherwise,
the customer must wait in line to be called. The customer will tell the teller what transition
to make. The teller must then go into the safe, for which only two tellers are allowed in
side at any one time. Additionally, if the customer wants to make a withdraw the teller
must get permission from the bank manager. Only one teller at a time can interact with
the manager. Once the transaction is complete the customer leaves the bank, and the teller
calls the next in line. Once all 50 customers have been served, and have left the bank, the
bank closes.
