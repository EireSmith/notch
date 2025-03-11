allowed_file_ext = ["DOC", "DOX", "PDF", "JPEG", "JPG", "PNG", "XLSX", "XLS"]
max_filesize = 1000000  # 1mb


def allowed_file(filename):
    if not "." in filename:
        return False

    # split on "." and get the extension element on the right.
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_file_ext:
        return True
    else:
        return False


def allowed_filesize(filesize):

    if int(filesize) > max_filesize:
        return False
    else:
        return True
