from ui.customer_ui import today_str
from datetime import date


def test_today_str():
    assert today_str() == date.today().isoformat()
