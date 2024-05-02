# Description

With this script you can get the highlights from Kobo reader using the sqlite file. The reason I made it is because when you export the highlights, a basic information as the page where are located is not exported. Oh, thanks, Kobo, for this useless option. When I highlight something usually I want to reference in other place, so maybe I need to search in the original content to expand the context.

## Basic Usage

To run the basic usage, you just need to clone this repo and follow the next steps:

1. Export the `KoboReader.sqlite` file from your Kobo and place it in the root path where this code has been downloaded.
2. Run `pip install .` or `pip install --upgrade .`
3. Run `python app.py`

All the highlights will be extracted and saved in an .md file with the name of the book, into a `highlights` folder, and with the follow structure:

```
# Title

## Chapter 1

Lorem Ipsum

Progress: Position progress on chapter
Date: date when the highlight was highlighted

---

Lorem Ipsum2

Progress: Position progress on chapter
Date: date when the highlight was highlighted

## Chapter B

Lorem Ipsum

Note: A note 

Progress: Position progress on chapter
Date: date when the highlight was highlighted

...
```
## Advanced usage
This script accepts some parameters to use in a more advanced usage:

- `--db-file`: if your .sqlite file has another name, you can specify it with this param
- `--template`: if you want to use another template, you can pass it using this param. Please, use the template at the end as example to know what variables you can use.
- `--highlights-path`: if you want to put the exported highlights in another place, you can specify it with this param.

### Basic template
```md
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
```