import requests
import datetime

# given date format from reqeust this function returns starting and ending date in format YYYY-MM-DD
def convertPeriod(date):
    inputStartDate = date[0].split(".")
    inputEndDate = date[1].split(".")
    outputStartDate = "-".join([inputStartDate[2], inputStartDate[1], inputStartDate[0]])
    outputEndDate = "-".join([inputEndDate[2], inputEndDate[1], inputEndDate[0]])
    return [outputStartDate, outputEndDate]


def getIntervalInfo(URL, currencyName, dateInterval):
    headers = {
        "Content-type": "application/json"
    }
    minPrice = 99999999
    maxPrice = 0
    
    dateCorrectness = checkDate(dateInterval)
    if dateCorrectness == False:
        return {"date-error": "Invalid interval date or exceeded 367 days!"}
    
    try:
        intervalResponse = requests.get(URL+f"/{currencyName}/{dateInterval[0]}/{dateInterval[1]}", headers=headers)
        code = int(intervalResponse.status_code)
        if code == 200:
            intervalResponseData = intervalResponse.json()["rates"]
        
            # getting starting and ending price of currency in given interval
            intervalLength = len(intervalResponseData)
            startPrice = float(intervalResponseData[0]["mid"])
            endPrice = float(intervalResponseData[intervalLength - 1]["mid"])
            
            for dayInfo in intervalResponseData:
                price = float(dayInfo["mid"])
                
                if price > maxPrice:
                    maxPrice = price
                if price < minPrice:
                    minPrice = price
            
            # calculate price differences 
            priceDifference = endPrice - startPrice
            priceDifferencePercentage = ((endPrice - startPrice) / startPrice) * 100
            minMaxDifference = maxPrice - minPrice
            minMaxDifferencePercentage = (maxPrice - minPrice) / maxPrice * 100
            
            parsedData = {
                    "currency": currencyName,
                    "maxPrice": maxPrice, 
                    "minPrice": minPrice, 
                    "intervalPriceDifference": priceDifference,
                    "intervalPriceDifferencePercentage": priceDifferencePercentage,
                    "minMaxDifference": minMaxDifference,
                    "minMaxDifferencePercentage": minMaxDifferencePercentage
                    }
            return parsedData
        else:
            # catching errors in currency name
            return { "currency": currencyName, "request-error": "Wrong data format!"}      
        
    except requests.exceptions.RequestException as error:
        return {"request-error": error}
    
# function to check if given date is between today's date and starting date
# returns true if both of the dates in interval are correct, false otherwise
def checkDate(dateList):
    for date in dateList:
        year, month, day = [int(x) for x in date.split("-")]
        if datetime.datetime(year=2002, month=1, day=2) < datetime.datetime(year=year, month=month, day=day) < datetime.datetime.now():
            continue
        else:
            return False
    
    # checking if dates in interval are between 367 days
    year1, month1, day1 = [int(x) for x in dateList[0].split("-")]
    year2, month2, day2 = [int(x) for x in dateList[1].split("-")]
    if not((datetime.date(year2, month2, day2) - datetime.date(year1, month1, day1)).days < 367):
        return False
    return True