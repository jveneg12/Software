from behave import given, when, then
from selenium.webdriver.common.by import By
import time

@given('que estoy en la página de login')
def step_ir_login(context):
    context.browser.get(context.base_url)

@when('ingreso usuario "{usuario}" y clave "{clave}"')
def step_ingresar_credenciales(context, usuario, clave):
    context.browser.find_element(By.NAME, "usuario").send_keys(usuario)
    context.browser.find_element(By.NAME, "clave").send_keys(clave)

@when('presiono el botón de ingresar')
def step_presionar_ingresar(context):
    context.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1)
