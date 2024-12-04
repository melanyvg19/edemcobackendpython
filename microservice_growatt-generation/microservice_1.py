# Importamos la clase AbstractAPI del módulo process
from process import AbstractAPI

# Importamos las clases necesarias de Selenium para interactuar con el navegador
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Importamos la clase WebAutomation del módulo main_automate en el paquete Automate
from Automate.main_automate import WebAutomation

# Definimos la clase Microservice_1 que hereda de AbstractAPI
class Microservice_1(AbstractAPI):
    # Definimos el método automation
    def automation(self):
        # Creamos una nueva instancia del navegador Chrome
        driver = webdriver.Chrome()
        # Configuramos el navegador para esperar hasta 20 segundos antes de lanzar una excepción
        driver.implicitly_wait(20)
        # Creamos una nueva instancia de WebAutomation pasando el navegador como argumento
        automation = WebAutomation(driver)
        # Navegamos a la página de inicio de sesión de Growatt
        automation.navigate_to_website('https://oss.growatt.com/login?lang=en')
        # Iniciamos sesión con el usuario 'AZPA4001' y la contraseña 'Edemco2020'
        automation.login('AZPA4001', 'Edemco2020')
        # Descargamos el archivo Excel y guardamos la ruta del archivo en la variable path_xlsx
        path_xlsx = automation.download_excel()
        # Cerramos el navegador
        automation.quit()
        # Devolvemos la ruta del archivo Excel
        return path_xlsx

    