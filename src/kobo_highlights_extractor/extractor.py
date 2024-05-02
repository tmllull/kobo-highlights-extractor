# -*- coding: utf-8 -*-
import os
import sqlite3
import sys

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

TEMPLATE = """
# {{ book_data['book_title'] }}

{% for chapter in book_data['chapters'] %}

## {{ chapter['chapter_title'] }}

{% for highlight in chapter['highlights'] %}

> {{ highlight['highlight'].strip() }}

{% if highlight['note'] is not none and highlight['note'] != "" %}
Note: {{ highlight['note'] }}
{% endif %}

Progress: {{ highlight['chapter_progress'] }} %
Date: {{ highlight['date'] }}

---

{% endfor %}
{% endfor %}
"""


class KoboHighlightsExtractor:
    def __init__(self, db_file=None, template=None, highlights_path=None):
        if db_file is None:
            print("Using default sqlite database...")
            db_file = "KoboReader.sqlite"
        else:
            print("Using provided sqlite database:", str(db_file), "...")
        connection = sqlite3.connect(db_file)
        self.cursor = connection.cursor()
        if template is None:
            print("Using default template...")
            self.template = Template(TEMPLATE)
        else:
            print("Using provided template:", str(template), "...")
            with open(template, "r") as file:
                template_content = file.read()
            self.template = Template(template_content)
        if highlights_path is None:
            self.highlights_path = "highlights/"
        else:
            self.highlights_path = highlights_path + "/"

    def get_books(self):
        books = []
        for row in self.cursor.execute(
            "SELECT DISTINCT BookID, BookTitle FROM content"
        ):
            book = {}
            if row[0] is not None:
                book["id"] = row[0]
                book["title"] = row[1]
                books.append(book)
        return books

    def get_chapters(self, book_id):
        chapters = []
        for row in self.cursor.execute(
            "SELECT ContentID, Title FROM content WHERE BookID = ? ORDER BY VolumeIndex ASC",
            (book_id,),
        ):
            chapter = {}
            if row[0] is not None:
                chapter["id"] = row[0]
                chapter["title"] = row[1]
                chapters.append(chapter)
        return chapters

    def get_highlights(self, chapter_id):
        highlights = []
        query = (
            "SELECT "
            + "VolumeID, ContentID, Text, Annotation, DateCreated, ChapterProgress FROM Bookmark WHERE (Type = 'highlight' OR Type = 'note') AND ContentID = "
            + "?"
            + " ORDER BY DateCreated ASC"
        )
        for row in self.cursor.execute(query, (chapter_id,)):
            highlight = {}
            highlight["book_id"] = row[0]
            highlight["content_id"] = row[1]
            highlight["text"] = row[2]
            highlight["note"] = row[3]
            highlight["date"] = row[4].split("T")[0]
            highlight["chapter_progress"] = row[5]
            highlights.append(highlight)
        return highlights

    def highlight_page(self, chapter_start_page, chapter_pages, percent):
        pages_read = (percent * chapter_pages) / 1
        return "{:.2f}".format(chapter_start_page + pages_read)

    def prepare_highlight(self, highlight):
        highlight_info = {}
        highlight_info["highlight"] = highlight["text"]
        highlight_info["note"] = highlight["note"]
        chapter_progress = round((highlight["chapter_progress"] * 100), 2)
        if chapter_progress.is_integer():
            chapter_progress = int(chapter_progress)
        highlight_info["chapter_progress"] = chapter_progress
        highlight_info["date"] = highlight["date"]
        return highlight_info

    def extract_highlights(self):
        # Create highlights folder if not exists
        if not os.path.exists(self.highlights_path):
            os.makedirs(self.highlights_path)

        books = self.get_books()
        books_highlights = []

        # Save highlight in md files
        for book in books:
            book_highlights = {}
            book_highlights["book_title"] = book["title"]
            book_highlights["chapters"] = []
            chapters = self.get_chapters(book["id"])
            for chapter in chapters:
                highlights = self.get_highlights(chapter["id"])
                if len(highlights) == 0:
                    continue
                chapter_info = {}
                chapter_info["chapter_title"] = chapter["title"]
                chapter_info["highlights"] = []
                for highlight in highlights:
                    highlight_info = self.prepare_highlight(highlight)
                    chapter_info["highlights"].append(highlight_info)
                book_highlights["chapters"].append(chapter_info)
                books_highlights.append(book_highlights)
        for book_data in books_highlights:
            try:
                rendered_content = self.template.render(book_data=book_data)
                with open(
                    self.highlights_path + book_data["book_title"] + ".md", "wb"
                ) as f:
                    f.write(rendered_content.encode("utf-8"))
            except Exception as e:
                print(e)
