async def get_category_of_resource(mime_type: str) -> str:
    if "video" in mime_type:
        return "video"

    if "image" in mime_type:
        return "image"

    if "font" in mime_type:
        return "font"

    if "css" in mime_type:
        return "css"

    if "javascript" in mime_type:
        return "javascript"

    return "other"
