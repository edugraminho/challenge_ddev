### Challenge
```
    To select a department individually: 
    - Open config.py
    - Select a name from the list
```

Your challenge is to automate the process of extracting data from [**itdashboard.gov**](http://itdashboard.gov/).

- The bot should get a list of agencies and the amount of spending from the main page
    - Click "**DIVE IN"** on the homepage to reveal the spend amounts for each agency
    - Write the amounts to an excel file and call the sheet "**Agencies**".
- Then the bot should select one of the agencies, for example, National Science Foundation (this should be configured in a file or on a Robocloud)
- Going to the agency page scrape a table with all "**Individual Investments**" and write it to a new sheet in excel.
- If the "**UII**" column contains a link, open it and download PDF with Business Case (button "**Download Business Case PDF**")
- Your solution should be submitted and tested on [**Robocloud**](https://cloud.robocorp.com/).
- Store downloaded files and Excel sheet to the root of the `output` folder

## Author
Eduardo Fior Graminho
[**github**](https://github.com/edugraminho)