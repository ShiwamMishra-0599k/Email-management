from better_profanity import profanity


profanity.load_censor_words()

def check_profanity_in_email(body: str) -> tuple[bool, str]:
    """
    Checks for profanity in the given email body.

    Returns:
        - contains_profanity (bool): True if profanity is detected.
        - profane_text (str): The first profane word found, or 'None'.
    """
    words = body.split()
    for word in words:
        if profanity.contains_profanity(word):
            return True, word  

    return False, "None"
