from bottle import route, run, request, HTTPError

import album

@route("/albums/<artist>")
def albums(artist):
    """
    Обабатывает GET-запрос
    """
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def new_album():
    test_year = album.is_number(request.forms.get("year"))  # Проверяет, являестя ли введенный год числом
    if test_year is not False:
        album_data = {
            "year": int(test_year),
            "artist": request.forms.get("artist"),
            "genre": request.forms.get("genre"),
            "album": request.forms.get("album")
        }
        if album.find_album(album_data["artist"], album_data["album"]):  # проверяет, есть ли такой альбом в базе
            result = HTTPError(409, "Альбом {} {} уже есть в базе".format(album_data["artist"], album_data["album"]))
        else:
            if 1900 <= album_data["year"] >= 2019:  # проверяет, корректно ли введен год
                result = HTTPError(409, "Введены неверные данные. Поле год допускает значения от 1900 до 2019")
            elif album_data["artist"].replace(" ", "") == "" or album_data["genre"].replace(" ", "") == "" or album_data["album"].replace(" ", "") == "":
                result = HTTPError(409, "Поля артист, жанр или альбом не могут быть пустыми")
            else:
                album.album_add(album_data["year"], album_data["artist"], album_data["genre"], album_data["album"])
                result = "Альбом {} {} добавлен в базу".format(album_data["artist"], album_data["album"])
    else:
        result = HTTPError(409, "Введены неверные данные. Поле год содержит не числовые значения")
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
