"""
Gradio Web UI for Assistant Bot

Run with: python src/web/gradio_app.py
Or: PYTHONPATH=. python src/web/gradio_app.py
"""

import gradio as gr
from pathlib import Path
from typing import Optional, Tuple

from src.domain.value_objects import Email, Phone, Address, Name, Tag, Birthday
from src.infrastructure.storage.storage_factory import StorageFactory
from src.infrastructure.storage.storage_type import StorageType
from src.infrastructure.storage.json_storage import JsonStorage
from src.infrastructure.persistence.data_path_resolver import DEFAULT_JSON_FILE, DEFAULT_NOTES_FILE
from src.application.services.note_service import NoteService
from src.application.services.contact_service import ContactService


# Initialize services with project's data directory
# Use project's data/ folder instead of home directory
project_root = Path(__file__).parent.parent.parent
data_dir = project_root / "data"
data_dir.mkdir(exist_ok=True)

storage_type = StorageType.JSON
storage = JsonStorage(data_dir=data_dir)  # Use project's data/ folder
contact_service = ContactService(storage)
note_service = NoteService(storage)

# Load existing data
try:
    contact_service.load_address_book(DEFAULT_JSON_FILE, user_provided=True)
except Exception:
    pass  # Start with empty address book if load fails

try:
    note_service.load_notes(DEFAULT_NOTES_FILE)
except Exception:
    pass  # Start with empty notes if load fails


# Contact Management Functions
def add_contact_ui(name: str, phone: str) -> str:
    """Add a new contact"""
    if not name or not phone:
        return ""
    try:
        result = contact_service.add_contact(Name(name), Phone(phone))
        contact_service.save_address_book()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def remove_contact_ui(name: str) -> str:
    """Remove a contact"""
    if not name:
        return ""
    try:
        result = contact_service.delete_contact(name)
        contact_service.save_address_book()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def add_email_ui(name: str, email: str) -> str:
    """Add email to contact"""
    if not name or not email:
        return ""
    try:
        result = contact_service.add_email(name, Email(email))
        contact_service.save_address_book()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def add_address_ui(name: str, address: str) -> str:
    """Add address to contact"""
    if not name or not address:
        return ""
    try:
        result = contact_service.add_address(name, Address(address))
        contact_service.save_address_book()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def add_birthday_ui(name: str, birthday: str) -> str:
    """Add birthday to contact (format: DD.MM.YYYY)"""
    if not name or not birthday:
        return ""
    try:
        result = contact_service.add_birthday(name, Birthday(birthday))
        contact_service.save_address_book()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def search_contacts_ui(query: str) -> str:
    """Search contacts by name or phone"""
    try:
        results = contact_service.search(query)
        if not results:
            return "No contacts found"

        output = []
        for contact in results:
            output.append(f"📇 {contact.name}")
            if contact.phones:
                phones_str = ", ".join(str(phone) for phone in contact.phones)
                output.append(f"   📞 {phones_str}")
            if contact.email:
                output.append(f"   📧 {contact.email}")
            if contact.address:
                output.append(f"   🏠 {contact.address}")
            if contact.birthday:
                output.append(f"   🎂 {contact.birthday}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def list_all_contacts_ui() -> str:
    """List all contacts"""
    try:
        contacts = contact_service.get_all_contacts()
        if not contacts:
            return "No contacts in address book"

        output = [f"📇 Total contacts: {len(contacts)}\n"]
        for contact in contacts:
            phones_str = ", ".join(str(phone) for phone in contact.phones) if contact.phones else "No phone"
            output.append(f"• {contact.name} - {phones_str}")
            if contact.email:
                output.append(f"  📧 {contact.email}")
            if contact.birthday:
                output.append(f"  🎂 {contact.birthday}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_birthdays_ui(days: int = 7) -> str:
    """Get upcoming birthdays"""
    try:
        birthdays = contact_service.get_upcoming_birthdays(days)
        if not birthdays:
            return f"No birthdays in the next {days} days"

        output = [f"🎂 Upcoming birthdays (next {days} days):\n"]
        for birthday_info in birthdays:
            output.append(f"• {birthday_info['name']}")
            output.append(f"  Birthday: {birthday_info['birthday']}")
            output.append(f"  Date: {birthday_info['congratulation_date']}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Note Management Functions
def add_note_ui(text, tags=""):
    """Add a new note (tags: comma-separated)"""
    if not text:
        return ""
    try:
        # Handle different input types for tags
        if isinstance(tags, list):
            # If it's already a list, join it
            tags_str = ",".join(str(t) for t in tags)
        elif isinstance(tags, str):
            tags_str = tags
        else:
            tags_str = str(tags) if tags else ""

        # Parse tags
        tag_list = []
        if tags_str:
            tag_list = [Tag(t.strip()) for t in tags_str.split(",") if t.strip()]

        # Use first line as title, rest as text (or use same for both)
        lines = text.strip().split('\n', 1)
        title = lines[0][:50]  # First line or first 50 chars as title
        note_text = text

        note_id = note_service.add_note(title, note_text)

        # Add tags to the created note
        for tag in tag_list:
            note_service.add_tag(note_id, tag)

        note_service.save_notes()
        return f"✅ Note added with ID: {note_id}"
    except Exception as e:
        import traceback
        return f"❌ Error: {str(e)}\n{traceback.format_exc()}"


def search_notes_ui(query: str) -> str:
    """Search notes by text or tags"""
    try:
        # Search both by content and title
        results = note_service.search_notes_by_content(query)
        if not results:
            results = note_service.search_notes_by_title(query)
        if not results:
            return "No notes found"

        output = []
        for note in results:
            output.append(f"📝 Note ID: {note.id}")
            output.append(f"   Title: {note.title}")
            output.append(f"   {note.text[:100]}{'...' if len(note.text) > 100 else ''}")
            if note.tags:
                tags_str = ", ".join(str(tag) for tag in note.tags)
                output.append(f"   🏷️  {tags_str}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def list_all_notes_ui() -> str:
    """List all notes"""
    try:
        notes = note_service.get_all_notes()
        if not notes:
            return "No notes found"

        output = [f"📝 Total notes: {len(notes)}\n"]
        for note in notes:
            output.append(f"ID: {note.id}")
            output.append(f"   {note.text[:100]}{'...' if len(note.text) > 100 else ''}")
            if note.tags:
                tags_str = ", ".join(str(tag) for tag in note.tags)
                output.append(f"   🏷️  {tags_str}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def delete_note_ui(note_id: str) -> str:
    """Delete a note by ID"""
    if not note_id:
        return ""
    try:
        result = note_service.delete_note_by_id(note_id)
        note_service.save_notes()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def add_tag_to_note_ui(note_id: str, tag: str) -> str:
    """Add a tag to an existing note"""
    if not note_id or not tag:
        return ""
    try:
        result = note_service.add_tag(note_id, Tag(tag))
        note_service.save_notes()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def remove_tag_from_note_ui(note_id: str, tag: str) -> str:
    """Remove a tag from a note"""
    if not note_id or not tag:
        return ""
    try:
        result = note_service.remove_tag(note_id, Tag(tag))
        note_service.save_notes()
        return f"✅ {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def search_by_tags_ui(tags: str) -> str:
    """Search notes by tags (comma-separated)"""
    try:
        tags_str = tags if isinstance(tags, str) else ""
        if not tags_str:
            return "Please enter at least one tag"

        # Search by first tag (service only supports single tag search)
        first_tag = tags_str.split(",")[0].strip()
        results = note_service.search_notes_by_tag(first_tag)
        if not results:
            return f"No notes found with tag: {first_tag}"

        output = []
        for note in results:
            output.append(f"📝 Note ID: {note.id}")
            output.append(f"   Title: {note.title}")
            output.append(f"   {note.text[:100]}{'...' if len(note.text) > 100 else ''}")
            if note.tags:
                tags_display = ", ".join(str(tag) for tag in note.tags)
                output.append(f"   🏷️  {tags_display}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Build Gradio Interface
def create_ui():
    """Create the Gradio interface with tabs"""

    # Custom theme with very light, clean colors
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="gray",
        spacing_size="lg",
        radius_size="md",
    ).set(
        body_background_fill="#f8f9fa",
        body_text_color="#2c3e50",
        block_background_fill="white",
        block_border_width="1px",
        block_border_color="#e9ecef",
        block_padding="20px",
        block_shadow="0 1px 3px rgba(0,0,0,0.05)",
        button_primary_background_fill="#4a90e2",
        button_primary_background_fill_hover="#357abd",
        button_primary_text_color="white",
        button_secondary_background_fill="white",
        button_secondary_background_fill_hover="#f1f3f5",
        button_secondary_border_color="#dee2e6",
        button_secondary_text_color="#495057",
        input_background_fill="white",
        input_border_color="#dee2e6",
        input_border_width="1px",
        input_shadow="0 1px 2px rgba(0,0,0,0.05)",
    )

    with gr.Blocks(title="Assistant Bot", theme=theme, css="""
        .gradio-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
            padding: 2rem !important;
        }
        .status-message {
            font-size: 0.9em;
            padding: 12px 16px;
            border-radius: 6px;
            background-color: #e7f3ff;
            border-left: 3px solid #4a90e2;
        }
        .status-message p {
            color: #2c3e50 !important;
            margin: 0 !important;
        }
        h1, h2 {
            color: #2c3e50 !important;
            font-weight: 600 !important;
        }
        h3 {
            color: white !important;
            font-weight: 600 !important;
        }
        .gr-textbox h3, .gr-textbox p {
            color: #2c3e50 !important;
        }
        .gr-group {
            margin-bottom: 2rem !important;
            padding: 1.5rem !important;
        }
        .gr-button {
            font-weight: 500 !important;
            border-radius: 6px !important;
        }
        .gr-input {
            border-radius: 6px !important;
        }
        .tabs {
            margin-top: 1.5rem !important;
        }
    """) as app:
        with gr.Row():
            with gr.Column():
                gr.Markdown("# 🤖 Assistant Bot")
                gr.Markdown("*Manage your contacts and notes with ease*")

        gr.Markdown("")  # Spacer

        with gr.Tabs():
            # === CONTACTS TAB ===
            with gr.Tab("📇 Contacts"):

                # Add new contact section
                with gr.Group():
                    gr.Markdown("### ➕ Add New Contact")
                    with gr.Row():
                        name_input = gr.Textbox(label="Name", placeholder="John Doe", scale=2)
                        phone_input = gr.Textbox(label="Phone", placeholder="+1234567890", scale=2)
                        add_btn = gr.Button("Add Contact", variant="primary", scale=1)
                    add_output = gr.Markdown(visible=False, elem_classes="status-message")
                    add_btn.click(
                        lambda n, p: (add_contact_ui(n, p), gr.update(visible=True) if n and p else gr.update(visible=False)),
                        inputs=[name_input, phone_input],
                        outputs=[add_output, add_output]
                    )

                # Update contact details
                with gr.Group():
                    gr.Markdown("### ✏️ Update Contact Details")
                    with gr.Row():
                        with gr.Column():
                            email_name = gr.Textbox(label="Contact Name", placeholder="John Doe")
                            email_input = gr.Textbox(label="Email", placeholder="john@example.com")
                            email_btn = gr.Button("Add Email")
                            email_output = gr.Markdown(visible=False, elem_classes="status-message")
                            email_btn.click(
                                lambda n, e: (add_email_ui(n, e), gr.update(visible=True) if n and e else gr.update(visible=False)),
                                inputs=[email_name, email_input],
                                outputs=[email_output, email_output]
                            )

                        with gr.Column():
                            bday_name = gr.Textbox(label="Contact Name", placeholder="John Doe")
                            bday_input = gr.Textbox(label="Birthday", placeholder="DD.MM.YYYY")
                            bday_btn = gr.Button("Add Birthday")
                            bday_output = gr.Markdown(visible=False, elem_classes="status-message")
                            bday_btn.click(
                                lambda n, b: (add_birthday_ui(n, b), gr.update(visible=True) if n and b else gr.update(visible=False)),
                                inputs=[bday_name, bday_input],
                                outputs=[bday_output, bday_output]
                            )

                    with gr.Row():
                        addr_name = gr.Textbox(label="Contact Name", placeholder="John Doe", scale=1)
                        addr_input = gr.Textbox(label="Address", placeholder="123 Main St, City", scale=2)
                        addr_btn = gr.Button("Add Address", scale=1)
                    addr_output = gr.Markdown(visible=False, elem_classes="status-message")
                    addr_btn.click(
                        lambda n, a: (add_address_ui(n, a), gr.update(visible=True) if n and a else gr.update(visible=False)),
                        inputs=[addr_name, addr_input],
                        outputs=[addr_output, addr_output]
                    )

                # Search and view
                with gr.Group():
                    gr.Markdown("### 🔍 Search & View")
                    with gr.Row():
                        with gr.Column():
                            search_input = gr.Textbox(label="Search", placeholder="Name or phone number")
                            search_btn = gr.Button("🔍 Search", variant="secondary")
                            search_output = gr.Textbox(label="", lines=12, show_label=False)
                            search_btn.click(search_contacts_ui, inputs=search_input, outputs=search_output)

                        with gr.Column():
                            gr.Markdown("**All Contacts**")
                            list_btn = gr.Button("📋 Show All Contacts", variant="secondary")
                            list_output = gr.Textbox(label="", lines=12, show_label=False)
                            list_btn.click(list_all_contacts_ui, outputs=list_output)

                # Birthdays and delete
                with gr.Row():
                    with gr.Column():
                        with gr.Group():
                            gr.Markdown("### 🎂 Upcoming Birthdays")
                            days_input = gr.Slider(minimum=1, maximum=365, value=7, step=1, label="Days ahead")
                            birthday_btn = gr.Button("Show Birthdays")
                            birthday_output = gr.Textbox(label="", lines=6, show_label=False)
                            birthday_btn.click(get_birthdays_ui, inputs=days_input, outputs=birthday_output)

                    with gr.Column():
                        with gr.Group():
                            gr.Markdown("### 🗑️ Remove Contact")
                            remove_name = gr.Textbox(label="Contact Name", placeholder="John Doe")
                            remove_btn = gr.Button("Delete Contact", variant="stop")
                            remove_output = gr.Markdown(visible=False, elem_classes="status-message")
                            remove_btn.click(
                                lambda n: (remove_contact_ui(n), gr.update(visible=True) if n else gr.update(visible=False)),
                                inputs=remove_name,
                                outputs=[remove_output, remove_output]
                            )

            # === NOTES TAB ===
            with gr.Tab("📝 Notes"):

                # Add note section
                with gr.Group():
                    gr.Markdown("### ➕ Add New Note")
                    note_text = gr.Textbox(label="Note Text", lines=4, placeholder="Enter your note...")
                    note_tags = gr.Textbox(label="Tags (optional, comma-separated)", placeholder="work, important")
                    add_note_btn = gr.Button("Add Note", variant="primary")
                    add_note_output = gr.Markdown(visible=False, elem_classes="status-message")
                    add_note_btn.click(
                        lambda t, tgs: (add_note_ui(t, tgs), gr.update(visible=True) if t else gr.update(visible=False)),
                        inputs=[note_text, note_tags],
                        outputs=[add_note_output, add_note_output]
                    )

                # Manage tags
                with gr.Group():
                    gr.Markdown("### 🏷️ Manage Tags")
                    with gr.Row():
                        tag_note_id = gr.Textbox(label="Note ID", scale=1)
                        tag_input = gr.Textbox(label="Tag", scale=2)
                        with gr.Column(scale=1):
                            add_tag_btn = gr.Button("Add Tag")
                            remove_tag_btn = gr.Button("Remove Tag")
                    tag_output = gr.Markdown(visible=False, elem_classes="status-message")

                    add_tag_btn.click(
                        lambda n, t: (add_tag_to_note_ui(n, t), gr.update(visible=True) if n and t else gr.update(visible=False)),
                        inputs=[tag_note_id, tag_input],
                        outputs=[tag_output, tag_output]
                    )
                    remove_tag_btn.click(
                        lambda n, t: (remove_tag_from_note_ui(n, t), gr.update(visible=True) if n and t else gr.update(visible=False)),
                        inputs=[tag_note_id, tag_input],
                        outputs=[tag_output, tag_output]
                    )

                # Search and view
                with gr.Group():
                    gr.Markdown("### 🔍 Search & View")
                    with gr.Row():
                        with gr.Column():
                            search_note_input = gr.Textbox(label="Search by text", placeholder="Enter search term")
                            search_note_btn = gr.Button("🔍 Search", variant="secondary")
                            search_note_output = gr.Textbox(label="", lines=10, show_label=False)
                            search_note_btn.click(search_notes_ui, inputs=search_note_input, outputs=search_note_output)

                        with gr.Column():
                            search_tags_input = gr.Textbox(label="Search by tags", placeholder="work, important")
                            search_tags_btn = gr.Button("🏷️ Search by Tags", variant="secondary")
                            search_tags_output = gr.Textbox(label="", lines=10, show_label=False)
                            search_tags_btn.click(search_by_tags_ui, inputs=search_tags_input, outputs=search_tags_output)

                # View all and delete
                with gr.Row():
                    with gr.Column():
                        with gr.Group():
                            gr.Markdown("### 📋 All Notes")
                            list_notes_btn = gr.Button("Show All Notes", variant="secondary")
                            list_notes_output = gr.Textbox(label="", lines=12, show_label=False)
                            list_notes_btn.click(list_all_notes_ui, outputs=list_notes_output)

                    with gr.Column():
                        with gr.Group():
                            gr.Markdown("### 🗑️ Delete Note")
                            del_note_id = gr.Textbox(label="Note ID", placeholder="Enter note ID")
                            del_note_btn = gr.Button("Delete Note", variant="stop")
                            del_note_output = gr.Markdown(visible=False, elem_classes="status-message")
                            del_note_btn.click(
                                lambda n: (delete_note_ui(n), gr.update(visible=True) if n else gr.update(visible=False)),
                                inputs=del_note_id,
                                outputs=[del_note_output, del_note_output]
                            )

            # === ABOUT TAB ===
            with gr.Tab("ℹ️ About"):
                gr.Markdown("""
                ## Assistant Bot

                A simple contact and note management system with:
                - 📇 **Contact Management**: Store names, phones, emails, addresses, and birthdays
                - 📝 **Note Management**: Create notes with tags for easy organization
                - 🔍 **Search**: Find contacts and notes quickly
                - 🎂 **Birthday Reminders**: Track upcoming birthdays

                ### How to Run
                - **CLI Mode**: `python src/presentation/cli/main.py`
                - **Web UI Mode**: `python src/web/gradio_app.py` (this interface)
                - **MCP Server**: `python src/web/server.py` (for AI integration)

                ### Storage
                Data is stored in JSON format in the project directory.

                ### Features
                - Add, edit, and remove contacts
                - Search contacts by name or phone
                - Track birthdays and get reminders
                - Create and organize notes with tags
                - Search notes by text or tags
                """)

    return app


if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
