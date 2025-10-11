from typing import List
from ..services.note_service import NoteService

# Додає нову нотатку
def add_note(args: List[str], service: NoteService) -> str:
    if not args:
        # Перевірка наявності тексту для нотатки
        raise ValueError("Add-note command requires text argument")

    text = " ".join(args)  # Об'єднуємо аргументи в один рядок
    note_id = service.add_note(text)  # Додаємо нотатку через сервіс
    return f"Note added with ID: {note_id}"  # Повертаємо повідомлення з ID

# Відображає всі нотатки
def show_notes(args: List[str], service: NoteService) -> str:
    notes = service.get_all_notes()  # Отримуємо всі нотатки

    if not notes:
        # Якщо нотаток немає
        return "No notes found."

    lines = ["All notes:"]  # Список для збереження рядків виводу
    for note in notes:
        lines.append(f"ID: {note.id}")  # Додаємо ID нотатки
        lines.append(f"Text: {note.text}")  # Додаємо текст нотатки
        if note.tags:
            tags_str = ", ".join(str(tag) for tag in note.tags)  # Формуємо рядок тегів
            lines.append(f"Tags: {tags_str}")  # Додаємо теги
        lines.append("")  # Порожній рядок для розділення нотаток

    return "\n".join(lines)  # Повертаємо всі нотатки у вигляді рядка

# Редагує існуючу нотатку
def edit_note(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        # Перевірка наявності ID та нового тексту
        raise ValueError("Edit-note command requires 2 arguments: ID and new text")

    note_id = args[0]  # ID нотатки
    new_text = " ".join(args[1:])  # Новий текст нотатки

    return service.edit_note(note_id, new_text)  # Викликаємо метод редагування

# Видаляє нотатку за ID
def delete_note(args: List[str], service: NoteService) -> str:
    if not args:
        # Перевірка наявності ID
        raise ValueError("Delete-note command requires ID argument")

    note_id = args[0]  # ID нотатки
    return service.delete_note(note_id)  # Видаляємо нотатку через сервіс
