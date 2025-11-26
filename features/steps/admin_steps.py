from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@then('debería ver la página de menú')
def step_ver_menu(context):
    body_text = context.browser.find_element(By.TAG_NAME, "body").text
    assert "Bienvenido" in body_text  # validamos que entró al menú admin

@when('selecciono la opción de productos')
def step_ir_productos(context):
    wait = WebDriverWait(context.browser, 5)
    # El botón "🧱 Mantenedor" apunta a /productos
    link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/productos']")))
    link.click()
    time.sleep(1)

@then('debería ver la página de productos')
def step_ver_productos(context):
    body_text = context.browser.find_element(By.TAG_NAME, "body").text
    assert "Mantenedor de Productos" in body_text


