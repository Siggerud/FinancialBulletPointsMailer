from scrapedDataCleaner import ScrapedDataCleaner
from emailSender import send_email

cleaner = ScrapedDataCleaner()
commodities = cleaner.get_commodity_list()
indices = cleaner._get_indices_threaded()
currencies = cleaner._get_currencies_threaded()
crypto = cleaner._get_crypto_currencies_threaded()
oneYearEtfs, threeYearEtfs = cleaner.get_etfs()

message = ""
financialsOfInterest = {"commodoties": commodities, "indices": indices, "currencies": currencies,
                        "crypto": crypto, "Three year ETFs": threeYearEtfs, "One year ETFs": oneYearEtfs}

for financial in financialsOfInterest:
    message += f"Top three {financial}:\n"
    for i in range(3):
        message += financialsOfInterest[financial][i]

    print(message)

