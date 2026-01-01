def test_records_columns_present():
    with open('ui/main_window.py', 'r', encoding='utf-8') as f:
        s = f.read()
    assert '"Customer ID", "Name", "Address", "Village", "Brand"' in s
