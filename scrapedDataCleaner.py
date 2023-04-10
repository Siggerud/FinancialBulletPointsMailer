from scraper import Scraper
from threading import Thread

# write Readme
class ScrapedDataCleaner:
    # for retrieving and cleaning data from businessinsider.com
    def __init__(self):
        self._url = "https://markets.businessinsider.com/"
        self._currencyChanges = []
        self._indicesChanges = []
        self._cryptoChanges = []
        self._oneYearEtfChanges = []
        self._threeYearEtfChanges = []

    # starts several threads to retrieve all etf data
    def get_etfs(self):
        lastEtfPage = self._get_page_count("api/etf-ajax-search")
        threads = []
        for page in range(1, lastEtfPage+1):
            thread = Thread(target=self._get_etfs_threaded, args=(page,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # first expunge duplicates with set, transform back to list and then sort by
        # second element of each set in the list
        return sorted(list(set(self._oneYearEtfChanges)), key=lambda x: x[1]), \
               sorted(list(set(self._threeYearEtfChanges)), key=lambda x: x[1])

    # finds the etf and corresponding change in percent for given page
    def _get_etfs_threaded(self, page):
        subUrl = "api/etf-ajax-search?p="
        scraper = Scraper(self._url + subUrl + str(page))
        trTags = self._get_tr_tags(scraper, "table__tr")
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            etf = tdTags[0].find("a").text
            try:
                oneYearChangeValue = tdTags[3].find("span").text
                try:
                    oneYearChange = float(oneYearChangeValue[:-1])
                except ValueError:
                    oneYearChange = float(oneYearChangeValue[:-1].replace(",", ""))
            except AttributeError: # means no data exists for one year change in value
                oneYearChange = None

            if oneYearChange: # only include etf if there are corresponding values
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

    # find how many pages there are to scrape through at given URL
    def _get_page_count(self, subUrl):
        scraper = Scraper(self._url + subUrl)
        soup = scraper.get_soup()
        lastLiTag = soup.find_all("li", class_="pagination__item")[-1]
        pageCount = int(lastLiTag["data-pagination-page"])

        return pageCount

    # starts several threads to retrieve all cryptocurrency data
    def get_crypto_currencies(self):
        # there can be more pages for either EURO or USD, so we account for that
        cryptoPageCountEuro = self._get_page_count("ajax/ExchangeRate_CryptoExchangeRatePriceList/1/2")
        cryptoPageCountDollar = self._get_page_count("ajax/ExchangeRate_CryptoExchangeRatePriceList/1/3")
        numberOfPages = cryptoPageCountEuro + cryptoPageCountDollar
        threads = []
        for pageCount in range(1, (numberOfPages+1)):
            if pageCount < cryptoPageCountEuro:
                page = pageCount
                currencyNum = "2" # number corresponds to EURO
            else:
                page = pageCount - cryptoPageCountEuro # start new page count when looking at USD
                currencyNum = "3" # number corresponds to USD

            thread = Thread(target=self._get_crypto_currencies_threaded, args=(currencyNum, page))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return sorted(list(set(self._cryptoChanges)), key=lambda x: x[1])

    # finds the cryptocurrency and corresponding change in percent for given page
    def _get_crypto_currencies_threaded(self, currencyNum, page):
        subUrl = "ajax/ExchangeRate_CryptoExchangeRatePriceList/"
        scraper = Scraper(self._url + f"{subUrl}{page}/{currencyNum}")
        trTags = self._get_tr_tags(scraper, "table__tr")
        for trTag in trTags:
            tdTags = trTag.find_all("td", class_="table__td")
            currencyRef, aTag = self._get_atag_title(tdTags)
            crypto = aTag.text
            title = f"{crypto}/{currencyRef}"

            change = float(tdTags[3].find("span").text[:-1])
            self._cryptoChanges.append((title, change))

    # finds the commodity and corresponding change in percent
    def get_commodities(self):
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

    # starts several threads to retrieve all currency data
    def get_currencies(self):
        currencies = ["USD", "EUR", "CHF", "JPY", "GBP"] # all currency tables found on page
        threads = []
        for i in range(len(currencies)):
            currency = currencies[i]
            thread = Thread(target=self._get_currencies_threaded, args=(currency,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return sorted(list(set(self._currencyChanges)), key=lambda x: x[1])

    # finds the currency and corresponding change in percent for given page
    def _get_currencies_threaded(self, currency):
        scraper = Scraper(self._url + "ajax/ExchangeRate_ListWithShortNameExcludes?currency=" + currency)
        trTags = self._get_tr_tags(scraper, "table__tr")
        for trTag in trTags:
            tdTags = trTag.find_all("td")
            currencyPair = tdTags[0].text.strip()
            change = float(tdTags[4].text.strip())
            self._currencyChanges.append((currencyPair, change))

    # starts several threads to retrieve all market index data
    def get_indices(self):
        markets = ["us-stock-markets", "latin-america-canadian-markets", "south-american-markets",
                   "european-stock-markets/western", "european-stock-markets/western",
                   "african-middle-eastern-stock-markets",
                   "asian-pacific-stock-markets"] # all markets found on page
        threads = []
        for i in range(len(markets)):
            market = markets[i]
            thread = Thread(target=self._get_indices_threaded, args=(market,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return sorted(list(set(self._indicesChanges)), key=lambda x: x[1])

    # finds the index and corresponding change in percent for given page
    def _get_indices_threaded(self, market):
        scraper = Scraper(self._url + "ajax/IndexListTab/" + market)
        trTags = self._get_tr_tags(scraper, "row-hover")
        for trTag in trTags:
            tdTags = trTag.find_all("td", class_="table__td")
            index = self._get_atag_title(tdTags)[0]

            change = float(tdTags[2].find_all("span")[1].text[:-1])
            self._indicesChanges.append((index, change))

    # retrieves tr tags
    def _get_tr_tags(self, scraper, trClass):
        soup = scraper.get_soup()
        tbody = soup.find("tbody")
        trTags = tbody.find_all("tr", class_=trClass)

        return trTags

    # retrieves title element of type a tag
    def _get_atag_title(self, tdTags):
        aTag = tdTags[0].find("a")
        title = aTag["title"]

        return title, aTag





