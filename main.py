from scraper import get_reviews
from save import save_file

reviews = get_reviews()
save_file(reviews)