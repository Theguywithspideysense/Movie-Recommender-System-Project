import requests

API_KEY = "0ff4cc61a5005fcc2bd6e2254fd767e3"

url = f"https://api.themoviedb.org/3/movie/19995?api_key={API_KEY}"

try:
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    print("Status:", response.status_code)
    print(response.text)

except Exception as e:
    print(e)