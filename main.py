# main program for sending email with financial movements of the day

from scrapedDataCleaner import ScrapedDataCleaner
from emailSender import send_email
from datetime import datetime

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

def get_title_and_change_lists(interval, financialsOfInterest, financial):
    titles = []
    changes = []
    for i in interval:
        title, change = financialsOfInterest[financial][i]
        titles.append(title)
        changes.append(change)

    return titles, changes

def generate_message(date, weekday):
    cleaner = ScrapedDataCleaner()
    commodities = cleaner.get_commodities()
    indices = cleaner.get_indices()
    currencies = cleaner.get_currencies()
    crypto = cleaner.get_crypto_currencies()
    oneYearEtfs, threeYearEtfs = cleaner.get_etfs()

    message = f"Financial movements of {weekday.lower()} {date}:\n\n"
    financialsOfInterest = {"Commodities": commodities, "Indices": indices, "Currencies": currencies,
                            "Crypto": crypto, "ETF 1-year changes": oneYearEtfs, "ETF 3-year changes": threeYearEtfs}

    for financial in financialsOfInterest:
        message += f"{financial}:\n"
        # add the five best performers
        message += f"Top five {financial.lower()}:\n"
        numberOfValues = len(financialsOfInterest[financial])
        topInterval = reversed(range(numberOfValues-5, numberOfValues)) # the last five values of the list
        titlesTop, changesTop = get_title_and_change_lists(topInterval, financialsOfInterest, financial)

        message += add_titles_and_changes_justified(titlesTop, changesTop)

        # add the five worst performers
        message += f"Bottom five {financial.lower()}:\n"
        bottomInterval = range(5)
        titlesBottom, changesBottom = get_title_and_change_lists(bottomInterval, financialsOfInterest, financial)

        message += add_titles_and_changes_justified(titlesBottom, changesBottom)

    return message

if __name__ == "__main__":
    now = datetime.now()
    todayDate = now.strftime("%d/%m/%Y")
    weekDay = now.strftime("%A")
    message = generate_message(todayDate, weekDay)
    subject = f"Financials for {weekDay.lower()} {todayDate}"
    send_email(subject, message)

