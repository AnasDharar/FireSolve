import requests
def getSubmissions(username=None):
    html_content = None
    if username is None:
        print("Please provide a username.")
    url = f"https://www.codechef.com/recent/user?page=0&user_handle={username}"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.json()["content"]
        return html_content #html_content = None will never be returned
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None
    
def getUser(username=None):
    html_content = None
    if username is None:
        username = input("Enter the username: ")
    url = f"https://www.codechef.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None