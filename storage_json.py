from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        with open(self.file_path, "r") as fileobj:
            data = json.loads(fileobj.read())
            return data

    def add_movie(self, title, year, poster, rating):
        self.title = title
        self.year = year
        self.rating = rating
        self.poster = poster
        new_data = {"Title": self.title, "Rating": self.rating, "Year": self.year, "Poster": self.poster}
        with open("movies.json", "r+") as fileobj:
            file_data = json.loads(fileobj.read())
            file_data.append(new_data)
            fileobj.seek(0)
            json.dump(file_data, fileobj, indent=4)

    def delete_movie(self, title):
        self.title = title
        with open("movies.json") as fileobj:
            file_data = json.loads(fileobj.read())
            for item in file_data:
                if self.title == item["Title"]:
                    file_data.remove(item)
        with open("movies.json", "w") as fileobj:
            json.dump(file_data, fileobj, indent=4)

    def update_movie(self, title, rating):
        self.title = title
        self.rating = rating
        with open("movies.json", "r") as fileobj:
            file_data = json.loads(fileobj.read())
            for item in file_data:
                if self.title == item["Title"]:
                    item["Rating"] = self.rating
        with open("movies.json", "w") as fileobj:
            json.dump(file_data, fileobj, indent=4)
