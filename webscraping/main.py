import requests
from bs4 import BeautifulSoup
import json

episodes_counter = 1


def create_imdb_ratings():
    all_dictionary = {}

    amount_seasons = 7
    season = 1
    while season <= amount_seasons:
        url_to_scrape = (
            f"https://www.imdb.com/title/tt2861424/episodes/?season={season}&ref_=ttep"
        )
        all_dictionary.update(web_scraper_imdb(url_to_scrape))
        season += 1

    json_text = json.dumps(all_dictionary)
    f = open("./episodes.json", "w")
    f.write(json_text)

    print(all_dictionary)


def web_scraper_imdb(url):

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


def generate_plots():

    base_url = "https://rickandmorty.fandom.com"

    all_episode_url = "https://rickandmorty.fandom.com/wiki/List_of_episodes"

    try:
        response = requests.get(all_episode_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        soup = BeautifulSoup(response.text, "html.parser")

        episode_urls = [x.get("href") for x in soup.select(f"td b a")]
        episode_titles = [x.get("title") for x in soup.select(f"td b a")]
        episodes_numbers = range(len(episode_titles))

        print(episode_urls[9])

        temp_dict = {}

        whole_dict = {}

        for id in episodes_numbers:
            temp_dict = {
                "title": episode_titles[id],
                "text": get_single_plot(base_url + episode_urls[id]),
            }

            whole_dict[id] = temp_dict

        f = open("./data/episodes_descriptions.json", "w")
        f.write(json.dumps(whole_dict))

    except requests.exceptions.RequestException as e:

        print(f"An error occurred: {e}")
        return {}


def get_single_plot(url: str) -> str:

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        soup = BeautifulSoup(response.text, "html.parser")
        start_tag = soup.find(id="Plot")
        end_tag = soup.find(id="Characters")
        content = []
        current_tag = start_tag.find_next()

        while current_tag and current_tag != end_tag:
            if current_tag.name == "p":  # Nur <p>-Tags
                modified_p = current_tag.decode_contents()
                p_soup = BeautifulSoup(modified_p, "html.parser")
                for a_tag in p_soup.find_all("a"):
                    a_tag.replace_with(f"___{a_tag.text}___")

                content.append(p_soup.get_text(strip=True))
            current_tag = current_tag.find_next()
        prettify_content = "".join([line.replace("___", " ") for line in content])
        return prettify_content
    except requests.exceptions.RequestException as e:

        print(f"An error occurred: {e}")
        return ""


# Example usage
if __name__ == "__main__":

    # create_imdb_ratings()
    generate_plots()
