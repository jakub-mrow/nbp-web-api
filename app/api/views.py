from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Currencies
from api.serializers import CurrenciesSerializer

import api.converters as con

URL = "http://api.nbp.pl/api/exchangerates/rates/A/"

headers = {
    "Content-type": "application/json"
}

@api_view(['GET'])
def apiInformation(request):
    information = {
        "api/exchangerates": "POST",
        "api/history": "POST"
    }
    return Response(information)


@api_view(['POST'])
def getCurrenciesData(request):
    serializer = CurrenciesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    period = request.data["period"]
    sortingOrder = request.data["sortingOrder"]
    
    responseStructure = []
    for currency in request.data["currencies"]:
        currencyName = currency
        startDate, endDate = con.convertPeriod(period)
        parsedData = con.getIntervalInfo(URL, currencyName, [startDate, endDate])
        
        # catching date errors
        if "date-error" in parsedData:
            return Response(parsedData, status=400)
        
        responseStructure.append(parsedData)

    # sorting currencies by name ascending or descending
    if sortingOrder == "ascending":
        responseStructure = sorted(responseStructure, key = lambda c: c["currency"])
    elif sortingOrder == "descending":
        responseStructure = sorted(responseStructure, key = lambda c: c["currency"], reverse=True)

    return Response(responseStructure)

@api_view(['POST'])
def historyData(request):
    serializer = CurrenciesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    currencies = request.data["currencies"]
    period = request.data["period"]
    sortingOrder = request.data["sortingOrder"]
    startDate, endDate = con.convertPeriod(period)
    
    currenciesPeriodPrices = con.getHistoryData(currencies, startDate, endDate)
    historyDataResponse = con.createHistoryDataResponse(currenciesPeriodPrices)
    
    if sortingOrder == "ascending":
        responseStructure = sorted(historyDataResponse, key = lambda c: c["currency"])
    elif sortingOrder == "descending":
        responseStructure = sorted(historyDataResponse, key = lambda c: c["currency"], reverse=True)
    
    return Response(responseStructure)