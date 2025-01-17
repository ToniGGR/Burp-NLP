import requests
from bs4 import BeautifulSoup
import json

episodes_counter = 1


def basic_web_scraper(url):

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        soup = BeautifulSoup(response.text, "html.parser")

        soup_episodes = soup.find_all("div", {"class": "ipc-title__text"})

        soup_ratings = soup.find_all("span", {"class": "ipc-rating-star--rating"})

        list_episode_tuples = [
            (
                str(x)
                .replace("<div ", "")
                .replace("</div>", "")
                .replace('class="ipc-title__text">', "")
                .split(" ∙ ")[0],
                str(x)
                .replace("<div ", "")
                .replace("</div>", "")
                .replace('class="ipc-title__text">', "")
                .split(" ∙ ")[1],
            )
            for x in soup_episodes
        ]

        list_ratings = [
            str(x)
            .replace('class="ipc-rating-star--rating">', "")
            .replace("<span ", "")
            .replace("</span>", "")
            for x in soup_ratings
        ]

        global episodes_counter
        d = {}
        for i in range(len(list_episode_tuples)):
            episode_d = {}
            episode_d["season"] = list_episode_tuples[i][0].split(".")[0]
            episode_d["episode"] = list_episode_tuples[i][0].split(".")[1]
            episode_d["title"] = list_episode_tuples[i][1]
            episode_d["rating"] = float(list_ratings[i])
            d[episodes_counter + i] = episode_d

        episodes_counter += len(list_episode_tuples)

        return d

    except requests.exceptions.RequestException as e:

        print(f"An error occurred: {e}")
        return {}


# Example usage
if __name__ == "__main__":

    all_dictionary = {}

    amount_seasons = 7
    season = 1
    while season <= amount_seasons:
        url_to_scrape = (
            f"https://www.imdb.com/title/tt2861424/episodes/?season={season}&ref_=ttep"
        )
        all_dictionary.update(basic_web_scraper(url_to_scrape))
        season += 1

    json_text = json.dumps(all_dictionary)
    f = open("./episodes.json", "w")
    f.write(json_text)

    print(all_dictionary)
