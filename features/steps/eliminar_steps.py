from behave import when
from selenium.webdriver.common.by import By
import time

@when('elimino el producto con ID "{id}"')
def step_eliminar_producto(context, id):
    # Busca el enlace de eliminar según el ID
    selector = f"a[href='/eliminar_producto/{id}']"
    link = context.browser.find_element(By.CSS_SELECTOR, selector)
    link.click()
    time.sleep(1)