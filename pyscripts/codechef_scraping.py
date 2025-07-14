from bs4 import BeautifulSoup
# import fetching
import requests
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

def soup_for_submissions(username):
    html_content = None
    url = f"https://www.codechef.com/recent/user?page=0&user_handle={username}"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.json()["content"]
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    if html_content:
        return BeautifulSoup(html_content, "html.parser")
    return None

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
    
def submissions(user,target):
    soup = soup_for_submissions(user)
    table = soup.find_all("table", class_="dataTable")[0]
    content = table("tbody")[0] #Getting the first and only tbody, which contains all the submissions
    for i in range(min(len(content.find_all("tr")), 5)):
        sub = content("tr")[i].find_all("td")
        if sub[1]["title"] == target and sub[2].find("span")["title"]=="accepted":
            return True
    return False

if __name__ == "__main__":
    username = input("Enter the username: ")
    soup = soup_for_submissions(username)
    soupUser = soup_for_user(username)
    kundli() #get everything from name, rating, rank(global and country),college,country etc
    print(submissions('COSTSWAP'))