from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Automate.edemco_page import EdemcoPage 
import time

class WebAutomation:
    """
    Clase para automatizar la interacción con una página web utilizando Selenium.
    """

    def __init__(self, driver):
        """
        Inicializa la clase WebAutomation.

        Args:
            driver (webdriver): El controlador de navegador web de Selenium.
        """
        self.driver = driver
        self.edemco_page = EdemcoPage(driver)

    def switch_to_new_window(self):
        """
        Cambia el controlador para apuntar a la última ventana abierta.
        """
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])

    def navigate_to_website(self, url):
        """
        Navega a la URL especificada.

        Args:
            url (str): La URL a la que se debe navegar.
        """
        self.driver.get(url)

    def login(self, username, password):
        """
        Realiza el inicio de sesión en la página web.

        Args:
            username (str): El nombre de usuario para iniciar sesión.
            password (str): La contraseña para iniciar sesión.
        """
        self.edemco_page.click_tips()
        self.edemco_page.click_cookies()
        self.edemco_page.set_username(username)
        self.edemco_page.set_password(password)
        self.edemco_page.click_login()

    def download_excel(self):
        """
        Descarga un archivo Excel de la página web.

        Returns:
            str: La ruta al archivo Excel descargado.
        """
        self.edemco_page.device_list_click()
        self.edemco_page.export_data()
        path_xlsx = self.edemco_page.download_list()
        return path_xlsx

    def quit(self):
        """
        Cierra el controlador del navegador después de una espera de 20 segundos.
        """
        time.sleep(20)
        self.driver.quit()
