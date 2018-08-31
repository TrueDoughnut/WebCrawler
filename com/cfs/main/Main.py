import mechanicalsoup
import os

downloaded_urls = []

# downloads a file with the url as a name
def download_file(url, browser):
    path = "downloads\\" + url[:-1].replace("https://", "").replace("/", "+") + ".html"
    for i in range(0, len(path)):
        if path[i] == "+":
            path = path[i:]
        else:
            break
    file = open(path, "w+")
    file.close()
    if "https://" not in browser.get_url() and "http://" not in browser.get_url():
        browser.open("https://" + browser.get_url())
    elif "https:" not in browser.get_url() and "http:" not in browser.get_url():
        browser.open("https" + browser.get_url())
    browser.download_link(file=path)
    downloaded_urls.append(url)

def downloaded(url):
    return url in downloaded_urls

def download_all_links(initial_url, function_browser):
    # get all links
    links = [function_browser.get_url()] # add initial url
    for x in function_browser.get_current_page().find_all('a'):
        links.append(x.get('href'))
    print(links)
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

def run():
    initial_url = "https://www.wikipedia.org/"

    # create browser object
    browser = mechanicalsoup.StatefulBrowser()
    # change directory to access downloads folder
    os.chdir("..\\..\\..")
    # open starting page
    browser.open(initial_url)
    download_all_links(initial_url, browser)

if __name__ == '__main__':
    run()
    print(downloaded_urls)