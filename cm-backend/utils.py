from datetime import datetime

valid_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo",
                "mistral-large-latest", "mistral-small-latest", "open-mistral-7b"]
valid_extensions = [".gif", ".jpeg", ".pdf", ".png", ".svg"]
valid_contexts = ["default", "wiki-text", "scientific", "mathematical"]


def create_timestamp_str():
    stamp = datetime.now()
    stamp_str = stamp.strftime("%d-%m-%Y_%H-%M-%S")

    return stamp_str


def check_if_txt(filename):
    return filename.endswith(".txt") or filename.endswith(".tex") or filename.endswith(".md")


def check_extension(extension):
    return extension in valid_extensions


def get_mediatype(extension):
    if "pdf" in extension:
        return "application/pdf"

    if "svg" in extension:
        return "image/svg+xml"

    return f"image/{extension[1:]}"


def check_context(context):
    return context in valid_contexts


def check_model(model_name):
    return model_name in valid_models
