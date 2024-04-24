
# Freyja Feeney
# CS2660 Cybersecurity Principles
# Lab 7.0 Blockchain

import miner 
import hashlib

# global variables
# genesis block hash from miner.py
prev_block_hash = '35bc0983b2a7907d1ce3da3c1163f23aa927bf7ed959606fbc55c4e04432224e'
# block id for block counting
block_id = 0

# menu! prints menu options and validates user input. calls appropriate functions 
def menu():
    print("Welcome to CatCoin!\n")
    print("Please select from the following options:")
    choice = input("\t1. Check Wallet Balance\n\t2. Transfer CatCoins\n\t3. Quit CatCoin\n")
    # validate input
    while not choice.isdigit() or int(choice) not in [1, 2, 3]:
        print("Not a valid choice. Enter a valid number.")
        choice = input("\t1. Check Wallet Balance\n\t2. Transfer CatCoins\n\t3. Quit CatCoin\n")
    # call the right functions!
    if int(choice) == 1:
        balance_check()
    if int(choice) == 2:
        transfer()
    if int(choice) == 3:
        # confirmation message for quitting
        sure = input("Are you sure you want to exit CatCoin? Y or N: ")
        if sure.lower() in ['y', 'yes']:
            quit()
        else:
            menu()

# check the balance of each wallet! accesses text files for each wallet and updates them appropriately
def balance_check():
    # lots of file validation!
    # open the wallet files to read in the current balance
    try:
        with open("wallet_1_balance.txt", "r") as file:
            wallet_1_bal = file.readline()
    except FileNotFoundError:
        print("There was an error opening the wallet 1 file. Please make sure you have downloaded it correctly.")
        menu()
    try:
        with open("wallet_2_balance.txt", "r") as file:
            wallet_2_bal = file.readline()
    except FileNotFoundError:
        print("There was an error opening the wallet 2 file. Please make sure you have downloaded it correctly.")
        menu()
    try:       
        with open("wallet_3_balance.txt", "r") as file:
            wallet_3_bal = file.readline()
    except FileNotFoundError:
        print("There was an error opening the wallet 3 file. Please make sure you have downloaded it correctly.")
        menu()

    # choose your wallet
    wallet = input("Choose your wallet:\n\t1. Wallet 1\n\t2. Wallet 2\n\t3. Wallet 3\n\t4. Return to menu\n")
    # input validation for wallet choice
    while not wallet.isdigit() or int(wallet) not in [1, 2, 3, 4]:
        print("Please choose a valid option")
        wallet = input("Choose your wallet:\n\t1. Wallet 1\n\t2. Wallet 2\n\t3. Wallet 3\n\t4. Return to menu\n")
    wallet = int(wallet)
    # check wallet balances 
    if wallet == 1:
        print("Balance: " + str(wallet_1_bal))
        balance_check()
    if wallet == 2:
        print("Balance: " + str(wallet_2_bal))
        balance_check()
    if wallet == 3:
        print("Balance: " + str(wallet_3_bal))
        balance_check()
    # return to menu
    if wallet == 4:
        menu()

# transfer transfers catcoins from wallet to wallet. deducts from wallet file and adds to other
# calls mining function post successful transfer
# creates block and adds it to block text file
def transfer():
    global prev_block_hash
    global block_id
    # choose the source waller
    source = input("From which wallet would you like to transfer?: ")
    #input validation
    while not source.isdigit() or int(source) not in [1, 2, 3]:
        print("Please choose a valid option")
        source = input("From which wallet would you like to transfer?: ")

    # choose the destination wallet
    destination = input("And to where would you like to transfer these coins?: ")
    #input validation
    while not destination.isdigit() or int(destination) not in [1, 2, 3]:
        print("Please choose a valid option")
        destination = input("From which wallet would you like to transfer?: ")
    # choose the amount you want to transfer
    while True:
        try:
            amount = int(input("How much?: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # transfer confirmation  
    sure = input("Are you sure you want to transfer " + str(amount) + " coins to Wallet " + str(destination) + "?: ")
    while sure.lower() not in ["y", "yes", "n", "no"]:
        sure = input("Please choose a valid option: Yes or No: ")
    if sure.lower() in ["y", "yes"]:
        # remove amount from source wallet file
        try:
            with open("wallet_" + str(source) + "_balance.txt", "r") as file:
                bal = int(file.readline())
            if bal >= amount:
                bal -= amount
                with open("wallet_" + str(source) + "_balance.txt", "w") as file:   
                    file.write(str(bal))
                    # add amount to destination wallet file
                with open("wallet_" + str(destination) + "_balance.txt", "r") as file:
                    bal_2 = int(file.readline())
                bal_2 += amount
                with open("wallet_" + str(destination) + "_balance.txt", "w") as file:   
                    file.write(str(bal_2))
            else:
                print("Insufficient funds. Try again another time.\n\n")
                menu()
        except FileNotFoundError:
            print("Invalid file.")
            menu()

        # create block id .. counts number of blocks
        block_id += 1
        #transaction complete
        print("Transaction Complete.\n")
        #call mining from miner.py with the previous block hash
        n, t = miner.mining(prev_block_hash)

        #create block dictionary to store info
        block = {
            "block_id" : block_id,
            "previous_block_hash": prev_block_hash,
            "timestamp" : t,
            "nonce": n,
            "from_wallet": source,
            "to_wallet": destination,
            "amount" : amount
        }

        # hash block data
        block_data = f"{block['from_wallet']}:{block['to_wallet']}:{block['amount']}"
        hash_of_block_data = hashlib.sha256(block_data.encode('utf-8')).hexdigest()
        
        # hash the header of the block for the next block
        # got 'utf-8' from miner.py
        current_hash_header = f"{block['block_id']}:{str(prev_block_hash)}:{block['timestamp']}:{block['nonce']}:{(hash_of_block_data)}"
        hashed_header = hashlib.sha256(current_hash_header.encode('utf-8')).hexdigest()
        #write block to blocks.txt file
        try:
            with open("blocks.txt", 'a') as f:
                f.write("block_id : " + str(block_id) + "\n")
                f.write("previous_block_hash : " + str(prev_block_hash) + "\n")
                f.write("timestamp : " + str(t) + "\n")
                f.write("nonce : " + str(n) + "\n")
                f.write("hash of block data : " + str(hash_of_block_data) + "\n")
                f.write("block_data:\n")
                f.write("\tfrom_wallet : " + str(source) + "\n")
                f.write("\tto_wallet : " + str(destination) + "\n")
                f.write("\tamount : " + str(amount) + "\n")
        except FileNotFoundError:
            print("blocks.txt not found! Returning you to menu...")
            menu()
        #set the hash header to the previous block hashed header for next block
        prev_block_hash = hashed_header
        menu()
    else:
        print("Returning you to menu..")
        menu()

menu()
