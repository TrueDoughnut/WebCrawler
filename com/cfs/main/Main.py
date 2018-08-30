import mechanicalsoup
import os
import re

# create browser object
browser = mechanicalsoup.StatefulBrowser()
# change directory to access downloads folder
os.chdir("..\\..\\..")

# downloads a file with the url as a name
def download_file(url):
    path = "downloads\\" + url[:-1].replace("https://", "").replace("/", "+") + ".html"
    file = open(path, "w+")
    file.close()
    browser.download_link(file=path)

# open starting page
browser.open("https://github.com/")
download_file(browser.get_url())

print(browser.links(href=re.compile("github.com")))

