from dataclasses import dataclass
import sqlite3


__con__ = sqlite3.connect("./bumpers.db")
__cur__ = __con__.cursor()


@dataclass()
class Bumper:
    user_id: int
    bumps: int
    ping: bool


def insert(id):
    __cur__.execute("INSERT INTO bumpers VALUES (?,?,?)", (id, 1, 0))
    __con__.commit()


def get(id):
    if not registered(id):
        raise BumperNotRegistered(id)
    __cur__.execute("SELECT * FROM bumpers WHERE id=:id", {"id": id})
    bt = __cur__.fetchone()
    return Bumper(bt[0], bt[1], bt[2] == 1)


def registered(user_id: int) -> bool:
    __cur__.execute("SELECT * FROM bumpers WHERE id=:id", {"id": user_id})
    if len(__cur__.fetchall()) == 1:
        return True
    return False


def get_top():
    __cur__.execute("SELECT * FROM bumpers ORDER BY bumps DESC")
    return __cur__.fetchall()


def get_pinged():
    __cur__.execute("SELECT * FROM bumpers WHERE ping=1")
    return __cur__.fetchall()


def add_bump(bumper: Bumper):
    __cur__.execute("UPDATE bumpers SET bumps=? WHERE id=?", (bumper.bumps + 1, bumper.user_id))
    __con__.commit()


def enable_ping(bumper: Bumper):
    __cur__.execute("UPDATE bumpers SET ping=? WHERE id=?", (1, bumper.user_id))
    __con__.commit()


def disable_ping(bumper: Bumper):
    __cur__.execute("UPDATE bumpers SET ping=? WHERE id=?", (0, bumper.user_id))
    __con__.commit()


class BumperNotRegistered(Exception):
    def __init__(self, requested_id, *args: object) -> None:
        self.requested_id = requested_id
        super().__init__(*args)

    def __str__(self) -> str:
        return f"The requested bumper ({self.requested_id}) is not registered"
