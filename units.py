# helpers.py

def generate_new_user_id(last_user):
    """Generate the next user ID based on the last user record."""
    return 1 if not last_user else last_user["User_id"] + 1


def borrow_logic(book):
    """Decrease available copies if possible, otherwise raise error."""
    if book["Available_copies"] > 0:
        return book["Available_copies"] - 1
    else:
        raise ValueError("No copies left")


def return_logic(book):
    """Increase available copies by 1 when returned."""
    return book["Available_copies"] + 1


def normalize_borrowed_item(item, books_lookup):
    """Normalize borrowed book info into {Book_id, Title} format."""
    if isinstance(item, dict) and "Book_id" in item:
        return {"Book_id": item["Book_id"], "Title": item.get("Title", "Unknown")}
    elif isinstance(item, str):
        return {"Book_id": books_lookup.get(item), "Title": item}
    return {"Book_id": None, "Title": str(item)}


def build_book_prompt(book):
    """Builds a Gemini AI prompt from a book record."""
    return f"Title: {book.get('Title', '')}, Authors: {', '.join(book.get('Authors', []))}"
