from database import models


class Config:
    @staticmethod
    def get_table_fields(table):
        table_fields = {
            'halls': ['№', 'Вместимость'],
            'movies': ['№', 'Название', 'Жанр'],
            'sales': ['№', '№ фильма', '№ зала', 'Время', '№ места']
        }

        return table_fields[table]

    @staticmethod
    def get_field_by_output(type_output):
        output_fields = {
            'hall_workload': ['№ зала', 'Загрузка (%)'],
            'popular_genre': ['Жанр', 'Популярность (кол-во фильмов)']
        }

        return output_fields[type_output]

    @staticmethod
    def get_table_model(table):
        table_models = {
            'halls': models.Hall,
            'movies': models.Movie,
            'sales': models.Sale,
        }

        return table_models[table]

    @staticmethod
    def get_table_field_models(table):
        table_field_models = {
            'halls': {
                'default': models.Hall,
                'capacity': models.Hall.capacity,
            },
            'movies': {
                'default': models.Movie,
                'title': models.Movie.title,
                'genre': models.Movie.genre
            },
            'sales': {
                'default': models.Sale,
                'id_movie': models.Sale.id_movie,
                'id_hall': models.Sale.id_hall,
                'time': models.Sale.time,
                'place_number': models.Sale.place_number,

            }
        }

        return table_field_models[table]
