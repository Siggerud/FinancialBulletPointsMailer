from scrapedDataCleaner import ScrapedDataCleaner
from emailSender import send_email

cleaner = ScrapedDataCleaner()
commodities = cleaner.get_commodity_list()
indices = cleaner.get_indices()
currencies = cleaner.get_currencies()
crypto = cleaner.get_crypto_currencies()
oneYearEtfs, threeYearEtfs = cleaner.get_etfs()

message = ""
financialsOfInterest = {"commodoties": commodities, "indices": indices, "currencies": currencies,
                        "crypto": crypto, "Three year ETFs": threeYearEtfs, "One year ETFs": oneYearEtfs}

for financial in financialsOfInterest:
    message += f"Top three {financial}:\n"
    for i in range(3):
        message += financialsOfInterest[financial][i]

    print(message)

