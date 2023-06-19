import statistics
import random
import requests
from storage_json import StorageJson


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def get_url(self, url):
        try:
            movie_title = input("Which movie do you want to add? ")
            params = {"t": movie_title}
            r = requests.get(url, params=params)
            data = r.json()
            if data["Response"] == "False":
                print(f"We Couldn't find the movie {movie_title}. Please, try again.")
                self.get_url(url)
            self._command_add_movie(data)
            return
        except requests.HTTPError as e:
            print(f"[!] Exception caught: {e}")

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        # iterate over the data showing the list of movies
        #print(f"{len(movies)} movies in total")
        for item in movies:
            print(f"{item['Title']}, Year of release: {item['Year']}")
        # Returns to the main menu
        input("Press enter to continue:")
        return self.run()

    def _command_add_movie(self, movie):
        # No fututo impedir duplicadas - Chamar função list e atribuir a lista a uma var depois verificar se o filme já existe na lista.
        self.movie = movie
        # Gets the data from the json
        movie_title = self.movie["Title"]
        movie_year = self.movie["Year"]
        movie_poster = self.movie["Poster"]
        for i in self.movie["Ratings"]:
            if i["Source"] == "Internet Movie Database":
                movie_rating = i["Value"]
        # Sends the data to the module
        self._storage.add_movie(movie_title, movie_year, movie_poster, movie_rating)
        input("Press enter to continue")
        return self.run()

    def _command_del_movie(self):
        # Aks for the name of the movie to be deleted
        movie_name = input("Enter movie name:")
        # Calls the module
        self._storage.delete_movie(movie_name)
        # Returns to the main menu
        print(f"Movie {movie_name} successfully deleted:")
        input("Press enter to continue")
        return self.run()

    def _command_update_movie(self):
        # Verificar erros com os inputs, letras sem caps ou numero de digitos nos rating
        # Asks for the data to be updated
        movie_name = input("Enter movie name:")
        new_rating = float(input("Enter new rating:"))
        # Calls the module
        self._storage.update_movie(movie_name, new_rating)
        # Returns to the main menu
        print(f"Movie {movie_name} successfully updated:")
        input("Press enter to continue")
        return self.run()

    def _command_stats(self):
        # Transforms in a list
        ratings = []
        movies = self._storage.list_movies()
        for movie in movies:
            ratings.append(float(movie['Rating'][slice(0, 3)]))
        # Calculates the mean
        ratings_mean = statistics.mean(ratings)
        print(f"Average rating: {ratings_mean}")
        # Calculates the median
        ratings_median = statistics.median(ratings)
        print(f"Median rating: {ratings_median}")
        # Finds max and min
        max_rating = max(ratings)
        min_rating = min(ratings)
        # Iterates through the list to find a match for max and min
        for i in movies:
            if max_rating == i['Rating']:
                print(f"Best movie: {i['Title']}, {i['Rating']}")
            elif min_rating == i['Rating']:
                print(f"Worst movie: {i['Title']}, {i['Rating']}")
        # Returns to the main menu
        input("Press enter to continue")
        return self.run()

    def _command_random_movie(self):
        # Randomly chooses a movie
        movies = self._storage.list_movies()
        rdm_movie = random.choice(movies)
        for movie in movies:
            if movie == rdm_movie:
                # print(rdm_movie)
                print(f"{movie['Title']}, Rating: {movie['Rating']}, Year of release: {movie['Year']}")
        # Returns to the main menu
        input("Press enter to continue")
        return self.run()

    def _command_search_movie(self):
        # Asks for element of the search
        part_of_movie = input("Enter part of movie name:")
        # Searches through the dictionaries to find match
        movies = self._storage.list_movies()
        for i in movies:
            if part_of_movie not in i['Title']:
                continue
            else:
                print(f"Results of your search:{i['Title']}, Rating: {i['Rating']}, Year of release: {i['Year']}")
                break
        # Returns to the main menu
        input("Press enter to continue")
        return self.run()

    def _command_sorted_movies(self):
        # Sorts the ratings into a list
        ratings = []
        movies = self._storage.list_movies()
        for i in movies:
            if i['Rating'] not in ratings:
                ratings.append(i['Rating'])
                srtd_list = sorted(ratings, reverse=True)
        # iterates to print a sorted set of movie and ratings
        for i in srtd_list:
            for j in movies:
                if i == j['Rating']:
                    print(f"{j['Title']} {j['Rating']}")
        # Returns to the main menu
        input("Press enter to continue")
        return self.run()

    @staticmethod
    def _command_exit(self):
        print('Bye!')

    # Generate Website functions
    def website_info(self):
        movie_output = ''
        movies_info = self._storage.list_movies()
        for i in movies_info:
            movie_output += '<li class="movie-grid li">\n<div class="movie">'
            movie_output += f'<img src = {i["Poster"]} class="movie-poster">'
            movie_output += f'<div class="movie-title">{i["Title"]}</div>'
            movie_output += f'<div class="movie-year">{i["Year"]}</div>\n<div/>\n</li>'
        return movie_output

    def read_template(self):
        with open("index_template.html", "r") as template:
            data = template.read()
            return data

    def open_new_file(self, content):
        with open("index.html", "w") as fileobj:
            new_data = fileobj.write(content)
            print("Website successfully generated")
            return new_data

    def replace(self, output, template):
        content = template.replace('__TEMPLATE_MOVIE_GRID__', output).replace('__TEMPLATE_TITLE__', 'My Movie App')
        return content

    def run(self):
        menu_text = """
      Menu:
      0. Exit
      1. List movies
      2. Add movies 
      3. Delete movie
      4. Update movie
      5. Stats
      6. Random movie
      7. Search movie
      8. Sort movies
      9. Generate website
      """
        url = "http://www.omdbapi.com/?apikey=19391c77&"
        print(menu_text)
        item_chosen = int(input(f" Enter choice (0-9):"))
        if item_chosen == 1:
            self._command_list_movies()
        elif item_chosen == 2:
            self.get_url(url)
        elif item_chosen == 3:
            self._command_del_movie()
        elif item_chosen == 4:
            self._command_update_movie()
        elif item_chosen == 5:
            self._command_stats()
        elif item_chosen == 6:
            self._command_random_movie()
        elif item_chosen == 7:
            self._command_search_movie()
        elif item_chosen == 8:
            self._command_sorted_movies()
        elif item_chosen == 0:
            exit()
        elif item_chosen == 9:
            new_file_content = self.replace(self.website_info(), self.read_template())
            self.open_new_file(new_file_content)

    def main(self):
        self.run()


"""storage = StorageJson('movies.json')
movie_app = MovieApp(storage)
movie_app.run()"""
