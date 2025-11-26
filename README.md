# Current Entry Point - market_scan.py
1. Connect to Interactive Broker API Asychronously (Host IP, Port, and Client Id required)
2. Subscribe to a scanner (for now I scan Major US Stocks that opened with a gap upon market open, filtering above a certain market cap, price, volume, and change in pct)
3. Request an instance of the scanner data and take the top N amount (in my code I set it to 10)
4. For each entry in the scanner response, fetch the contract details and use it to fetch Historical Data.
5. From the Historical Data, calculate the open gap size and how long the stock continued to run upwards for.
6. Persist the resulting details to a pandas DataFrame and save as a pkl file.
   Note to self::Could we not create a db table?
7. Also log the resulting details on the console for logging and confirmation purposes.

# Next Stage in Data Pipeline - data_gateway.py
1. Python opens the saved pkl file and fetches every stock from the 'symbol' column.
   Note to self::If a db were intrdouces, this would be an SQL query.
2. Python then fetches historical data on each going back 10 years.
3. Each dataset fetched gets saved in its own csv file in a dedicated folder.
   Note to sef::Could the historical data not be added as a separate db? That way we could smoothly append on a scheduled basis.
Note: This file could be named in a way that better reflects its purpose, but when opening the file you will find unused functions, such as one for fetching realtime data and another for fetching historical data. I was thinking that this file could server as a general gateway dedicated solely to data persistence, irrespective of its nature.

# Statistical Analysis
## Historgrams, Vertical Scatter Plots, Power Analysis, Hypothesis Tests, Correlations, P-Values, and Benjamini-Hochberg Method
1. Python begins by ingesting the saved csvs one by one and deriving pct_change for closing prices and volumes.
  Note to self::Could step 1 not be moved to data_gateway? market_stats should only be consuming data.
2. It then plots a histogram for each - for both price returns and volume changes.
3. After that it produces a set of jittered 1d vertical scatterplotq for each stock with a mean for each.
4. Next steps will be to run combinations and permutations on every possible pair of stocks and determining which ones are different to the other when compared side by side.

## Contingency Tables, Bayes' Theorem, and Expected Values
In this section of the Statistical Analysis stack, the chosen project is on building a contingency table of earnings surprises and next day returns.
1. Fetch data with the following attributes: Ticker, Earnings Announcement Dates, Actual EPS, Consensus EPS, Next-day close prices.
2. Compute surprise: Surprise = (Actual - Consensus) / |Consensus|
3. Store Surprise numbers into categories:
    - Beat = Surprise > 0
    - Meet = Surprise == 0
    - Miss = Surprise < 0
    OR
    - Strong Beat: x > +3%
    - Mild Beat: 0% < x < +3%
    - Mild Miss: 0% > x > -3%
    - Strong Miss: x < -3%
4. Compute next-day return: (P(d+1) - P(d)) / P(d) and introduce binary classification:
    - Up if return > 0.1%
    - Down if return <= 0
    - Flat if return 0 < x <= 0.1%
5. Build contingency table between Beats and Misses and Up v Down. Frequencies for each combination.
6. Convert each frequency into conditional probabilities
7. Compute expected number of beats:
    -------------------------------------------------------------------
    (Probability of price going up given estimate beat * return if up)
    +
    (Probability of price going down given beat * return if down)
    -------------------------------------------------------------------
    (Probability of price going up given estimate miss * return if up)
    +
    (Probability of price going down given miss * return if down)
8. Conduct sanity checks:
    - Next trading day as opposed to nexy calendar day
    - If announcements is after hours, ensure that the next trading day is captured, not the one after
    - Ensure no duplicated announcements or missing EPS estimates
9. Stratification - build contingency tables by sectore, size, volatility, surprise, and pre-earnings drift (momentum effect)
