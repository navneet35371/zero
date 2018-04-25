# zerodha assignment [*demo*](https://afternoon-oasis-67555.herokuapp.com/)

BSE publishes a "Bhavcopy" file every day here: http://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3

Write a Python script that:
- Downloads the Equity bhavcopy zip from the above page
- Extracts and parses the CSV file in it
- Writes the records into Redis into appropriate data structures
(Fields: code, name, open, high, low, close)

Write a simple CherryPy python web application that:
- Renders an HTML5 + CSS3 page that lists the top 10 stock entries from the Redis DB in a table
- Has a searchbox that lets you search the entries by the 'name' field in Redis and renders it in a table
- Make the page look nice!

