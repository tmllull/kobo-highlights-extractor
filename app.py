import argparse

from kobo_highlights_extractor.extractor import KoboHighlightsExtractor

# Check if DB is passed
parser = argparse.ArgumentParser()
parser.add_argument("--db-file", type=str, default=None, help="db file")
parser.add_argument("--template", type=str, default=None, help="template file")
parser.add_argument(
    "--highlights-path",
    type=str,
    default=None,
    help="highlights path",
)
args = parser.parse_args()
db_file = args.db_file
template = args.template
highlights_path = args.highlights_path

extractor = KoboHighlightsExtractor(
    db_file=db_file, template=template, highlights_path=highlights_path
)
extractor.extract_highlights()
print("Done")
