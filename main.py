from scrapedDataCleaner import ScrapedDataCleaner
from emailSender import send_email

def add_titles_and_changes_justified(titles, changes):
    message = ""

    longestTitleLength = len(max(titles, key=len))
    for title, change in zip(titles, changes):
        lengthOfTitle = len(title)
        defaultJustification = len(str(change)) + 2
        justification = defaultJustification + (longestTitleLength - lengthOfTitle)
        message += f"{title}{change : >{justification}}%\n"
    message += "\n"

    return message

def generate_message():
    cleaner = ScrapedDataCleaner()
    commodities = cleaner.get_commodity_list()
    indices = cleaner.get_indices()
    currencies = cleaner.get_currencies()
    crypto = cleaner.get_crypto_currencies()
    oneYearEtfs, threeYearEtfs = cleaner.get_etfs()

    #TODO: add date for today
    message = "Financial movements of today:\n"
    financialsOfInterest = {"Commodities": commodities, "Indices": indices, "Currencies": currencies,
                            "Crypto": crypto, "ETF 1-year changes": oneYearEtfs, "ETF 3-year changes": threeYearEtfs}

    for financial in financialsOfInterest:
        message += f"{financial}:\n"
        message += f"Top three {financial.lower()}:\n"
        numberOfValues = len(financialsOfInterest[financial])

        titlesTop = []
        changesTop = []
        for i in reversed(range(numberOfValues-3, numberOfValues)):
            title, change = financialsOfInterest[financial][i]
            titlesTop.append(title)
            changesTop.append(change)

        message += add_titles_and_changes_justified(titlesTop, changesTop)

        message += f"Bottom three {financial.lower()}:\n"
        titlesBottom = []
        changesBottom = []
        for i in range(3):
            title, change = financialsOfInterest[financial][i]
            titlesBottom.append(title)
            changesBottom.append(change)

        message += add_titles_and_changes_justified(titlesBottom, changesBottom)

    return message

if __name__ == "__main__":
    message = generate_message()
    send_email("Financials for today", message)

