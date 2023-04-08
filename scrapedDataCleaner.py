import requests.exceptions
from scraper import Scraper
import time
import os

#TODO: make everything faster by threading
class ScrapedDataCleaner:
    def __init__(self):
        self._url = "https://markets.businessinsider.com/"
        self._numberOfProcessors = os.cpu_count()

    def get_etfs(self):
        oneYearChanges = {}
        threeYearChanges = {}

        subUrl = "api/etf-ajax-search?p="

        count = 1
        endFound = False
        while True:
            if endFound:
                break

            scraper = Scraper(self._url + subUrl + str(count))
            try:
                soup = scraper.get_soup()
            except requests.exceptions.HTTPError:
                break
            tbody = soup.find("tbody", class_="table__tbody")
            trTags = tbody.find_all("tr", class_="table__tr")
            for trTag in trTags:
                tdTags = trTag.find_all("td")
                try:
                    title = tdTags[0].find("a").text
                except AttributeError:
                    if tdTags[0].find("div").text.strip() == "Your search did not return any results.":
                        endFound = True
                        break
                try:
                    oneYearChangeValue = tdTags[3].find("span").text
                    try:
                        oneYearChange = float(oneYearChangeValue[:-1])
                    except ValueError:
                        oneYearChange = float(oneYearChangeValue[:-1].replace(",", ""))
                except AttributeError:
                    oneYearChange = None

                if oneYearChange:
                    oneYearChanges[title] = oneYearChange

                try:
                    threeYearChangeValue = tdTags[4].find("span").text
                    try:
                        threeYearChange = float(threeYearChangeValue[:-1])
                    except ValueError:
                        threeYearChange = float(threeYearChangeValue[:-1].replace(",", ""))
                except AttributeError:
                    threeYearChange = None

                if threeYearChange:
                    threeYearChanges[title] = threeYearChange

            count += 1

        sortedOneYearChanges = self._sort_dict_by_value(oneYearChanges)
        sortedThreeYearChanges = self._sort_dict_by_value(threeYearChanges)

        return sortedOneYearChanges, sortedThreeYearChanges

    def get_crypto_currencies(self):
        start = time.time()
        cryptoChanges = {}
        subUrl = "ajax/ExchangeRate_CryptoExchangeRatePriceList/"

        for i in range(2, 4):
            count = 1
            while True:
                scraper = Scraper(self._url + f"{subUrl}{count}/{i}")
                try:
                    soup = scraper.get_soup()
                except requests.exceptions.HTTPError:
                    break

                tbody = soup.find("tbody", class_="table__tbody")
                trTags = tbody.find_all("tr", class_="table__tr")
                for trTag in trTags:
                    tdTags = trTag.find_all("td", class_="table__td")
                    aTag = tdTags[0].find("a")
                    currencyRef = aTag["title"]
                    crypto = aTag.text
                    title = f"{crypto}/{currencyRef}"

                    change = float(tdTags[3].find("span").text[:-1])
                    cryptoChanges[title] = change

                count += 1

        sortedCryptoChanges = self._sort_dict_by_value(cryptoChanges)
        end = time.time()
        print("Crypto time: ", end - start)

        return sortedCryptoChanges

    def get_commodity_list(self):
        commodityChanges = {}
        scraper = Scraper(self._url + "commodities")
        soup = scraper.get_soup()
        trTags = soup.find_all("tr", class_="table__tr")[5:] # skip first table
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            if tdTags:
                title = tdTags[0].find("a").text
                change = float(tdTags[2].find("span").text[:-1])
                commodityChanges[title] = change
        sortedCommodityChanges = self._sort_dict_by_value(commodityChanges)

        return sortedCommodityChanges

    def _sort_dict_by_value(self, unsortedDict):
        return sorted(unsortedDict.items(), key=lambda x: x[1])

    def get_currencies(self):
        #start = time.time()
        currencyChanges = {}
        currencies = ["USD", "EUR", "CHF", "JPY", "GBP"]
        for currency in currencies:
            scraper = Scraper(self._url + "ajax/ExchangeRate_ListWithShortNameExcludes?currency=" + currency)
            soup = scraper.get_soup()
            tbody = soup.find("tbody")
            trTags = tbody.find_all("tr", class_="table__tr")
            for trTag in trTags:
                tdTags = trTag.find_all("td")
                currencyPair = tdTags[0].text.strip()
                change = float(tdTags[4].text.strip())
                currencyChanges[currencyPair] = change

        sortedCurrencyChanges = self._sort_dict_by_value(currencyChanges)
        #end = time.time()
        #print(end-start)
        return sortedCurrencyChanges


    def get_indices(self):
        indicesChanges = {}
        subUrls = ["us-stock-markets", "latin-america-canadian-markets", "south-american-markets",
                   "european-stock-markets/western", "european-stock-markets/western", "african-middle-eastern-stock-markets",
                   "asian-pacific-stock-markets"]
        for subUrl in subUrls:
            scraper = Scraper(self._url + "ajax/IndexListTab/" + subUrl)
            soup = scraper.get_soup()
            tbody = soup.find("tbody", class_="table__tbody")
            trTags = tbody.find_all("tr", class_="row-hover")
            for trTag in trTags:
                tdTags = trTag.find_all("td", class_="table__td")
                aTag = tdTags[0].find("a")
                title = aTag["title"]

                change = float(tdTags[2].find_all("span")[1].text[:-1])
                indicesChanges[title] = change
        sortedIndicesChanges = self._sort_dict_by_value(indicesChanges)

        return sortedIndicesChanges







