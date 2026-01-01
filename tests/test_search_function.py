def test_search_function_exists():
    from models.report_model import search_customer_items
    assert callable(search_customer_items)
