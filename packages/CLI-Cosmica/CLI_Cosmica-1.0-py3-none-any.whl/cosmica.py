import eel

def output(text):
    formatted_text = text.format()
    eel.appendOutput(formatted_text)

@staticmethod
def isSet(value):
    try:
        _ = value
        return True
    except (IndexError, TypeError):
        return False