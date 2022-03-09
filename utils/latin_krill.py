import re


latin = ["YO", "Yo", "yo", "YA", "Ya", "ya", "Ye", "YE", "ye", "O'", "o'", "G'", "g'", "SH", "Sh", "sh", "CH", "Ch", "ch", "Yu", "YU", "yu", "A", "a", "B", "b", "D", "d", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "X", "x", "Y", "y", "Z", "z", "'"]
krill = ["Ё", "Ё", "ё", "Я", "Я", "я", "Е", "Е", "е", "Ў", "ў", "Ғ", "ғ", "Ш", "Ш", "ш", "Ч", "Ч", "ч", "Ю", "Ю", "ю", "А", "а", "Б", "б", "Д", "д", "Ф", "ф", "Г", "г", "Ҳ", "ҳ", "И", "и", "Ж", "ж", "К", "к", "Л", "л", "М", "м", "Н", "н", "О", "о", "П", "п", "Қ", "қ", "Р", "р", "С", "с", "Т", "т", "У", "у", "В", "в", "Х", "х", "Й", "й", "З", "з", "ъ"]

def latin_krill_converter(text: str, dest: str):
    for i in range(len(latin)):
        if dest == "latin":
            text = re.sub(krill[i], latin[i], text)
        else:
            text = re.sub(latin[i], krill[i], text)
    return text