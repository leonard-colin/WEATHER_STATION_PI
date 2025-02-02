# -*- coding:utf-8 -*-

import requests
import textwrap

class News:
    def __init__(self):
        pass

    def update(self, api_id):
        # TODO: check if google news api has been "fixed" (`sources=google-news-fr`)
        self.news_list = requests.get(
            f"https://newsapi.org/v2/top-headlines?sources=le-monde&apiKey={api_id}"
        ).json()
        return self.news_list

    def selected_title(self):
        list_news = []
        if self.news_list["status"] == "ok":
            for i in range(len(self.news_list["articles"])):
                line = self.news_list["articles"][i]["title"]
                line = textwrap.wrap(line, width=60)
                list_news.append(line)
        else:
            list_news = ["Problème de chargement des news"]
        return list_news
