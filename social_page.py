# social_page.py
import json
from style_one_category import style_one_category  # الكلاس الأساسي

# قراءة البيانات من ملف events.json
with open("events.json", "r") as f:
    events_data = json.load(f)

class social_page(style_one_category):
    def __init__(self, parent,nav_stack):
        # نرسل فقط قسم "tech" من JSON
        super().__init__(parent, "social", events_data["social"],nav_stack)