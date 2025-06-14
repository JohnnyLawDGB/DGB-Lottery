# DigiByte Lottery

### Simple Python script for generating DigiByte addresses and checking them for balance on the blockchain.

# Update

Old scripts are outdated, I've updated a more efficient version that allows for a single call to check multiple addresses and a timeout to not get flagged as spam by the blockchain API, as well as the option to have the bot send a collision to your Telegram bot. Check the `DGB_Async_Test_Incremental.py` script for more info.

# Idea

As of 2021, there are many dormant DigiByte addresses with unspent balances, so these scripts are more or less like playing the lottery with an infinite amount of attempts.

Needless to say, you're more likely to throw random mechanical parts off a cliff and come down to a fully working car rather than finding a collision, but you're still free to try! 👀

# Scripts 

There are two main scripts, `DGB_Lottery_Create.py` will generate a random private key with matching public compressed and uncompressed key (They're two different wallet addresses) and test it against a public blockchain for any balance. (Slower script).

The second script `DGB_Lottery_From_List.py` will take in a list of dynamically generated private and public keys (In this case [cryptoguru](https://lbc.cryptoguru.org/dio/) and test every single wallet in that page for balance. HTTP requests are asynchronous, so consider adding a timeout to not get flagged as spam by the blockchain API. (Faster script)

The script `DGB_Lottery_Single_Page.py` is just for proof or testing lucky numbers. It works like the second one, but with a page number of your choice. This is useful to check that the script is working as intended, you could for example try page no. `412146261462724578030299224086806743063916127103968361179779786746970751006` and see the script catch a wallet with transactions on it.
The script `DGB_Lottery_Slot_GUI.py` provides a simple GUI with a slot-machine style animation while new DigiByte addresses are generated.

# First time run
 - Make sure you have Python 3 or higher installed and setup as OS PATH.
 - Run 'pip install -r -requirements.txt' on the same folder.
 - Run the script.
 - If any collision is found, a 'loot.txt' file will be created, containing the private key to access the wallet.
 - (OPTIONAL) Add your Telegram bot details in the commented section to get notified via message if a collision is found!


# Screenshots
`DGB_Lottery_Create.py`

![EuxImxg](https://user-images.githubusercontent.com/85108160/129419646-8f7527e8-6a35-44c9-a271-2266f22ead64.png)

`DGB_Lottery_From_List.py`

![2UI5LrW](https://user-images.githubusercontent.com/85108160/129419795-23519077-49cb-48fe-b2fc-5c0b627e7d91.png)

# Contribution
This is just a small project I had in mind so I'm sure it can be improved in many ways, I'm open to any suggestion!

