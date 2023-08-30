import sqlite3
import os
from typing import List, Union

_DB_FILE = "{}/cim-11.sqlite3".format(
    os.path.dirname(__file__)
)

_db = sqlite3.connect(f'file:{_DB_FILE}?mode=ro', uri=True)
_cur = _db.cursor()


class Concept:
    def __init__(self, idc_id: str, icode: str = None, label: str = None, parent_idc_id: str = None):
        self.idc_id = idc_id
        self.icode = icode
        self.label = label
        self.parent_idc_id = parent_idc_id

    @property
    def children(self) -> List["Concept"]:
        items = []
        for row in _cur.execute("SELECT idc_id, icode, label, parent_idc_id from cim11 where parent_idc_id = ?",
                                (self.idc_id,)):
            items.append(Concept(row[0], row[1], row[2], row[3]))
        return items

    @property
    def parent(self) -> Union["Concept", None]:
        for row in _cur.execute("SELECT idc_id, icode, label, parent_idc_id from cim11 where idc_id = ?",
                                (self.parent_idc_id,)):
            return Concept(row[0], row[1], row[2], row[3])


def root_concepts() -> List[Concept]:
    items = []
    for row in _cur.execute("SELECT idc_id, icode, label, parent_idc_id from cim11 where parent_idc_id is null"):
        if row[1] not in ["X", "V"]:
            items.append(Concept(row[0], row[1], row[2], row[3]))
    return items


def label_search(terms: str) -> List[Concept]:
    def fts_escape(user_input: str) -> str:
        wrds = []
        for wrd in user_input.split(" "):
            wrds.append('"' + wrd.replace('"', '""') + '"')
        return " ".join(wrds)

    terms = fts_escape(terms)
    items = []
    for row in _cur.execute(
            "SELECT idc_id, icode, label, parent_idc_id from cim11 where label match ? and icode is not null order by icode",
            (terms,)):
        if row[1] not in ["X", "V"]:
            items.append(Concept(row[0], row[1], row[2], row[3]))
    return items
