import reflex as rx
from typing import List, Dict, Any, TypedDict
from datetime import datetime

class Event(TypedDict):
    title: str
    time_date: str
    avatar: str

class ActionableData(TypedDict):
    events: List[Event]

SAMPLE_ACTIONABLES_DATA: ActionableData = {
    "events": [
        {
            "title": "Breakfast with the Team",
            "time_date": "9 AM - 5 PM on June 2nd 2025",
            "avatar": "/avatars/team_breakfast.jpg"
        },
        {
            "title": "Amazon Prime Day Sale",
            "time_date": "10 AM - 11 AM on June 3nd 2025",
            "avatar": "/avatars/team_breakfast.jpg"
        }
    ]
}

SAMPLE_TASKS = [
    {
        "id": "FIG-123",
        "subject": "RE: Going Away Party For Oscar",
        "tags": "Project 1",
        "priority": "High", 
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-122",
        "subject": "Water Bill Notice",
        "tags": "Acme-CRM",
        "priority": "Low",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    },
    {
        "id": "FIG-121",
        "subject": "Write blog post for demo day",
        "tags": "Acme-CRM",
        "priority": "High",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-120",
        "subject": "Publish blog page",
        "tags": "Website Launch",
        "priority": "Low",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    },
    {
        "id": "FIG-119",
        "subject": "Add gradients to rx design systems",
        "tags": "Design backlog",
        "priority": "Medium",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-118",
        "subject": "Responsive leaderboard doesn't work on Android",
        "tags": "Bug fix",
        "priority": "High",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    },
    {
        "id": "FIG-117",
        "subject": "Confirmation states not rendering properly",
        "tags": "Bug fix",
        "priority": "Medium",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-116",
        "subject": "Text wrapping is awkward on older iPhones",
        "tags": "Bug fix",
        "priority": "Low",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-115",
        "subject": "Revise copy on About page",
        "tags": "Website Launch",
        "priority": "Low",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    },
    {
        "id": "FIG-114",
        "subject": "Publish Houston times post",
        "tags": "Acme-CRM",
        "priority": "Low",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Low",
    },
    {
        "id": "FIG-113",
        "subject": "Resume image licensing for header section images",
        "tags": "Website Launch",
        "priority": "High",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    },
    {
        "id": "FIG-112",
        "subject": "Accessibility keyboard issue for input fields",
        "tags": "Design backlog",
        "priority": "High",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-111",
        "subject": "Headless UI rendition re support addition of Blog page",
        "tags": "Design backlog",
        "priority": "High",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    },
    {
        "id": "FIG-110",
        "subject": "Fixes autosound",
        "tags": "Bug fix",
        "priority": "Medium",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "High",
    },
    {
        "id": "FIG-109",
        "subject": "GIFs broken when looping back more than 3 times on the Search page",
        "tags": "Bug fix",
        "priority": "Low",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Low",
    },
    {
        "id": "FIG-108",
        "subject": "Editorial refresh for blog posts on mobile",
        "tags": "Website Launch",
        "priority": "Medium",
        "date": "Dec 5",
        "sender": "👤",
        "accuracy": "Medium",
    }
]


class State(rx.State):
    tasks: List[Dict[str, Any]] = SAMPLE_TASKS
    actionable_data: ActionableData = SAMPLE_ACTIONABLES_DATA
    search_query: str = ""
    selected_tab: str = "all_emails" 

    def set_search_query(self, query: str):
        self.search_query = query

    def set_tab(self, tab_value: str):
        self.selected_tab = tab_value
    
    def update_task_accuracy(self, task_id: str, new_accuracy: str):
        for task in self.tasks:
            if task["id"] == task_id:
                task["accuracy"] = new_accuracy
                break

    @rx.var
    def filtered_tasks(self) -> List[Dict[str, Any]]:
        current_tasks = self.tasks 

        if not self.search_query:
            return current_tasks
        
        lower_search_query = self.search_query.lower()
        return [
            task for task in current_tasks 
            if any(
                lower_search_query in str(task.get(key, "")).lower()
                for key in ["id", "subject", "tags", "priority", "date", "accuracy"]
            )
        ]

    @rx.var
    def events(self) -> List[Event]:
        """Computed variable to properly access events for Reflex's reactive system."""
        return self.actionable_data["events"]

def priority_badge(priority: str) -> rx.Component:
    return rx.cond(
        priority == "High",
        rx.badge(priority, color_scheme="red", size="1"),
        rx.cond(
            priority == "Medium",
            rx.badge(priority, color_scheme="orange", size="1"),
            rx.cond(
                priority == "Low",
                rx.badge(priority, color_scheme="green", size="1"),
                rx.text("")
            )
        )
    )

def tag_badge(tag: str) -> rx.Component:
    return rx.cond(
        tag,
        rx.cond(
            tag == "Project 1",
            rx.badge(tag, color_scheme="blue", size="1"),
            rx.cond(
                tag == "Acme-CRM",
                rx.badge(tag, color_scheme="purple", size="1"),
                rx.cond(
                    tag == "Website Launch",
                    rx.badge(tag, color_scheme="green", size="1"),
                    rx.cond(
                        tag == "Design backlog",
                        rx.badge(tag, color_scheme="orange", size="1"),
                        rx.cond(
                            tag == "Bug fix",
                            rx.badge(tag, color_scheme="red", size="1"),
                            rx.badge(tag, color_scheme="gray", size="1")
                        )
                    )
                )
            )
        ),
        rx.text("")
    )

def accuracy_feedback_selector(task_id: str, current_accuracy: str) -> rx.Component:
    """A component for users to select the accuracy of AI's prediction."""
    return rx.select(
        ["High", "Medium", "Low"],
        value=current_accuracy,
        on_change=lambda value: State.update_task_accuracy(task_id, value),
        placeholder="Select accuracy...",
        size="1",
        color_scheme=rx.cond(
            current_accuracy == "High", "green",
            rx.cond(current_accuracy == "Medium", "orange", "red")
        )
    )

def render_task_row(task_item):
    return rx.table.row(
        rx.table.cell(
            rx.checkbox(),
            width="40px"
        ),
        rx.table.cell(
            rx.hstack(
                rx.text(task_item["id"], color="gray", size="2"),
                rx.text(task_item["subject"], weight="medium"),
                spacing="2"
            )
        ),
        rx.table.cell(
            tag_badge(task_item["tags"])
        ),
        rx.table.cell(
            priority_badge(task_item["priority"])
        ),
        rx.table.cell(
            rx.text(task_item["date"], size="2")
        ),
        rx.table.cell(
            rx.avatar(size="2", fallback=task_item["sender"])
        ),
        rx.table.cell(
            accuracy_feedback_selector(task_item["id"], task_item["accuracy"])
        ),
        style={
            "border_bottom": "1px solid #e5e7eb",
            "background_color": "white"
        },
        _hover={"background_color": "#f8fafc"}
    )

def header() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.heading("GmailAnalyzer", size="6", weight="bold"),
            spacing="2"
        ),
        rx.spacer(),
        rx.hstack(
            rx.avatar(src="/avatars/user.jpg", fallback="U", size="2"),
            rx.icon(tag="chevron_down", size=24),
            spacing="2"
        ),
        width="100%",
        padding="1rem",
        border_bottom="1px solid #eee"
    )

def tabs_section() -> rx.Component:
    return rx.hstack(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Actionable", value="actionable", on_click=State.set_tab("actionable")),
                rx.tabs.trigger("All Emails", value="all_emails", on_click=State.set_tab("all_emails")), 
            ),
            value=State.selected_tab,
            variant="soft-rounded",
            color_scheme="orange"
        ),
        rx.spacer(),
        rx.hstack(
            rx.input(
                placeholder="Search...",
                value=State.search_query,
                on_change=State.set_search_query,
                width="300px",
                padding_right="40px"
            ),
            rx.icon(tag="search", size=20, margin_left="-35px", color="gray.500"),
            spacing="0",
            align_items="center",
        ),
        width="95%",
        margin_x="auto",
        padding="1rem 0",
        align_items="center",
    )

def table_header() -> rx.Component:
    return rx.table.header(
        rx.table.row(
            rx.table.column_header_cell(""),
            rx.table.column_header_cell("Task"),
            rx.table.column_header_cell("Tags"),
            rx.table.column_header_cell("Priority"),
            rx.table.column_header_cell("Date"),
            rx.table.column_header_cell("Sender"),
            rx.table.column_header_cell("Accuracy Feedback"),
            rx.table.column_header_cell(""),
        )
    )

def main_table() -> rx.Component:
    return rx.table.root(
        table_header(),
        rx.table.body(
            rx.foreach(
                State.filtered_tasks,
                render_task_row 
            )
        ),
        size="1",
        variant="surface",
        width="100%",
        overflow="auto",
        box_shadow="lg",
        border_radius="8px"
    )

def render_event_card(event_item):
    """Component for a single identified event."""
    return rx.hstack(
        rx.avatar(src=event_item.get("avatar", ""), fallback=event_item["title"][0], size="4"),
        rx.vstack(
            rx.text(event_item["title"], weight="bold"),
            rx.text(event_item["time_date"], color="gray.600", size="2"),
            rx.button("Schedule", size="1"),
            spacing="1",
            align_items="flex-start",
        ),
        align_items="flex-start",
        spacing="3",
        width="100%",
    )

def actionable_section() -> rx.Component:
    """Combines events into the actionable view."""
    return rx.box(
        rx.vstack(
            rx.text("Events We Have Identified", size="4", weight="bold", margin_bottom="1rem"),
            rx.vstack(  
                rx.foreach(
                    State.events,
                    lambda event_item: rx.card(render_event_card(event_item), width="100%")
                ),
                spacing="3", 
                width="100%",
            ),
            padding="1.5rem",
            box_shadow="lg",
            border_radius="8px",
            background_color="white",
            width="100%",
            align_items="flex-start",
        ),
        width="350px",
        margin_x="auto",
        padding_top="1rem",
        padding_bottom="1rem",
    )


def index() -> rx.Component:
    return rx.vstack(
        header(),
        tabs_section(),
        rx.cond(
            State.selected_tab == "all_emails", 
            rx.box(
                main_table(),
                width="95%",
                margin_x="auto",
                padding_top="1rem",
                padding_bottom="1rem",
            ),
            actionable_section()
        ),
        width="100%",
        min_height="100vh",
        background_color="#fafafa",
        spacing="0",
        align_items="center",
    )

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
        gray_color="slate",
        radius="small"
    )
)
app.add_page(index, route="/")