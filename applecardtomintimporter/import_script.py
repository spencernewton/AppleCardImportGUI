import csv
import datetime
import os
import random
import time
import urllib.parse
import urllib # makes it compatible with GUI
#import urlparse
import json

with open('changes.txt') as json_file:
    data = json.load(json_file)
    for p in data['changes']:
        cookie = p['cookie']
        token = p['token']
        csv_name = p['csv_name']

with open('perm.txt') as json_file:
    data = json.load(json_file)
    for p in data['permanent_vars']:
        account = p['account']
	tag1 = p['tag1']
	tag2 = p['tag2']
	tag3 = p['tag3']


# csv_name = 'import.csv' # name of csv you you want import to mint [string.csv]
verbose_output = 1 # should verbose messages be printed [0,1] 
uk_to_us = 0 # do you need to change dates from UK to US format [0,1]
min_wait = 0 # min wait time in seconds between requests, int[0-n]
max_wait = 2 # max wait time in seconds between requests, int[0-n]



#account = 'XXXXXXX' # grab from POST request form body in devtools
#tag1 = 'tagXXXXXX' # in form of tagXXXXXXX
#tag2 = 'tagXXXXXXX' # in form of tagXXXXXXX
#tag3 = 'tagXXXXXXX' # in form of tagXXXXXXX
#cookie = input("Copy and paste cookie here from POST request header in devtools:") # grab from POST request header in devtools
referrer = 'https://mint.intuit.com/transaction.event' # grab from POST request header in devtools
#token = input("Copy and paste token here from POST request form body in devtools:") # grab from POST request form body in devtools

csv_object = csv.reader(open(csv_name,'rU'))
next(csv_object)

for row in csv_object:

	# Initialize Variables
	date = (row[0])
	postDate = (row[1])
	merchant = (row[3])
	catName = (row[4])
	typeID = (row[5])
	amount = (float(row[6]))
	expense = 'true'
	curl_input = 'Error: Did not Generate'
	curl_output = 'Error: Did not run'

	# Convert Commonwealth to US Date System 
	if uk_to_us == 1: # based on setting
		dateconv = time.strptime(date,"%d/%m/%Y") # not needed for US to US
		date = (time.strftime("%m/%d/%Y",dateconv)) # converted new US date format from UK

	# Require "/" for date delimiter and HTTP Encode Character, supports "/", ".", "-"
	# We are not using url encode library here because we custom map other delimiters 
	dateoutput = date.replace("/", "%2F")
	dateoutput = date.replace(".", "%2F")
	dateoutput = date.replace("-", "%2F")


	#merchant = urllib.parse.quote(merchant)
	merchant = urllib.parse.quote(merchant)

	# Category ID Mapping Function 
	def category_id_switch(import_category):

		# Define mapping of import categories to : Mint Category IDs
		switcher={
			#Apple Card categories - incomplete
			'Gas':1401,
			'Food & Drink':7,
			'Grocery':701,
			'Restaurants':707,
			'Bills & Utilities':13,
			'Shopping':2,
			'Health & Wellness':5,
			'Personal':4,
			'Payment':2101,
			'Travel':15,
			'Entertainment':1,
			'Automotive':14,
			'Education':10,
			'Professional Services':17,
			'Home':12,
			'Fees & Adjustments':16,
			'Gifts & Donations':8,
			'Alcohol':708,
			'Credit':3003,
			'Medical':502,
			'Gift': 801,
			'Clothing': 201,
			# American Express Categories - Incomplete
			# American Express doesn't provide category information for payments, so I recommend manually changing those to "Payment"
			'Merchandise & Supplies-Groceries':701,
			'Transportation-Fuel':1401,
			'Fees & Adjustments-Fees & Adjustments':16,
			'Merchandise & Supplies-Wholesale Stores':2,
			'Restaurant-Restaurant':707,
			'Payment':2101,
			# The following categories are Mint categories. 
			# Citi does not included categories in downloaded transactions so I added my own categories using the Mint categories.
			# These mappings make sure those categories don't get mapped to 'uncategorized:20' when they aren't found in the mappings
			# for the other banks above.
			#
			# If you want to change a category mapping, be mindful that some category names may be repeated because Mint uses 
			# the same category name as another bank. 
			'Auto & Transport':14,
			'Auto Insurance':1405,
			'Auto Payment':1404,
			'Gas & Fuel':1401,
			'Parking':1402,
			'Public Transportation':1406,
			'Service & Parts':1403,
			'Bills & Utilities':13,
			'Home Phone':1302,
			'Internet':1303,
			'Mobile Phone':1304,
			'Television':1301,
			'Utilities':1306,
			'Business Services':17,
			'Advertising':1701,
			'Legal':1705,
			'Office Supplies':1702,
			'Printing':1703,
			'Shipping':1704,
			'Education':10,
			'Books & Supplies':1003,
			'Student Loan':1002,
			'Tuition':1001,
			'Entertainment':1,
			'Amusement':102,
			'Arts':101,
			'Movies & DVDs':104,
			'Music':103,
			'Newspapers & Magazines':105,
			'Fees & Charges':16,
			'ATM Fee':1605,
			'Bank Fee':1606,
			'Finance Charge':1604,
			'Late Fee':1602,
			'Service Fee':1601,
			'Trade Commissions':1607,
			'Financial':11,
			'Financial Advisor':1105,
			'Life Insurance':1102,
			'Food & Dining':7,
			'Alcohol & Bars':708,
			'Coffee Shops':704,
			'Fast Food':706,
			'Groceries':701,
			'Restaurants':707,
			'Gifts & Donations':8,
			'Charity':802,
			'Gift':801,
			'Health & Fitness':5,
			'Dentist':501,
			'Doctor':502,
			'Eyecare':503,
			'Gym':507,
			'Health Insurance':506,
			'Pharmacy':505,
			'Sports':508,
			'Home':12,
			'Furnishings':1201,
			'Home Improvement':1203,
			'Home Insurance':1206,
			'Home Services':1204,
			'Home Supplies':1208,
			'Lawn & Garden':1202,
			'Mortgage & Rent':1207,
			'Income':30,
			'Bonus':3004,
			'Interest Income':3005,
			'Paycheck':3001,
			'Reimbursement':3006,
			'Rental Income':3007,
			'Returned Purchase':3003,
			'Kids':6,
			'Allowance':610,
			'Baby Supplies':611,
			'Babysitter & Daycare':602,
			'Child Support':603,
			'Kids Activities':609,
			'Toys':606,
			'Misc Expenses':70,
			'Personal Care':4,
			'Hair':403,
			'Laundry':406,
			'Spa & Massage':404,
			'Pets':9,
			'Pet Food & Supplies':901,
			'Pet Grooming':902,
			'Veterinary':903,
			'Shopping':2,
			'Books':202,
			'Clothing':201,
			'Electronics & Software':204,
			'Hobbies':206,
			'Sporting Goods':207,
			'Taxes':19,
			'Federal Tax':1901,
			'Local Tax':1903,
			'Property Tax':1905,
			'Sales Tax':1904,
			'State Tax':1902,
			'Transfer':21,
			'Credit Card Payment':2101,
			'Transfer for Cash Spending':2102,
			'Travel':15,
			'Air Travel':1501,
			'Hotel':1502,
			'Rental Car & Taxi':1503,
			'Vacation':1504,
			'Uncategorized':20,
			'Cash & ATM':2001,
			'Check':2002,
			'Hide from Budgets & Trends':40,
		}
		# Get the mint category ID from the map 
		return switcher.get(import_category,20) # For all other unmapped cases return uncategorized category "20" 

	# Category NAME Mapping Function 
	def category_name_switch(mint_id):

		# Define mapping of import categories to : Mint Category IDs
		switcher={
			# All default mint categories are listed here. Your custom categories will not be here. If you have custome categories
			# you want to use, you'll need to add a mapping for them here and in the category_id_switch above.
			14:'Auto & Transport',
			1405:'Auto Insurance',
			1404:'Auto Payment',
			1401:'Gas & Fuel',
			1402:'Parking',
			1406:'Public Transportation',
			1403:'Service & Parts',
			13:'Bills & Utilities',
			1302:'Home Phone',
			1303:'Internet',
			1304:'Mobile Phone',
			1301:'Television',
			1306:'Utilities',
			17:'Business Services',
			1701:'Advertising',
			1705:'Legal',
			1702:'Office Supplies',
			1703:'Printing',
			1704:'Shipping',
			10:'Education',
			1003:'Books & Supplies',
			1002:'Student Loan',
			1001:'Tuition',
			1:'Entertainment',
			102:'Amusement',
			101:'Arts',
			104:'Movies & DVDs',
			103:'Music',
			105:'Newspapers & Magazines',
			16:'Fees & Charges',
			1605:'ATM Fee',
			1606:'Bank Fee',
			1604:'Finance Charge',
			1602:'Late Fee',
			1601:'Service Fee',
			1607:'Trade Commissions',
			11:'Financial',
			1105:'Financial Advisor',
			1102:'Life Insurance',
			7:'Food & Dining',
			708:'Alcohol & Bars',
			704:'Coffee Shops',
			706:'Fast Food',
			701:'Groceries',
			707:'Restaurants',
			8:'Gifts & Donations',
			802:'Charity',
			801:'Gift',
			5:'Health & Fitness',
			501:'Dentist',
			502:'Doctor',
			503:'Eyecare',
			507:'Gym',
			506:'Health Insurance',
			505:'Pharmacy',
			508:'Sports',
			12:'Home',
			1201:'Furnishings',
			1203:'Home Improvement',
			1206:'Home Insurance',
			1204:'Home Services',
			1208:'Home Supplies',
			1202:'Lawn & Garden',
			1207:'Mortgage & Rent',
			30:'Income',
			3004:'Bonus',
			3005:'Interest Income',
			3001:'Paycheck',
			3006:'Reimbursement',
			3007:'Rental Income',
			3003:'Returned Purchase',
			6:'Kids',
			610:'Allowance',
			611:'Baby Supplies',
			602:'Babysitter & Daycare',
			603:'Child Support',
			609:'Kids Activities',
			606:'Toys',
			70:'Misc Expenses',
			4:'Personal Care',
			403:'Hair',
			406:'Laundry',
			404:'Spa & Massage',
			9:'Pets',
			901:'Pet Food & Supplies',
			902:'Pet Grooming',
			903:'Veterinary',
			2:'Shopping',
			202:'Books',
			201:'Clothing',
			204:'Electronics & Software',
			206:'Hobbies',
			207:'Sporting Goods',
			19:'Taxes',
			1901:'Federal Tax',
			1903:'Local Tax',
			1905:'Property Tax',
			1904:'Sales Tax',
			1902:'State Tax',
			21:'Transfer',
			2101:'Credit Card Payment',
			2102:'Transfer for Cash Spending',
			15:'Travel',
			1501:'Air Travel',
			1502:'Hotel',
			1503:'Rental Car & Taxi',
			1504:'Vacation',
			20:'Uncategorized',
			2001:'Cash & ATM',
			2002:'Check',
			40:'Hide from Budgets & Trends',
		}
		# Get the mint category NAME from the map 
		return switcher.get(mint_id,'Uncategorized') # For all other unmapped cases return uncategorized category "20" 

	# typeID payment overrides all categories 
	if typeID == "Payment":
		catID = '2101' # Since I was importing credit cards I have mine set to credit card payment. If you are doing bank accounts you many want to change this to payment general

	# if type is NOT payment then do a category check 
	else:

		# if there IS no cat it is uncategorized 
		if len(catName) == 0: 
			catID = '20' # mint's uncategorized category

		# If there is a category check it against mapping	
		else :
			# Use a switch since there may be MANY category maps 
			catID = str(category_id_switch(catName))


	# Set mint category name by looking up name in ID map 
	category = catName
	#category = urllib.parse.quote(category)
	category = urllib.parse.quote(category)

	"""
	#################################
	Process Amount seeing if transaction is an expense or income.   
	#################################
	"""
	if amount > 0:
		expense = 'true' # when amount is less than 0 this is an expense, ie money left your account, ex like buying a sandwich. 					
	else:
		expense = 'false' # when amount is greater than 0 this is income, ie money went INTO your account, ex like a paycheck. 				
	amount = str(amount) # convert amount to string so it can be concatenated in POST request 


	# Break curl lines 
	curl_line = " "

	# fragment curl command 
	curl_command = "curl -i -s -k -X POST 'https://mint.intuit.com/updateTransaction.xevent'" + curl_line
	curl_host = "-H 'Host: mint.intuit.com'" + curl_line
	curl_user_agent = "-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'" + curl_line
	curl_accept = "-H 'Accept: */*'" + curl_line
	curl_accept_language = "-H 'Accept-Language: en-US,en;q=0.5'" + curl_line
	curl_compressed = "--compressed" + curl_line
	curl_x_requested_with = "-H 'X-Requested-With: XMLHttpRequest'" + curl_line
	curl_content_type = "-H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'" + curl_line
	curl_referer = "-H 'Referer: https://mint.intuit.com/transaction.event?accountId=" + referrer + "'" + curl_line
	curl_cookie = "-H 'Cookie: " + cookie + "'" + curl_line
	curl_connection = "-H 'Connection: close' " + curl_line
	curl_data =  "--data" + curl_line

	# Fragment the curl form data 	
	form_p1 = "'cashTxnType=on&mtCheckNo=&" + tag1 + "=0&" + tag2 + "=0&" + tag3 + "=0&"
	form_p2 = "task=txnadd&txnId=%3A0&mtType=cash&mtAccount=" + account + "&symbol=&note=&isInvestment=false&"
	form_p3 = "catId="+catID+"&category="+category+"&merchant="+merchant+"&date="+dateoutput+"&amount="+amount+"&mtIsExpense="+expense+"&mtCashSplitPref=2&"
	form_p4 = "token=" + token + "'"

	# Piece together curl form data 
	curl_form = form_p1 + form_p2 + form_p3 + form_p4

	# Combine all curl fragments together into an entire curl command 
	curl_input = curl_command + curl_host + curl_user_agent + curl_accept + curl_accept_language + curl_compressed + curl_x_requested_with + curl_content_type + curl_referer + curl_cookie + curl_connection + curl_data + curl_form

	"""
	#################################
	Submit CURL POST Request
	#################################
	"""
	curl_output = str(os.system(curl_input)) # use os sytem to run a curl request submitting the form post

	"""
	#################################
	Verbose Output for Debug
	#################################
	"""
	if verbose_output == 1:
		print ('Transaction Date:', dateoutput) # date of transaction
		print ('Merchant', merchant) # merchant Description 
		print ('Category ID:', catID) # category of transaction
		print ('Category Name:', category) # category of transaction
		print ('Amount:', amount) # amount being processed
		print ('Expense:', expense) # in amount expense
		print ('CURL Request:', curl_input) # what was sent to mint 
		print ('CURL Response:', curl_output) # what was returned from mint OR curl ERROR
		print ('\n\n==============\n') # new line break


	time.sleep(random.randint(min_wait, max_wait))
