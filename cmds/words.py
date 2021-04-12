import os

def words(message):
    sec = os.environ['words']
    words = sec.split(', ')
    variable = any(msg in message for msg in words)
    return variable