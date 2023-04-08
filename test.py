from scrapedDataCleaner import ScrapedDataCleaner
from scraper import Scraper

cleaner = ScrapedDataCleaner()
cryptos = cleaner.get_crypto_currencies()
print(cryptos)
print(len(cryptos))
