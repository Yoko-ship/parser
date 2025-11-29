SELECTORS = {
    "OLX": {
        "input": "#search",
        "container": ".css-1g5933j",
        "title": ".css-1g61gc2",
        "href": ".css-1tqlkj0",
        "price": ".css-uj7mm0",
        "condition": ".css-iudov9 span",
        "scroll": None,
        "URL":"https://www.olx.uz/",
        "price_filter":"//input[contains(@placeholder,'до:')]"
    },
    "UZUM": {
        "input": ".input-line input",
        "container": "#category-products > div",
        "title": ".product-card__title",
        "href": "[data-test-id='product-card--default']",
        "price": ".currency",
        "condition": ".reviews",
        "scroll": {"step": 400, "repeats": 5, "click_selector": ".button-more", "delay": 2},
        "URL":"https://uzum.uz/ru",
        "price_filter":"//input[@data-test-id='input__max-price']"
    },
    "Яндекс маркет": {
        "input": "#header-search",
        "container": "[data-auto='SerpList'] > div, [data-auto='SerpGrid'] > div",
        "title": "[data-auto='snippet-title']",
        "href": ".EQlfk",
        "price": "[data-auto='snippet-price-current']",
        "condition": "[data-baobab-name='rating'] > *:first-child",
        "scroll": {"step": 100, "repeats": 200, "delay": 0.1},
        "URL":"https://market.yandex.uz/",
        "price_filter":"//input[@id='range-filter-field-glprice_25563_max']"
    },
}