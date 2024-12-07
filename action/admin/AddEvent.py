# action/admin/AddEvent.py

from ..Action import Action
from DB_utils import add_event, list_categories, list_organizers

class AddEvent(Action):
    def __init__(self, action_name="Add Event"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        if user is None or not user.isAdmin():
            conn.send("Unauthorized action.\n".encode('utf-8'))
            return

        # 輸入活動名稱
        event_name = self.read_input(conn, "event name")
        if not event_name:
            conn.send("Event name cannot be empty.\n".encode('utf-8'))
            return

        # 列出所有類別
        categories = list_categories()
        if not categories:
            conn.send("No categories available. Please add a category first.\n".encode('utf-8'))
            return
        self.send_table(conn, categories)

        # 選擇類別 ID
        category_id_str = self.read_input(conn, "category ID")
        if not category_id_str.isdigit():
            conn.send("Invalid Category ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        category_id = int(category_id_str)

        # 列出所有主辦方
        organizers = list_organizers()
        if not organizers:
            conn.send("No organizers available. Please add an organizer first.\n".encode('utf-8'))
            return
        self.send_table(conn, organizers)

        # 選擇主辦方 ID
        organizer_id_str = self.read_input(conn, "organizer ID")
        if not organizer_id_str.isdigit():
            conn.send("Invalid Organizer ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        organizer_id = int(organizer_id_str)

        # 輸入活動日期及時間
        event_datetime = self.read_input(conn, "event date and time (YYYY-MM-DD HH:MM:SS)")
        if not event_datetime:
            conn.send("Event date and time cannot be empty.\n".encode('utf-8'))
            return

        # 輸入活動地點
        event_location = self.read_input(conn, "event location")
        if not event_location:
            conn.send("Event location cannot be empty.\n".encode('utf-8'))
            return

        # 輸入描述
        description = self.read_input(conn, "event description")

        # 新增活動
        success, message = add_event(event_name, category_id, organizer_id, event_datetime, event_location, description)
        conn.send(f"{message}\n".encode('utf-8'))
