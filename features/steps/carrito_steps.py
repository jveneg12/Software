from behave import when
from selenium.webdriver.common.by import By
import time

@when('selecciono el producto "pera"')
def step_seleccionar_pera(context):
    cards = context.browser.find_elements(By.CLASS_NAME, "card")
    for card in cards:
        titulo = card.find_element(By.CLASS_NAME, "card-title").text
        if titulo.lower() == "pera":
            card.find_element(By.LINK_TEXT, "Comprar").click()
            time.sleep(1)
            break