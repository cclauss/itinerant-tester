    publishers = {publisher.casefold() for publisher in book_item["publishers"]}
    book_title = book_item["title"].casefold()  # should we .split() ?
    if low_quality := "notebook" in book_title and publishers & LOW_QUALITY_PUBLISHERS:
        return bool(low_quality)
    """
    A recent independently published book with these key words in its title (regardless
    of case)is also considered a low quality book.
    """
    created_year = int(book_item.get("created", "0")[:4])  # YYYY
    return "independently published" in publishers and created_year >= 2018 and any(
                title in book_title for title in ("annotated", "annoté", "illustrated")
            )

# ===========

    book["publishers"] = ["razal", "tobias publishing", "koraya", "pickleball", "d"]
    assert is_low_quality_book(book) is True, book

    book = {
        "title": "A aNNotaTEd Z",
        "publishers": ["Independently Published"],
        "created": "2017-09-01T05:14:17",
    }
    assert is_low_quality_book(book) is False, book
    book["created"] = "2018"
    assert is_low_quality_book(book) is True, book
    book["publishers"] = ["Independently Publish"]
    assert is_low_quality_book(book) is False, book
    book["publishers"] += ["Independently Published"]
    assert is_low_quality_book(book) is True, book
    book["title"] = "A aNNotaTE Z"
    assert is_low_quality_book(book) is False, book
