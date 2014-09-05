#!/usr/bin/env python
# vim: fileencoding=utf8
#
###
# (c) RePa
# public domain, csinalsz vele amit akarsz

from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Text, MetaData
from sqlalchemy.orm import mapper
import sys
import random

engine = create_engine('sqlite:///bible.sqlite')

metadata = MetaData()
bible_table = Table('bible_lines', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('book', Integer),
                    Column('chapter', Integer),
                    Column('line', Integer),
                    Column('language', String(4)),
                    Column('text', Text)
                    )

metadata.create_all(engine)


class BibleLine(object):
    def __init__(self, book, chapter, line, language, text, lineTo=None):
        self.id = None
        self.book = book
        self.chapter = chapter
        self.line = line
        self.language = language
        self.text = text
        self._lineTo = lineTo

    @property
    def bookname(self):
        return get_book_name(self.book, self.language)

    @property
    def lineTo(self):
        return getattr(self, '_lineTo', self.line)

    def __repr__(self):
        return "<BibleLine Book %s %s:%s-%s [%s]>" % (
            self.book,
            self.chapter,
            self.line,
            self.lineTo,
            self.language
        )

    def as_dict(self):
        return {
            "book": self.book,
            "bookname": self.bookname,
            "chapter": self.chapter,
            "line": self.line,
            "lineTo": self.lineTo,
            "language": self.language,
            "text": self.text
        }

    def __unicode__(self):
        return self.text

    def __str__(self):
        return u"%s" % self.text

mapper(BibleLine, bible_table)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

books = {
    'hu': {
        1: [u"Mózes I. könyve", "mozi", "moz1", "mozes i", "mozes 1", ],
        2: [u"Mózes II. könyve", "mozii", "moz2", "mozes ii", "mozes 2", ],
        3: [u"Mózes III. könyve", "moziii", "moz3", "mozes iii", "mozes 3", ],
        4: [u"Mózes IV. könyve", "moziv", "moz4", "mozes iv", "mozes 4", ],
        5: [u"Mózes V. könyve", "mozv", "moz5", "mozes v", "mozes 5", ],
        6: [u"Józsué könyve", "jozs", "jozsue", ],
        7: [u"Bírák könyve", "birak", ],
        8: [u"Ruth könyve", "ruth", ],
        9: [u"Sámuel I. könyve", "samuel i", "samuel 1", "sami", "sam1", ],
        10: [u"Sámuel II. könyve", "samuel ii", "samuel 2", "samii", "sam2", ],
        11: [u"Királyok I. könyve", "kiralyok 1", "kiralyok i", "kiri",
             "kir1", ],
        12: [u"Királyok II. könyve", "kiralyok 2", "kiralyok ii", "kirii",
             "kir2", ],
        13: [u"Krónika I. könyve", "kronika 1", "kronika i", "kroni",
             "kron1", ],
        14: [u"Krónika II. könyve", "kronika 2", "kronika ii", "kronii",
             "kron2", ],
        15: [u"Ezsdrás könyve", "ezsdras", "ezsd", ],
        16: [u"Nehémiás könyve", "nehemias", "nehe", ],
        17: [u"Eszter könyve", "eszter", "eszt", ],
        18: [u"Jób könyve", "job", ],
        19: [u"Zsoltárok könyve", "zsoltarok", "zsolt", ],
        20: [u"Példabeszédek", "peldabeszedek", "peld", ],
        21: [u"Prédikátor könyve", "predikatorok", "pred", ],
        22: [u"Énekek Éneke", "enekek", "enek", ],
        23: [u"Ésaiás próféta könyve", "esaias", "esa", ],
        24: [u"Jeremiás próféta könyve", "jeremias", "jer", "jer1", ],
        25: [u"Jeremiás siralmai", "siralmok", "jer2", ],
        26: [u"Ezékiel próféta könyve", "ezekiel", "ez", "ezek", ],
        27: [u"Dániel próféta könyve", "daniel", "dan", ],
        28: [u"Hóseás próféta könyve", "hoseas", "hos", ],
        29: [u"Jóel próféta könyve", "joel", ],
        30: [u"Ámós próféta könyve", "amos", ],
        31: [u"Abdiás próféta könyve", "abdias", "abd", ],
        32: [u"Jónás próféta könyve", "jonas", "jon", ],
        33: [u"Mikeás próféta könyve", "mikeas", "mik", ],
        34: [u"Náhum próféta könyve", "nahum", "nah", ],
        35: [u"Habakuk próféta könyve", "habakuk", "hab", ],
        36: [u"Sofóniás próféta könyve", "sofonias", "sof", ],
        37: [u"Aggeus próféta könyve", "aggeus", "agg", ],
        38: [u"Zakariás próféta könyve", "zakarias", "zak", ],
        39: [u"Malakiás próféta könyve", "malakias", "mal", ],
        40: [u"Máté Evangyélioma", "mate", "mt", "mat", ],
        41: [u"Márk Evangyélioma", "mark", "mrk", "mr", ],
        42: [u"Lukács Evangyélioma", "lukacs", "luk", ],
        43: [u"János Evangyélioma", "janos", "jan", ],
        44: [u"Apostolok Cselekedetei", "apostolok", "ap", ],
        45: [u"Rómabeliekhez írt levél", "romabeliekhez", "rom", "rm", ],
        46: [u"Korinthusbeliekhez írt I. levél", "kor1", "kori", ],
        47: [u"Korinthusbeliekhez írt II. levél", "kor2", "korii", ],
        48: [u"Galátziabeliekhez írt levél", "gal", ],
        49: [u"Efézusbeliekhez írt levél", "euf", ],
        50: [u"Filippibeliekhez írt levél", "fili", "fil", ],
        51: [u"Kolossébeliekhez írt levél", "kol", ],
        52: [u"Thessalonikabeliekhez írt I. levél", "thes1", "thesi", "th1",
             "thi", ],
        53: [u"Thessalonikabeliekhez írt II. levél", "thes2", "thesii", "th2",
             "thii", ],
        54: [u"Timótheushoz írt I. levél", "tim1", "timi", ],
        55: [u"Timótheushoz írt II. levél", "tim2", "timii", ],
        56: [u"Titushoz írt levél", "titus", "tit", ],
        57: [u"Filemonhoz írt levél", "filemon", "file", ],
        58: [u"Zsidókhoz írt levél", "zsidokhoz", "zsid", ],
        59: [u"Jakab Apostol levele", "jakab", "jak", ],
        60: [u"Péter Apostol I. levele", "peter1", "peteri", "pet1", "peti", ],
        61: [u"Péter Apostol II. levele", "peter2", "peterii", "pet2",
             "petii", ],
        62: [u"János Apostol I. levele", "jan1", "jani", "janos1", "janosi", ],
        63: [u"János Apostol II. levele", "jan2", "janii", "janos2",
             "janosii", ],
        64: [u"János Apostol III. levele", "jan3", "janiii", "janos3",
             "janosiii", ],
        65: [u"Júdás Apostol levele", "judas", "jud", ],
        66: [u"Jelenések könyve", "jelenesek", "jelen", "jel", ],
    },
    'en': {
        1: ["Genesis", ],
        2: ["Exodus", ],
        3: ["Leviticus", ],
        4: ["Numbers", ],
        5: ["Deuteronomy", ],
        6: ["Joshua", ],
        7: ["Judges", ],
        8: ["Ruth", ],
        9: ["1 Samuel", ],
        10: ["2 Samuel", ],
        11: ["1 Kings", ],
        12: ["2 Kings", ],
        13: ["1 Chronicles", ],
        14: ["2 Chronicles", ],
        15: ["Ezra", ],
        16: ["Nehemiah", ],
        17: ["Esther", ],
        18: ["Job", ],
        19: ["Psalms", ],
        20: ["Proverbs", ],
        21: ["Ecclesiastes", ],
        22: ["Song of Solomon", ],
        23: ["Isaiah", ],
        24: ["Jeremiah", ],
        25: ["Lamentations", ],
        26: ["Ezekiel", ],
        27: ["Daniel", ],
        28: ["Hosea", ],
        29: ["Joel", ],
        30: ["Amos", ],
        31: ["Obadiah", ],
        32: ["Jonah", ],
        33: ["Micah", ],
        34: ["Nahum", ],
        35: ["Habakkuk", ],
        36: ["Zephaniah", ],
        37: ["Haggai", ],
        38: ["Zechariah", ],
        39: ["Malachi", ],
        40: ["Matthew", ],
        41: ["Mark", ],
        42: ["Luke", ],
        43: ["John", ],
        44: ["Acts", ],
        45: ["Romans", ],
        46: ["1 Corinthians", ],
        47: ["2 Corinthians", ],
        48: ["Galatians", ],
        49: ["Ephesians", ],
        50: ["Philippians", ],
        51: ["Colossians", ],
        52: ["1 Thessalonians", ],
        53: ["2 Thessalonians", ],
        54: ["1 Timothy", ],
        55: ["2 Timothy", ],
        56: ["Titus", ],
        57: ["Philemon", ],
        58: ["Hebrews", ],
        59: ["James", ],
        60: ["1 Peter", ],
        61: ["2 Peter", ],
        62: ["1 John", ],
        63: ["2 John", ],
        64: ["3 John", ],
        65: ["Jude", ],
        66: ["Revelation", ]
    }
}


class BibleCache(object):

    def __init__(self):
        self.__cache = {
            "byid": {},
            "byline": {},
        }
        self.__filled = False

    @property
    def filled(self):
        return self.__filled

    def get_line_by_id(self, id):
        """
        Returns line by id
        - [line] if cached an exists
        - None not cached
        - False does not exist
        """

        return self.__cache["byid"].get(id, False if self.filled else None)

    def get_line(self, book, chapter, line, lang):
        """
        Returns line
        - [line] if cached an exists
        - None not cached
        - False does not exist
        """

        book = self.__cache["byline"].get(book, False if self.filled else None)

        if not book:
            return book

        chapter = book.get(chapter, False if self.filled else None)

        if not chapter:
            return chapter

        line = chapter.get(line, False if self.filled else None)

        if not line:
            return line

        langLine = line.get(lang, False if self.filled else None)

        return langLine

    def insert(self, line):

        if not line.id:
            return

        line.cached = True

        # add by id
        self.__cache["byid"][line.id] = line

        # add by line
        book = self.__cache["byline"].get(line.book)
        if not book:
            book = {}
            self.__cache["byline"][line.book] = book

        chapter = book.get(line.chapter)
        if not chapter:
            chapter = {}
            book[line.chapter] = chapter

        bline = chapter.get(line.line)
        if not bline:
            bline = {}
            chapter[line.line] = bline

        bline[line.language] = line

    def fill(self, session):
        lines = session.query(BibleLine).all()
        for line in lines:
            self.insert(line)

        self.__filled = True

    def get_random_line(self, lang):
        book = self.__cache["byline"].get(
            random.choice(self.__cache["byline"].keys()))
        chapter = book.get(random.choice(book.keys()))
        line = chapter.get(random.choice(chapter.keys()))

        return line.get(lang)


class BibleDAO(object):

    def __init__(self, session, cache):
        self.session = session
        self.cache = cache

    def get_line(self, book, chapter, line, lang):
        cline = self.cache.get_line(book, chapter, line, lang)
        if cline is not None:
            return cline

        line = session.query(BibleLine).filter(
            and_(BibleLine.book == book,
                 BibleLine.chapter == chapter,
                 BibleLine.line == line,
                 BibleLine.language == lang)
        ).first()

        self.cache.insert(line)
        return line

    def get_line_by_id(self, id):
        cline = self.cache.get_line_by_id(id)
        if cline is not None:
            return cline

        line = session.query(BibleLine).filter(BibleLine.id == id).one()

        self.cache.insert(line)
        return line


bibleCache = BibleCache()
bibleDao = BibleDAO(session, bibleCache)


def get_bible_line_by_id(id):
    return bibleDao.get_line_by_id(id)


def get_bible_line(book, chapter, line, lang='hu'):
    return bibleDao.get_line(book, chapter, line, lang)


def get_next_line(book, chapter, line, lang='hu'):
    line = bibleDao.get_line(book, chapter, line+1, lang)

    if not line:
        line = bibleDao.get_line(book, chapter+1, 1, lang)

    if not line:
        line = bibleDao.get_line(book+1, 1, 1, lang)

    if not line:
        line = bibleDao.get_line(1, 1, 1, lang)

    return line


def get_random_line(lang='hu'):

    if bibleCache.filled:
        line = bibleCache.get_random_line(lang)
    else:
        ids = session.query(BibleLine.id).filter(BibleLine.language == lang)
        count = ids.count()

        id = ids[random.randint(0, count-1)][0]

        line = get_bible_line_by_id(id)

    return line


def get_random_quote(lang='hu'):
    line = get_random_line(lang)
    bookname = get_book_name(line.book, lang)
    quotestr = u"%s (%s %s:%s)" % (
        line.text.strip(),
        bookname,
        line.chapter,
        line.line
    )

    return quotestr


def get_bible_lines(book, chapter, line, lineTo=None, lang='hu', wrapper="%s"):
    if lineTo is None:
        lineTo = line

    lines = []
    quote = None
    for i in range(line, lineTo+1):
        bline = get_bible_line(book, chapter, i, lang)
        if not bline:
            break
        lines.append(bline)

    if len(lines):
        firstline = lines[0]
        lastline = lines[-1]
        quote = BibleLine(
            firstline.book,
            firstline.chapter,
            firstline.line,
            firstline.language,
            "\n".join([wrapper % ln.text for ln in lines]),
            lastline.line
        )

    return quote


def get_book_name(booknr, lang='hu'):
    return books[lang][booknr][0]


def get_book_number(book):
    if book.isdigit():
        return int(book)

    for nr in books['hu']:
        if book.lower() in books['hu'][nr]:
            return nr

    return 0


def bible_quote(book, chapter, lines, lang='hu', info=True):
    booknr = get_book_number(book)
    bookname = get_book_name(booknr, lang)
    txt = ""

    for line in lines:
        txt += "%s\n" % get_bible_line(booknr, chapter, line, lang)

    if info:
        if len(lines) == 1:
            linestr = "%s" % lines[0]
        else:
            linestr = "%s-%s" % (lines[0], lines[-1])

        quotestr = u"%s (%s %s:%s)" % (txt.strip(), bookname, chapter, linestr)
    else:
        quotestr = u"%s" % txt

    return quotestr


def help():
    print "Usage: %s <book> <chapter>:<line>[-line_to] [language]" % sys.argv[0]
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        help()

    try:
        book = sys.argv[1]
        chapter_line = sys.argv[2]
        if len(sys.argv) > 3:
            lang = sys.argv[3]
        else:
            lang = 'hu'

        (chapter, line) = chapter_line.split(':')
        line_fromto = line.split('-')

        if len(line_fromto) > 1:
            line_from = int(line_fromto[0])
            line_to = int(line_fromto[1])
            lines = range(line_from, line_to+1)
        else:
            lines = [int(line_fromto[0])]

        quote = bible_quote(book, int(chapter), lines, lang, True)
    except:
        help()

    print quote,
