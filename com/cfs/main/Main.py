import mechanicalsoup
import os

downloaded_urls = []
scraped_urls = []

# downloads a file with the url as a name
def download_file(url, browser):
    print(url)
    path = "downloads\\" + url[:-1].replace("https://", "").replace("/", "+") + ".html"

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
    file_endings = [".mp3"]
    for file_ending in file_endings:
        current_ending = path[len(path)-len(file_ending)-4:]
        print(current_ending)
        if file_ending in current_ending:
            scraped_urls.append(url)
            return

    # create file
    file = open(path, "w+")
    file.close()

    # download browser
    browser.download_link(file=path)
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
        if initial_url.replace("https://www", "") in x:
            temp.add(x)
    links = temp
    print(links)
    # download all pages linked on this page
    for x in links:
        if not downloaded(x):
            download_file(str(x), function_browser)
    scraped_urls.append(initial_url)

def array_equality():
    if len(downloaded_urls) != len(scraped_urls):
        return False
    for i in range(0, len(downloaded_urls)-1):
        if downloaded_urls[i] != scraped_urls[i]:
            return False
    return True

def run():
    initial_url = "https://www.madebyfew.com/"

    # create browser object
    browser = mechanicalsoup.StatefulBrowser()
    # change directory to access downloads folder
    os.chdir("..\\..\\..")
    # open starting page
    browser.open(initial_url)
    download_all_links_on_page(initial_url, browser)

    # cycle through all urls
    while not array_equality():
        urls = list(set(scraped_urls).symmetric_difference(set(downloaded_urls)))
        for url in urls:
            print(urls)
            download_all_links_on_page(url, browser)
            print("next page")

if __name__ == '__main__':
    run()