import requests
from bs4 import BeautifulSoup
import re
def exchange(amount, currency1, currency2):
	URL = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
	resp = requests.get(URL)
	data = resp.text
	soup = BeautifulSoup(data,"html.parser")
	matchValues = soup.find_all('span', class_='rate')
	realValueList = []
	for i in matchValues:
		realValue=i.get_text()
		realValueList.append(realValue)
	matchCurrency = soup.find_all('td',class_="currency")
	currencyList = []
	for j in matchCurrency:
		realCurrency=j.get_text()
		currencyList.append(realCurrency)
	exchangeRateDict = {}
	length = len(currencyList)
	for i in range(length):
		exchangeRateDict[currencyList[i]] = float(realValueList[i])
	exchangeRateDict['EUR'] = 1.0000
	exchange1 = exchangeRateDict[currency1]
	exchange2 = exchangeRateDict[currency2]
	exchangeValue = amount/exchange1*exchange2
	exchangeValue = round(exchangeValue,2)
	return exchangeValue


def parse_HTML(websiteList):
	aDict = {}
	for website in websiteList:
		country = website.split('.')
		country = country[0]
		with open(website,encoding = "utf-8") as file:
			soup = BeautifulSoup(file,"html.parser")
			matchPrice = soup.find_all('div',class_="search-result")
			priceList = []
			valueList = []
			for element in matchPrice:
				subtag = element.find('a',class_='search-result-info')
				subSubTag = subtag.find('div', class_='search-result-label-primary price-native')
				span = subSubTag.find('span').find('span').text
				actualValue = span.replace(',','')
				currency = re.findall(r'[a-zA-Z]{3}',subSubTag.text)
				realCurrency = currency[0]
				sizeSubTag = subtag.find('div',class_='size')
				if sizeSubTag == None:
					sqft = float(0)
				else:
					sqft = re.findall(r'[0-9]+[,]?[0-9]*[,]?[0-9]*',sizeSubTag.text)
					sqft = sqft[0]
					sqft = sqft.replace(',','')
					sqft = float(sqft)
				valueList.append((float(actualValue),realCurrency,sqft))
			aDict[country] = valueList
	return aDict

def most_expensive_home(aDict):
	aTup =('',0.0)
	for country in aDict.keys():
		listCountryValues = aDict[country]
		cost = 0.0
		for element in listCountryValues:
			value = element[0]
			currency1 = element[1]
			currency2 = 'USD'
			cost = exchange(value,currency1,currency2)
			if cost > aTup[1]:
				aTup = (country,cost)
	print(aTup)
def highest_avg_price(aDict,currency):
	avgList = []
	for country in aDict.keys():
		listCountryValues = aDict[country]
		cost = 0.0
		for element in listCountryValues:
			value = element[0]
			currency1 = element[1]
			cost += exchange(value,currency1,currency)
		length = len(listCountryValues)
		averageValue = cost/length
		subList = [country,averageValue]
		avgList.append(subList)
	sortedList = sorted(avgList, key = lambda x:x[1],reverse = True)
	highList = sortedList[0]
	aTup = (highList[0],round(highList[1],2))
	return aTup

def ideal_homes(aDict,currency):
	idealList = []
	for country in aDict.keys():
		listCountryValues = aDict[country]
		
		for element in listCountryValues:
			elementList = []
			value = element[0]
			currency1 = element[1]
			price = exchange(value,currency1,currency)
			sqft = element[2]
			if sqft != 0:
				pps = sqft/price
			else:
				pps = 0
			pps = round(pps,10)
			elementList.append(country)
			elementList.append(price)
			elementList.append(sqft)
			elementList.append(pps)
			idealList.append(elementList)
	idealList.sort(key = lambda x:x[3], reverse = True)
	length = 5
	topFiveList = []
	for i in range(length):
		subList = idealList[i]
		subList.pop()
		topFiveList.append(subList)
	finalList = []
	for sub in topFiveList:
		subTup = tuple(sub)
		finalList.append(subTup)
	return finalList

def big_baller_homes(aDict,desired_countries,budget,currency):
	sortedList = []
	purchasedList = []
	for country in desired_countries:
		if country == 'japan' or country == 'turkey' or country == 'south_africa' or country == 'portugal' or country == 'israel':
			valueList = aDict[country];
			for house in valueList:
				houseList = []
				value = house[0]
				currency1 = house[1]
				price = exchange(value,currency1,currency)
				sqft = house[2]
				houseList.append(country)
				houseList.append(price)
				houseList.append(sqft)
				sortedList.append(houseList)
	sortedList.sort(key = lambda x:x[1], reverse = True)
	money = budget
	for home in sortedList:
		costOfHome = home[1]
		if costOfHome <= money:
			money = money - costOfHome
			tupHome = tuple(home)
			purchasedList.append(tupHome)
	finalMoney = round(money,2)
	finalTup = (purchasedList,finalMoney)
	return finalTup





'''
dic = parse_HTML(['turkey.html','japan.html','south_africa.html'])

big_baller_homes(dic,['japan','south_africa'],7500000,'GBP')
'''
