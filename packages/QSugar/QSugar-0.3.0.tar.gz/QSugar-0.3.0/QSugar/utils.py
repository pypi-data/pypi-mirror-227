def StyleDict(style: dict):
    """
    convert qss style from dictionary to QSugar property dictionary
    :param style: qss style dictionary
    :return: QSugar property dictionary
    """
    content = ''
    for key, value in style.items():
        content += str(key) + ':' + str(value) + ';'
    return {'style': content}


def Style(style: dict):
    """
    convert qss style from dictionary to string
    :param style: qss style dictionary
    :return: qss style string
    """
    content = ''
    for key, value in style.items():
        content += str(key) + ':' + str(value) + ';'
    return content