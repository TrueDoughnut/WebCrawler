import mechanicalsoup
import os

global downloaded_links = []

# downloads a file with the url as a name
def download_file(url, browser):
    path = "downloads\\" + url[:-1].replace("https://", "").replace("/", "+") + ".html"
    file = open(path, "w+")
    file.close()
    browser.download_link(file=path)

def download_all_links(function_browser):
    # get all links
    links = [function_browser.get_url()]
    for x in function_browser.get_current_page().find_all('a'):
        links.append(x.get('href'))
    # only use links that have github.com in url
    temp = set() # set to remove duplicates
    for x in links:
        if "github.com" in x:
            temp.add(x)
    links = temp
    print(links)
    # download all pages linked on this page
    for x in links:
        download_file(str(x))

def run():
    initial_url = "https://github.com"

    # create browser object
    browser = mechanicalsoup.StatefulBrowser()
    # change directory to access downloads folder
    os.chdir("..\\..\\..")
    # open starting page
    browser.open(initial_url)
    download_all_links(browser)

if __name__ == '__main__':
    run()