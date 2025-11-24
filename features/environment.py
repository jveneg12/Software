# Archivo environment.py
# Configuración del entorno para pruebas BDD con Behave y Selenium
# Captura de pantalla después de cada escenario

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import datetime

# Variable para rescatar fecha y hora de ejecución
fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Carpeta de capturas
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "evidencias")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def before_all(context):
    # Ruta al chromedriver dentro de la carpeta "drivers"
    chrome_driver_path = os.path.join(
        os.getcwd(), "drivers", "chromedriver.exe"
    )
    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # si quieres que corra sin abrir ventana

    context.browser = webdriver.Chrome(service=service, options=options)
    context.browser.maximize_window()
    context.base_url = 'http://127.0.0.1:5000'  # Flask corre en el puerto 5000

def before_scenario(context, scenario):
    # En Flask no necesitas borrar usuarios aquí.
    # Si quieres preparar datos, hazlo en los pasos GIVEN del escenario.
    pass

def after_scenario(context, scenario):
    """
    Se ejecuta después de CADA escenario y toma una captura SIEMPRE.
    """
    feature_name = scenario.feature.name.replace(" ", "_")
    scenario_name = scenario.name.replace(" ", "_")
    scenario_status = scenario.status.name  # "passed", "failed", etc.

    filename = f"{fecha}_{feature_name}_{scenario_name}_{scenario_status}.png"
    screenshot_path = os.path.join(SCREENSHOTS_DIR, filename)

    if hasattr(context, 'browser'):
        try:
            context.browser.save_screenshot(screenshot_path)
            print(f"Captura ({scenario_status}) guardada en: {screenshot_path}")
        except Exception as e:
            print(f"Error al guardar la captura de pantalla: {e}")

def after_all(context):
    context.browser.quit()