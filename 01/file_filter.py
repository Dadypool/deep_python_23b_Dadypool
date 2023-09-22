"Homework 1.2 with generator that filters file"

from io import TextIOBase


def filter_file(file_obj, keywords):
    "Generate lines of file_obj that have at least one keyword"

    if not isinstance(file_obj, TextIOBase):
        if isinstance(file_obj, str):
            file_obj = open(file_obj, "r", encoding="UTF-8")
        else:
            raise TypeError("file_obj must be a file object or a file name")

    keywords = tuple(map(lambda x: str(x).lower(), keywords))

    with file_obj:
        for line in file_obj:
            line_list = line.split()
            for word in line_list:
                if word.lower() in keywords:
                    yield line
                    continue
