import sqlite3


__con__ = sqlite3.connect("./bumpers.db")
__cur__ = __con__.cursor()
