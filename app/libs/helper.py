def is_isbn_or_key(word):
    isbn_or_key = "key"
    # 判断用户输入是否为ISBN13, 13位0-9组成
    if len(word) == 13 and word.isdigit():
        isbn_or_key = "isbn"
    # 判断用户输入是否为ISBN10，10位数字组成包含一些 "-"
    short_word = word.replace("-", "")
    if "-" in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = "isbn"
    return isbn_or_key
