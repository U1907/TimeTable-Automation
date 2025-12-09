import re
from html.parser import HTMLParser

class CourseParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_row = False
        self.in_cell = False
        self.row_data = []
        self.cell_content = []
        self.courses = []

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.in_row = True
            self.row_data = []
        elif tag == "td" and self.in_row:
            self.in_cell = True
            self.cell_content = []

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        elif tag == "tr" and self.in_tbody:
            self.in_row = False
            if len(self.row_data) == 8:
                self.extract_schedule(self.row_data)
        elif tag == "td" and self.in_row:
            self.in_cell = False
            text = " ".join(self.cell_content).strip()
            text = re.sub(r"\s+", " ", text)  
            self.row_data.append(text)

    def handle_data(self, data):
        if self.in_cell:
            self.cell_content.append(data)

    def extract_schedule(self, row):
        code, title, room, instructor = row[0], row[1], row[2], row[6]
        schedule_text = row[7]

        matches = re.findall(
            r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday):\s*(\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2})",
            schedule_text,
        )

        for day, start, end in matches:
            self.courses.append(
                {
                    "day": day,
                    "start": start[:5],
                    "end": end[:5],
                    "code": code,
                    "title": title,
                    "room": room,
                    "instructor": instructor,
                }
            )