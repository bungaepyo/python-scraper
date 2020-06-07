import csv


def save_file(reviews):
    file = open("reviews.csv", mode='w')
    writer = csv.writer(file)
    writer.writerow(['Name', 'Rating', 'Number of Reviews', 'Price', 'Tag'])
    for review in reviews:
        writer.writerow(review.values())
    return
