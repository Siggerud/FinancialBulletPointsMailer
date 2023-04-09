import requests.exceptions
from scraper import Scraper
from threading import Thread
import os
import time

#TODO: make all lists unique
class ScrapedDataCleaner:
    def __init__(self):
        self._url = "https://markets.businessinsider.com/"
        self._numberOfProcessors = os.cpu_count()
        self._currencyChanges = []
        self._indicesChanges = []
        self._cryptoChanges = []
        self._oneYearEtfChanges = []
        self._threeYearEtfChanges = []

    def get_etfs(self):
        start = time.time()
        lastEtfPage = self._get_page_count("api/etf-ajax-search")
        threads = []
        for page in range(1, lastEtfPage+1):
            thread = Thread(target=self._get_etfs_threaded, args=(page,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print("ETF time: ", end - start)

        return sorted(self._oneYearEtfChanges, key=lambda x: x[1]), \
               sorted(self._threeYearEtfChanges, key=lambda x: x[1])

    def _get_etfs_threaded(self, page):
        subUrl = "api/etf-ajax-search?p="
        scraper = Scraper(self._url + subUrl + str(page))
        soup = scraper.get_soup()
        tbody = soup.find("tbody", class_="table__tbody")
        trTags = tbody.find_all("tr", class_="table__tr")
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            etf = tdTags[0].find("a").text
            try:
                oneYearChangeValue = tdTags[3].find("span").text
                try:
                    oneYearChange = float(oneYearChangeValue[:-1])
                except ValueError:
                    oneYearChange = float(oneYearChangeValue[:-1].replace(",", ""))
            except AttributeError:
                oneYearChange = None

            if oneYearChange:
                self._oneYearEtfChanges.append((etf, oneYearChange))

            try:
                threeYearChangeValue = tdTags[4].find("span").text
                try:
                    threeYearChange = float(threeYearChangeValue[:-1])
                except ValueError:
                    threeYearChange = float(threeYearChangeValue[:-1].replace(",", ""))
            except AttributeError:
                threeYearChange = None

            if threeYearChange:
                self._threeYearEtfChanges.append((etf, threeYearChange))

    def _get_page_count(self, subUrl):
        scraper = Scraper(self._url + subUrl)
        soup = scraper.get_soup()
        lastLiTag = soup.find_all("li", class_="pagination__item")[-1]
        pageCount = int(lastLiTag["data-pagination-page"])

        return pageCount

    def get_crypto_currencies(self):
        start = time.time()
        cryptoPageCountEuro = self._get_page_count("ajax/ExchangeRate_CryptoExchangeRatePriceList/1/2")
        cryptoPageCountDollar = self._get_page_count("ajax/ExchangeRate_CryptoExchangeRatePriceList/1/3")
        numberOfPages = cryptoPageCountEuro + cryptoPageCountDollar
        threads = []
        for pageCount in range(1, (numberOfPages+1)):
            if pageCount < cryptoPageCountEuro:
                page = pageCount
                currencyNum = "2"
            else:
                page = pageCount - cryptoPageCountEuro
                currencyNum = "3"

            thread = Thread(target=self._get_crypto_currencies_threaded, args=(currencyNum, page))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print("Crypto time: ", end - start)

        return sorted(self._cryptoChanges, key=lambda x: x[1])


    def _get_crypto_currencies_threaded(self, currencyNum, page):
        subUrl = "ajax/ExchangeRate_CryptoExchangeRatePriceList/"
        scraper = Scraper(self._url + f"{subUrl}{page}/{currencyNum}")
        soup = scraper.get_soup()
        tbody = soup.find("tbody", class_="table__tbody")
        trTags = tbody.find_all("tr", class_="table__tr")
        for trTag in trTags:
            tdTags = trTag.find_all("td", class_="table__td")
            aTag = tdTags[0].find("a")
            currencyRef = aTag["title"]
            crypto = aTag.text
            title = f"{crypto}/{currencyRef}"

            change = float(tdTags[3].find("span").text[:-1])
            self._cryptoChanges.append((title, change))

    def get_commodity_list(self):
        commodityChanges = []
        scraper = Scraper(self._url + "commodities")
        soup = scraper.get_soup()
        trTags = soup.find_all("tr", class_="table__tr")[5:] # skip first table
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            if tdTags:
                commodity = tdTags[0].find("a").text
                change = float(tdTags[2].find("span").text[:-1])
                commodityChanges.append((commodity, change))

        return sorted(list(set(commodityChanges)), key = lambda x: x[1])

    def get_currencies(self):
        start = time.time()
        currencies = ["USD", "EUR", "CHF", "JPY", "GBP"]
        threads = []
        for i in range(len(currencies)):
            currency = currencies[i]
            thread = Thread(target=self._get_currencies_threaded, args=(currency,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print("currency time: ", end-start)

        return sorted(self._currencyChanges, key=lambda x: x[1])

    def _get_currencies_threaded(self, currency):
        scraper = Scraper(self._url + "ajax/ExchangeRate_ListWithShortNameExcludes?currency=" + currency)
        soup = scraper.get_soup()
        tbody = soup.find("tbody")
        trTags = tbody.find_all("tr", class_="table__tr")
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            currencyPair = tdTags[0].text.strip()
            change = float(tdTags[4].text.strip())
            self._currencyChanges.append((currencyPair, change))

    def get_indices(self):
        start = time.time()
        markets = ["us-stock-markets", "latin-america-canadian-markets", "south-american-markets",
                   "european-stock-markets/western", "european-stock-markets/western",
                   "african-middle-eastern-stock-markets",
                   "asian-pacific-stock-markets"]
        threads = []
        for i in range(len(markets)):
            market = markets[i]
            thread = Thread(target=self._get_indices_threaded, args=(market,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print("Indices time: ", end - start)

        return sorted(list(set(self._indicesChanges)), key=lambda x: x[1])

    def _get_indices_threaded(self, market):
        scraper = Scraper(self._url + "ajax/IndexListTab/" + market)
        soup = scraper.get_soup()
        tbody = soup.find("tbody", class_="table__tbody")
        trTags = tbody.find_all("tr", class_="row-hover")
        for trTag in trTags:
            tdTags = trTag.find_all("td", class_="table__td")
            aTag = tdTags[0].find("a")
            index = aTag["title"]

            change = float(tdTags[2].find_all("span")[1].text[:-1])
            self._indicesChanges.append((index, change))






