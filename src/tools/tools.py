from src.flashcard.storage import FlashcardStorage

# Initialize storage
storage = FlashcardStorage()

# --- Define execution functions (Functions) ---

def list_sets_func():
    try:
        sets = storage.list_sets()
        if not sets:
            return "No flashcard sets available yet."
        return "\n".join([f"- {s.name} ({len(s.cards)} cards)" for s in sets])
    except Exception as e:
        return f"Error: {str(e)}"

def create_set_func(set_name: str):
    try:
        storage.create_set(set_name)
        return f"Flashcard set '{set_name}' created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def add_card_func(set_name: str, front: str, back: str):
    try:
        # You can extend with synonyms if needed
        storage.add_card(set_name, front, back)
        return f"Added word '{front}' to set '{set_name}'."
    except Exception as e:
        return f"Error: {str(e)}"

def list_cards_func(set_name: str):
    try:
        cards = storage.list_cards(set_name)
        if not cards:
            return f"Set '{set_name}' is empty."
        return "\n".join([f"{c.front}: {c.back}" for c in cards])
    except Exception as e:
        return f"Error: {str(e)}"

# --- Tool definitions ---

tools = [
    {
        "name": "list_flashcard_sets",
        "description": "List all available flashcard sets.",
        "func": list_sets_func
    },
    {
        "name": "create_flashcard_set",
        "description": "Create a new flashcard set. Parameters: set_name (name of the set).",
        "func": create_set_func
    },
    {
        "name": "add_card_to_set",
        "description": "Add a new flashcard (word and meaning). Parameters: set_name, front (English), back (Vietnamese).",
        "func": add_card_func
    },
    {
        "name": "list_cards_in_set",
        "description": "View all cards in a flashcard set. Parameter: set_name.",
        "func": list_cards_func
    }
]