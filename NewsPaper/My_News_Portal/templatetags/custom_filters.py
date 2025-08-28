from django import template
import re

register = template.Library()

BAD_WORDS = ["лохи", "дурак", "блин"]
@register.filter(name="censor")
def censor(value):
    if not isinstance(value, str):
        return value

    result = value
    for word in BAD_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        replacement = word[0] + "*" * (len(word) - 1)
        result = pattern.sub(replacement, result)
    return result