def test_entry_date_label_present():
    with open('ui/customer_ui.py', 'r', encoding='utf-8') as f:
        contents = f.read()
    assert 'Entry Date (DD-MM-YYYY)' in contents
