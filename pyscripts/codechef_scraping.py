from bs4 import BeautifulSoup
# import fetching
import requests
import json
from requests.exceptions import RequestException
def soup_for_user(username):
    html_content = None
    url = f"https://www.codechef.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    if html_content:
        return BeautifulSoup(html_content, "html.parser")
    return None
# def soup_for_submissions(username):
#     html_content = None
#     url = f"https://www.codechef.com/recent/user?page=0&user_handle={username}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         html_content = response.json()["content"]
#         print("Fetched submissions successfully")
#     else:
#         print(f"Failed to fetch the webpage. Status code: {response.status_code}")
#     if html_content:
#         return BeautifulSoup(html_content, "html.parser")
#     return None
SESSION_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.codechef.com/",
    "X-Requested-With": "XMLHttpRequest",  # helps signal an AJAX request
    "Connection": "keep-alive",
}

def soup_for_submissions(username, session=None, page=0, timeout=20):
    if session is None:
        session = requests.Session()
        # Prime cookies by hitting homepage
        try:
            session.get("https://www.codechef.com/", headers=SESSION_HEADERS, timeout=timeout)
        except RequestException:
            pass  # not fatal; continue

    url = f"https://www.codechef.com/recent/user?page={page}&user_handle={username}"

    try:
        resp = session.get(url, headers=SESSION_HEADERS, timeout=timeout)
    except RequestException as e:
        print(f"Network error fetching submissions: {e}")
        return None

    if resp.status_code != 200:
        print(f"Failed: status {resp.status_code}")
        return None

    # Try to parse JSON
    try:
        data = resp.json()
    except json.JSONDecodeError:
        print("Response was not JSON (maybe blocked / HTML).")
        return None

    html_content = data.get("content")
    if not html_content:
        print("No 'content' field in response.")
        return None

    print("Fetched submissions successfully.")
    return BeautifulSoup(html_content, "html.parser")

def submissions(user,target):
    soup = soup_for_submissions(user)
    if not soup:
        print("Failed to fetch submissions.")
        return False
    table = soup.find_all("table", class_="dataTable")[0]
    content = table("tbody")[0] #Getting the first and only tbody, which contains all the submissions
    for i in range(min(len(content.find_all("tr")), 5)):
        sub = content("tr")[i].find_all("td")
        if sub[1]["title"] == target and sub[2].find("span")["title"]=="accepted":
            return True
    return False

def kundli():
    # Getting the name of the user
    name = soupUser.find("h1", class_="h2-style").text
    # # Getting the rating of the user
    rating = soupUser.find("div", class_="rating-number").text
    # Getting the rank of the user
    cont = soupUser.find("div", class_="rating-ranks")
    ranks = cont.find_all("strong")
    #container to getting username, country,student,institution
    container = soupUser.find("ul", class_="side-nav")
    spans = container.find_all("li")

    print("Name: ", name)
    print(spans[0].text)
    print("Rating: ", rating)
    print("Global rank: ", ranks[0].text)
    print("Country rank: ", ranks[1].text)


    print(spans[1].text)
    print(spans[2].text)
    print(spans[3].text)

if __name__ == "__main__":
    username = input("Enter the username: ")
    soup = soup_for_submissions(username)
    soupUser = soup_for_user(username)
    kundli() #get everything from name, rating, rank(global and country),college,country etc
    print(submissions('COSTSWAP'))