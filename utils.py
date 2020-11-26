base_url = "http://www.tennisabstract.com/charting/"


def convert_to_safe_filename(text):
    return text.translate(str.maketrans(": ", "__"))


def save_match_data(data, directory, filename, compression="bz2"):
    directory = directory.strip()
    filename = filename.strip()
    if directory[-1] == "/":
        fullpath = f"{directory}{filename}"
    else:
        fullpath = f"{directory}/{filename}"

    if compression is None:
        data.to_json(fullpath, force_ascii=False, orient="index")
    else:
        if not fullpath.endswith(compression):
            fullpath = fullpath + "." + compression
        data.to_json(fullpath, force_ascii=False, orient="index", compression=compression)
