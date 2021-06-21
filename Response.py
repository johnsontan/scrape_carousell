def response(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "sup"):
        return "Hey! Hello.."
    
    return "Sorry, I do not understand you."

