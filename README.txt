To Run AWS, follow the steps below:

1. Requires various packages and dependencies. Make sure to install the following:
	Python 2.7
	Selenium
	Flask
	PhantomJS
	ChromeDriver
	URLs are provided if needed further instruction.

	Python 2.7 can be installed by downloading the executable file and adding it as an environmental variable on your machine.
	https://www.python.org/downloads/
	https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation

	Selenium
	Assuming "pip install" is installed on your machine, use pip to install Silenium with the following command.
	pip install -U selenium
	https://pypi.python.org/pypi/selenium

	Flask
	Use the Pip Command "pip install Flask"
	http://flask.pocoo.org/docs/0.12/installation/

	PhantomJS
	Download the latest package and keep track of file path
	http://phantomjs.org/download.html

	ChromeDriver - Web Driver for Chrome
	Download the latest package and keep track of file path
	https://sites.google.com/a/chromium.org/chromedriver/downloads

2. Navigate to the webapp directory where you will see multiple amazon files. 
	C = Chrome
	HC = Headless Chrome
	PJS = PhantomJS
   Each file represents a different test browser to use when running the program. PhantomJS is the fastest method; however
   due to its excessive speed one might run into the issue where Amazon detects it as a bot and blocks it, running into a parsing
   error. Because of this, Chrome and Headless Chrome amazon files have been provided as well. Chrome opens each individual tab
   and takes the longest, but is the most stable. Headless Chrome takes the middle amount of time where it only loads the HTML of
   the web page. All three have been provided so that the user can test different methods in case one works better than the other.

3. Navigate to the webapp directory. Open upload.py and in the header directory. 
   Specify which amazon file you would like to import--AmazonC, amazonHC, or amazonPJS. Then open the respecitve amazon.py file and 
   find two path varaibles--one in parse() funtion and one in SearchList() function. CHANGE THE PATH variables to match the location
   path of either Chromedriver or PhantomJS (where the file is located on your machine). Now open up terminal and navigate to the 
   webapp directory in your terminal. 

        RUN THE FOLLOWING COMMANDS:
	export FLASK_APP=upload.py
	flask run
	
	The output should now be displayed and be running on your local machine at the URL:
	http://127.0.0.1:5000/
	http://flask.pocoo.org/docs/0.12/quickstart/

4. Navigate to website and enter product to search for in text box. Specify the number of SEARCH products.
   Keep in mind one search result will include 5 related product links. So if the user searches 2 search products 
   then 12 results will be returned. Specify whether the products will be displayed in price of ascending or descending order. 
   Note: parsing may take some time depending on which browser user specified. So if you see the browser tab loading, please be
   patient and wait. :)  Otherwise, use AmazonC to run it and observe the URLs being opened one by one.

*************************************************************************************************************************************

NOTE: This tool will not work for all Amazon products. It collects information based off of related products. HOWEVER, there are FEW
products on Amazon that do not have related product links (for example products made by Amazon). Additionally, Amazon has different 
UI page for different services, such as their pantry items or items made by them. The parser can only parse simple items and products
that show up from a basic search. If this is the case, simply stop the server and restart it with a new search entry. 

NOTE: Due to PhantomJS's quick loading time for rendering web pages, Amazon MAY DETECT YOU AS A BOT AND BLOCK YOU, giving an error when
running the program. This is why Chrome and HeadlessChrome have been included to try as well. So please follow the instructions and try
different browsers if PhantomJS does not work. And lastly, if you have any issues, please feel free to reach out to us :)s
