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

# Statistical Analysis - market_stats.py
1. Python begins by ingesting the saved csvs one by one and deriving pct_change for closing prices and volumes.
  Note to self::Could step 1 not be moved to data_gateway? market_stats should only be consuming data.
2. It then plots a histogram for each - for both price returns and volume changes.
3. After that it produces a set of jittered 1d vertical scatterplotq for each stock with a mean for each.
4. Next steps will be to run combinations and permutations on every possible pair of stocks and determining which ones are different to the other when compared side by side.
