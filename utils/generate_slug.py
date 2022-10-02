from .generate_random_string import generate_random_string
from slugify import slugify

def generate_slug(string):
    random_string = generate_random_string()
    if string != '':
        slug = slugify(string)
        return str(slug + "-" + random_string)
    else: return str(random_string)