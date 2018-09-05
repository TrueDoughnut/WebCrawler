import mechanicalsoup
import os

downloaded_urls = []
scraped_urls = []

base_url = ""

# downloads a file with the url as a name
def download_file(url, browser):
    path = "downloads\\" + url.replace("https://", "").replace("/", "+") + ".html"

    # remove pluses at beginning of filename
    for i in range(0, len(path)):
        if path[i] == "+":
            path = path[i:]
        else:
            break
    # remove illegal characters
    chars = ["<", ">", ":", "\"", "/", "|", "?", "*"]
    for char in chars:
        if char in path:
            path = path.replace(char, "")

    # check if url is valid
    if "https://" not in browser.get_url() and "http://" not in browser.get_url():
        browser.open("https://" + browser.get_url())
    elif "https:" not in browser.get_url() and "http:" not in browser.get_url():
        browser.open("https" + browser.get_url())

    # make sure url is webpage, not file
    file_endings = [".mp3", ".png", ".gif"]
    for file_ending in file_endings:
        current_ending = path[len(path)-len(file_ending)-4:]
        if file_ending in current_ending:
            scraped_urls.append(url)
            print("found ending")
            return

    # create file
    file = open(path, "w+")
    file.close()

    # download browser
    browser.download_link(file=path)
    print("downloading")
    downloaded_urls.append(url)

# has the url been downloaded
def downloaded(url):
    return url in downloaded_urls

def download_all_links_on_page(initial_url, function_browser):
    # get all links
    links = [function_browser.get_url()] # add initial url
    for x in function_browser.get_current_page().find_all('a'):
        links.append(x.get('href'))
    # only use links that have initial url in url
    temp = set() # set to remove duplicates
    for x in links:
        if base_url in x:
            temp.add(x)
    links = temp
    # download all pages linked on this page
    for x in links:
        if not downloaded(x):
            download_file(str(x), function_browser)
    scraped_urls.append(initial_url)
    print("added to scraped")

def array_equality():
    if len(downloaded_urls) != len(scraped_urls):
        return False
    for i in range(0, len(downloaded_urls)-1):
        if downloaded_urls[i] != scraped_urls[i]:
            return False
    return True

def run():
    initial_url = "http://www.pmichaud.com/"

    # create browser object
    browser = mechanicalsoup.StatefulBrowser()
    # change directory to access downloads folder
    os.chdir("..\\..\\..")
    global base_url
    base_url = initial_url.replace("http://www", "").replace("https://www", "")
    # open starting page
    browser.open(initial_url)
    download_all_links_on_page(initial_url, browser)

    # cycle through all urls
    while not array_equality():
        urls = list(set(scraped_urls).symmetric_difference(set(downloaded_urls)))
        for url in urls:
            download_all_links_on_page(url, browser)
            print("next page", urls)

if __name__ == '__main__':
    run()