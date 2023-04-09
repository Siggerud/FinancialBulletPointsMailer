from scrapedDataCleaner import ScrapedDataCleaner
from scraper import Scraper

cleaner = ScrapedDataCleaner()
#print(cleaner.get_currencies())
#print(cleaner.get_crypto_currencies())
oneYear, threeYear = cleaner.get_etfs()
print(oneYear)
print(threeYear)
