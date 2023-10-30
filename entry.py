import pickle
from hashlib import sha1


class Entry:
    def __init__(self, title, descr, link, is_top=False) -> None:
        self.title = title
        self.descr = descr
        self.link = link
        self.is_top = is_top
        self.iv = None
        self.guid = sha1(str.encode(f'{title}{descr}{link}')).hexdigest()
