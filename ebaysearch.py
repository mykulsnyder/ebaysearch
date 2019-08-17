#!/usr/local/bin/python3

import ebaysdk
import csv
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from bs4 import BeautifulSoup

#Define function to determine Paypal Fees
def paypal_fee(x):
    j = round((x * 0.029) + .3,2)
    return j


#Initial Lists
matrix = []
matrix_val = []
priceList = []

#Initial User Input Variables.
#Matrix_Det determines a custom or csv search
#Condition converts the user input to lower case and capitalizes
matrix_det = str.lower(input('CSV or Custom'))
condition = str.lower(input('New (1000)/Used (3000)/For Parts (7000)')).title()

# If statement to create a custom matrix for manual search.
cont = ' y'
if matrix_det == ' custom':
    while cont == ' y':
        matrix.append(input('Insert Item'))
        cont = str.lower(input('Continue y/n'))

# If statement to create a matrix from the csv.
if matrix_det == ' csv':
    with open('ebaycsv.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)

        for line in csv_reader:
            matrix.append(line[0])

#Create loop to run through the csv file list
for j in matrix:
    sum = 0
    price = 0
    priceList = []

    #Ebay Call Api.
    try:
        keywords = str.lower(j)
        api = finding(appid='SamSnyde-csvfindi-PRD-cd8d7989f-a6d2000a', config_file=None)
        api.execute('findCompletedItems', {
            'keywords':keywords,
            'itemFilter': [
                {'name': 'Condition', 'value': condition},
                {'name': 'SoldItemsOnly', 'value': True},
            ],
            'sortBy': 'EndTimeSoonest',
            'paginationInput': {
                'entriesPerPage': 15,
                'pageNumber': 1
            },
        })

        response = api.response

        numberofentries = int(response.reply.searchResult._count)

        #Determine if any results were found
        if numberofentries == 0:
            priceList.append(price)

        else:

            for item in response.reply.searchResult.item:
                price = item.sellingStatus.currentPrice.value
                price = round(float(price),2)
                priceList.append(price)

            if len(priceList) >= 4:
                priceList.remove(max(priceList))
                priceList.remove(min(priceList)); priceList.remove(min(priceList))

        for value in priceList:
            sum = value + sum

        avg = round(sum / len(priceList),2)
        pypl_fee = paypal_fee(avg)
        ebay_fee = round(avg * .1,2)
        net = round(avg - pypl_fee - ebay_fee,2)
        matrix_val.append(net)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

sum = 0

for j in matrix_val:
    sum = round(j + sum,2)

print(matrix_val)
print('$',sum)
