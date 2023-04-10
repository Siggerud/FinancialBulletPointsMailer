
# FinancialBulletPointsMailer
This program will send you a mail about the current financial data found at https://markets.businessinsider.com/. I would suggest scheduling this program to run once 
a day if you are interested.

#### How to:

1. Download all files to a folder

2. In the same folder add a .env file

3. **Optional:** Create a new email for sending the emails if you do not have an extra mail

4. To this .env file add the following
```python
SENDER_ADRESS="your.sender.email@yahoo.com"
SENDER_PASSWORD="yourPassword"
RECEIVER="your.receiver.email@aol.com"
```

5. Set the program to run once a day in your scheduling assistant

The mail will look something like the text below

---
Financial movements of monday 10/04/2023:

Commodities:<br>
Top five commodities:<br>
Sugar          3.01%<br>
Coffee         2.25%<br>
Rapeseed       1.99%<br>
Live Cattle    1.77%<br>
Feeder Cattle  1.45%<br>

Bottom five commodities:<br>
Coal          -6.9%<br>
Orange Juice  -4.26%<br>
Zinc          -1.83%<br>
Nickel        -1.01%<br>
Wheat         -0.99%<br>

Indices:<br>
Top five indices:<br>
DAXsubsector Real Estate (Kurs)             4.88%<br>
DAXsubsector Real Estate (Perf.)            4.88%<br>
VIX                                         4.84%<br>
DAXsubsector Diversified Financial (Perf.)  4.46%<br>
DAXsubsector Diversified Financial (Kurs)   4.46%<br>

Bottom five indices:<br>
Crude Oil VIX                                    -11.19%<br>
AMEX Biotechnology Index Final Settlement Value  -5.78%<br>
Russel 2000 VIX                                  -4.5%<br>
VDAX-NEW 1M                                      -3.93%<br>
VDAX-NEW 2M                                      -3.39%<br>

Currencies:<br>
Top five currencies:<br>
GBP/NLG  50.11%<br>
USD/NLG  50.08%<br>
EUR/NLG  50.0%<br>
JPY/NLG  49.84%<br>
CHF/NLG  49.83%<br>

Bottom five currencies:<br>
JPY/BITB  -72.49%<br>
CHF/BITB  -72.49%<br>
EUR/BITB  -72.46%<br>
USD/BITB  -72.45%<br>
GBP/BITB  -72.44%<br>

Crypto:<br>
Top five crypto:<br>
Bean Cash/Euro       263.39%<br>
Bean Cash/US-Dollar  262.37%<br>
ReddCoin/US-Dollar   84.34%<br>
Viacoin/US-Dollar    81.2%<br>
SeChain/US-Dollar    65.49%<br>

Bottom five crypto:<br>
Neutrino USD/US-Dollar  -53.23%<br>
SafeMoon/Euro           -40.72%<br>
SafeMoon/US-Dollar      -35.55%<br>
Dev Protocol/US-Dollar  -34.73%<br>
Dev Protocol/Euro       -34.66%<br>

ETF 1-year changes:<br>
Top five etf 1-year changes:<br>
ProShares UltraShort Bloomberg Natural Gas            64.75%<br>
Direxion Daily Real Estate Bear 3X Shares             55.81%<br>
iShares MSCI Turkey ETF                               55.21%<br>
DB Base Metals Double Short ETN                       53.12%<br>
BetaPro Natural Gas Inverse Leveraged Daily Bear ETF  51.68%<br>

Bottom five etf 1-year changes:<br>
VelocityShares 3x Long Natural Gas ETN Linked to the S&P GSCI® Natural Gas Index ER  -99.76%<br>
ProShares Ultra Bloomberg Natural Gas                                                -95.64%<br>
Osprey Solana Trust                                                                  -82.19%<br>
2x Long VIX Futures ETF                                                              -81.55%<br>
VelocityShares Daily 2x VIX Short-Term ETN                                           -80.49%<br>

ETF 3-year changes:<br>
Top five etf 3-year changes:<br>
VanEck Oil Services ETF                             5806.49%<br>
Grayscale Ethereum Trust (ETH)                      819.29%<br>
VanEck Rare Earth/Strategic Metals ETF              739.36%<br>
VanEck Energy Income ETF                            628.16%<br>
MicroSectors™ U.S. Big Oil Index 3X Leveraged ETNs  545.76%<br>

Bottom five etf 3-year changes:<br>
VelocityShares Daily 2x VIX Short-Term ETN                                           -99.92%<br>
MicroSectors™ U.S. Big Oil Index -3X Inverse Leveraged ETNs                          -99.9%<br>
VelocityShares 3x Long Natural Gas ETN Linked to the S&P GSCI® Natural Gas Index ER  -99.86%<br>
iShares MSCI Russia ETF                                                              -99.76%<br>
ProShares Ultra VIX Short-Term Futures ETF                                           -99.14%

---

