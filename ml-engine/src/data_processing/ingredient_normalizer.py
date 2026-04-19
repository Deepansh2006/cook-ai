import re

def clean_ingredient(text):
    """
    Normalize a single ingredient
    """

    text = text.lower()

    # remove numbers
    text = re.sub(r"\d+", "", text)

    # remove special characters except spaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    text = text.strip()

    return text


def parse_ingredients(ingredient_string):
    """
    Parse ingredient string like:
    c("tomato", "onion", "garlic")
    """

    if not isinstance(ingredient_string, str):
        return []

    # extract words inside quotes
    ingredients = re.findall(r'"(.*?)"', ingredient_string)

    cleaned = [clean_ingredient(i) for i in ingredients]

    return cleaned