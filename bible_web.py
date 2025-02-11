#!/usr/bin/env python
# vim: fileencoding=utf8
#
###
# (c) RePa
# public domain, csinalsz vele amit akarsz

from flask import Flask, jsonify, request, render_template, abort
from bible import get_random_line, get_bible_lines, get_book_number
from bible import get_next_line, bibleCache, session

app = Flask(__name__)
DEFAULT_LANG = 'hu'
LANGS = ['hu', 'en']


def getlang(lang):
    return lang if lang in LANGS else DEFAULT_LANG


def show_line(line, template_name='bibleline.html'):
    if line:
        if (request.headers['Content-Type'] == 'application/json'
                or request.args.get('json', False) is not False):
            return jsonify(line.as_dict())
        else:
            return render_template(template_name, line=line)
    else:
        abort(404)


@app.route("/prlx")
@app.route("/prlx/<lang>/")
def parallax_random_quote(lang=DEFAULT_LANG):
    """
    Display random bible quote
    """
    lang = getlang(lang)

    line = get_random_line(lang)
    return show_line(line, 'bibleline_parallax.html')


@app.route("/")
@app.route("/random/")
@app.route("/random/<lang>/")
def random_quote(lang=DEFAULT_LANG):
    """
    Display random bible quote
    """
    lang = getlang(lang)

    line = get_random_line(lang)
    return show_line(line)


@app.route("/<book>/<int:chapter>:<int:line>/")
@app.route("/<book>/<int:chapter>:<int:line>/<lang>")
@app.route("/<book>/<int:chapter>:<int:line>::<int:lineTo>/")
@app.route("/<book>/<int:chapter>:<int:line>::<int:lineTo>/<lang>")
def quote(book, chapter, line, lineTo=None, lang=DEFAULT_LANG):
    """
    Display a specific bible quote
    """
    lang = getlang(lang)
    book = get_book_number(book)

    lines = get_bible_lines(book, chapter, line, lineTo, lang, "<p>%s</p>")
    return show_line(lines)


@app.route("/next/<book>/<int:chapter>:<int:line>/")
@app.route("/next/<book>/<int:chapter>:<int:line>/<lang>")
def nextLine(book, chapter, line, lang=DEFAULT_LANG):
    """
    Display next line
    """
    lang = getlang(lang)
    book = get_book_number(book)

    nextLine = get_next_line(book, chapter, line, lang)
    return show_line(nextLine)


if __name__ == "__main__":
    bibleCache.fill(session)
    app.run('0.0.0.0', 7777)
