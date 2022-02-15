def listToString(list_, sep=" "):
    str_ = ""
    for elements in list_: # index all array elements
        for chars in elements: # index all chars  in current array element
            str_ += chars
        str_ += sep
    return str_

def join(list_, sep=" "):
    return sep.join(list_.split())
