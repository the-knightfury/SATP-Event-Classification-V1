import pandas as pd


def remove_special_characters(data, col_name):

    spec_chars = ["!", '"', "#", "%", "&", "'", "*", "+", "-", "/", ":", ";", "<", "=",
                  ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", "–"]
    for char in spec_chars:
        data[col_name] = data[col_name].str.replace(char, ' ')
    data[col_name] = data[col_name].str.split().str.join(" ")

    return data
