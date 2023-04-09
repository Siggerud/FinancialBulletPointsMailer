from scrapedDataCleaner import ScrapedDataCleaner
from scraper import Scraper

cleaner = ScrapedDataCleaner()
<<<<<<< HEAD
cryptos = cleaner.get_crypto_currencies()
print(cryptos)
print(len(cryptos))

#print(cleaner.get_currencies())
#print(cleaner.get_crypto_currencies())
oneYear, threeYear = cleaner.get_etfs()
print(oneYear)
print(threeYear)

