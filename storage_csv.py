from istorage import IStorage
import csv
import pandas as pd


# https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        with open(self.file_path, "r") as fileobj:
            csvreader = csv.DictReader(fileobj)
            list_of_movies = []
            for row in csvreader:
                list_of_movies.append(row)
            return list_of_movies

    def add_movie(self, title, year, poster, rating):
        self.title = title
        self.year = year
        self.rating = rating
        self.poster = poster
        new_data = {"Title": self.title, "Rating": self.rating, "Year": self.year, "Poster": self.poster}
        with open("movies.csv", "a", newline='') as fileobj:
            writer = csv.DictWriter(fileobj, fieldnames=new_data.keys())
            writer.writerow(new_data)

    def delete_movie(self, title):
        self.title = title
        df = pd.read_csv('movies.csv', index_col='Title')
        df = df.drop(self.title)
        df.to_csv('movies.csv', index=True)

    def update_movie(self, title, rating):
        self.title = title
        self.rating = rating
        list_of_movies = self.list_movies()
        for item in list_of_movies:
            print(item)
            print(self.title, "self")
            print(item["Title"])
            if self.title == item["Title"]:
                item["Rating"] = self.rating
        headers = ["Title","Rating","Year","Poster"]
        with open("movies.csv", "w") as fileobj:
            data = csv.DictWriter(fileobj, fieldnames=headers)
            data.writeheader()
            data.writerows(list_of_movies)

