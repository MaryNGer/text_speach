import os
from typing import Tuple

import whisper
from flask import Flask, render_template, request
from gtts import gTTS

app = Flask(__name__)

model = whisper.load_model("medium")


def save_files() -> str:
    """
    Функция save_files() используется для сохранения аудиофайлов в указанной директории 'static/voice'.

    :return: Возвращает путь к сохраненному аудиофайлу в формате строки.
    """

    path = os.path.join('static/voice')

    files_name = os.listdir(path)

    num = len(files_name)

    if len(files_name) == 0:
        new_name = 'voice.mp3'

    else:
        new_name = f'voice_{num}.mp3'

    path_voice = os.path.join(f"static/voice/{new_name}")

    return path_voice


def rec_audio(text) -> str:
    """
    Функция rec_audio(text) используется для создания аудиофайла с заданным текстом и сохранения его в директории 'static/voice'.

    :param text: Текст, который будет преобразован в аудиофайл.
    :return: Возвращает путь к сохраненному аудиофайлу в формате строки.
    """
    path = save_files()

    tts = gTTS(text, lang='ru')

    tts.save(path)

    return path


def get_text(text) -> Tuple[str, str]:
    """
    Функция принимает текст и преобразует его в аудио. Если текст отсутствует (длина меньше 1),
    выводится соответствующее сообщение. Возвращает путь к аудиофайлу и исходный текст.

    :param text: Текст для преобразования в аудио.
    :type text: str
    :return: Кортеж с путем к аудиофайлу и исходным текстом.
    :rtype: Tuple[str, str]
    """
    if len(text) < 1:
        text = ('Вы не передали текст для преобразования! Пожалуйста вернитесь на главную страницу'
                ' и передайте в окно текст')

    path = rec_audio(text)

    return path, text


def get_file(file) -> Tuple[str, str]:
    """
    Функция принимает загруженный файл и выполняет преобразование в текст.
    Если файл не загружен (имя файла пустое), возвращается соответствующее сообщение и путь к аудиофайлу.

    :param file: Загруженный файл для преобразования в текст.
    :type file: FileStorage
    :return: Кортеж с текстом и путем к файлу.
    :rtype: Tuple[str, str]
    """
    if file.filename == '':
        text = ('Вы не передали файл для преобразования! Пожалуйста вернитесь на главную страницу'
                ' и передайте в окно файл')
        path = rec_audio(text)
        return text, path

    # # Сохраняем загруженный файл на диск
    file_path = save_files()
    file.save(file_path)

    result = model.transcribe(file_path)
    text = result["text"]

    return text, file_path


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def index():
    """
    Обработчик маршрутов "/" и "/home" веб-приложения.
    Отвечает за отображение формы для ввода текста либо загрузки файла и обработку этих данных
    в соответствии с запросом пользователя.
    :return:
    """
    if request.method == "POST":
        if 'text' in request.form:

            text = request.form['text']

            result, text = get_text(text)

            return render_template("index_text_to_speach_result.html", result=result, text=text)
        else:

            file = request.files['file']

            result_text, result_file = get_file(file)

            return render_template("index_text_to_speach_result.html", result_text=result_text, result_file=result_file)

    return render_template("index_text_to_speach.html")


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
