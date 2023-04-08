from scrapedDataCleaner import ScrapedDataCleaner
from scraper import Scraper

cleaner = ScrapedDataCleaner()
#print(cleaner.get_currencies())
#print(cleaner.get_indices())
cryptos = cleaner.get_crypto_currencies()
print(cryptos)
print(len(cryptos))
