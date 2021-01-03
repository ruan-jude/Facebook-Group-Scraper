# FacebookGroupScraper
Created this tool to extract member information from a Facebook group to assist club alumni relations. FacebookScraper.py contains a scraper class which collects member names and join dates, then stores them into respective Lists. DataExtractor.py utilizes Pandas to store the List data into a properly labelled DataFrame. That DataFrame is then sent to a Google Sheet through Google APIs.

Sources:
  Google APIs: https://www.techwithtim.net/tutorials/google-sheets-python-api-tutorial/
  Selenium scrolling: https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
  Notifications options: https://stackoverflow.com/questions/38684175/how-to-click-allow-on-show-notifications-popup-using-selenium-webdriver
  
