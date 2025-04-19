import requests

username = "anasdharar"
url = f"https://www.codechef.com/recent/user?page=0&user_handle={username}"

headers = {
    "User-Agent": "Mozilla/5.0"
}
with open ("web.html", "w") as file:
    file.write(requests.get(url, headers=headers).json()["content"])
response = requests.get(url, headers=headers)
dic = response.json()
print(dic["content"])  # JSON of recent submissions
