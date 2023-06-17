from istorage import IStorage
import csv

# https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        with open(self.file_path, "r") as fileobj:
            data = csv.loads(fileobj.read())
            return data

    def add_movie(self, title, year, poster, rating):
        self.title = title
        self.year = year
        self.rating = rating
        self.poster = poster
        new_data = {"Title": self.title, "Rating": self.rating, "Year": self.year, "Poster": self.poster}
        with open("movies.csv", "r+") as fileobj:
            file_data = csv.loads(fileobj.read())
            file_data.append(new_data)
            fileobj.seek(0)
            csv.dump(file_data, fileobj, indent=4)

    def delete_movie(self, title):
        self.title = title
        with open("movies.csv") as fileobj:
            file_data = csv.loads(fileobj.read())
            for item in file_data:
                if self.title == item["Title"]:
                    file_data.remove(item)
        with open("movies.csv", "w") as fileobj:
            csv.dump(file_data, fileobj, indent=4)

    def update_movie(self, title, rating):
        self.title = title
        self.rating = rating
        with open("movies.csv", "r") as fileobj:
            file_data = csv.loads(fileobj.read())
            for item in file_data:
                if self.title == item["Title"]:
                    item["Rating"] = self.rating
        with open("movies.csv", "w") as fileobj:
            csv.dump(file_data, fileobj, indent=4)
