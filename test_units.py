import pytest # type: ignore
from units import (
    generate_new_user_id,
    borrow_logic,
    return_logic,
    normalize_borrowed_item,
    build_book_prompt,
)

# ---------- generate_new_user_id ----------
def test_generate_new_user_id_first():
    assert generate_new_user_id(None) == 1

def test_generate_new_user_id_next():
    assert generate_new_user_id({"User_id": 5}) == 6


# ---------- borrow_logic ----------
def test_borrow_logic_success():
    book = {"Available_copies": 3}
    assert borrow_logic(book) == 2

def test_borrow_logic_failure():
    book = {"Available_copies": 0}
    with pytest.raises(ValueError, match="No copies left"):
        borrow_logic(book)


# ---------- return_logic ----------
def test_return_logic():
    book = {"Available_copies": 2}
    assert return_logic(book) == 3


# ---------- normalize_borrowed_item ----------
def test_normalize_dict_item():
    item = {"Book_id": 1, "Title": "Book A"}
    assert normalize_borrowed_item(item, {}) == {"Book_id": 1, "Title": "Book A"}

def test_normalize_string_item_found():
    lookup = {"Book B": 2}
    assert normalize_borrowed_item("Book B", lookup) == {"Book_id": 2, "Title": "Book B"}

def test_normalize_string_item_not_found():
    assert normalize_borrowed_item("Unknown", {}) == {"Book_id": None, "Title": "Unknown"}


# ---------- build_book_prompt ----------
def test_build_book_prompt():
    book = {"Title": "1984", "Authors": ["George Orwell"]}
    prompt = build_book_prompt(book)
    assert "1984" in prompt
    assert "George Orwell" in prompt
