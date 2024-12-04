# Importamos las clases necesarias de Selenium para interactuar con la página web
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importamos las clases necesarias para trabajar con fechas y tiempos
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

# Obtenemos la fecha y hora actual
now = datetime.now()

# Formateamos la fecha actual para obtener el año y el mes en formato 'YYYY-MM'
year_month = now.strftime('%Y-%m')

# Obtenemos el nombre del mes actual
monthDate = now.strftime('%B')

# Calculamos la fecha correspondiente al mes anterior
monthLast = now - relativedelta(months=1)

# Obtenemos el nombre del mes anterior
monthPrevious = monthLast.strftime('%B')

# Formateamos la fecha del mes anterior para obtener el año y el mes en formato 'YYYY-MM'
formatDate = monthLast.strftime('%Y-%m')

# Definimos la clase EdemcoPage para interactuar con la página web de Edemco
class EdemcoPage:
    # En el constructor inicializamos el driver de Selenium y el objeto WebDriverWait
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    # Método para hacer clic en el botón de 'tips'
    def click_tips(self):
        # Buscamos el botón de region en el pop-up de tips por su XPATH y hacemos clic en él
        buttonRegion = self.driver.find_element(by=By.XPATH, value='//*[@id="fenquLayer"]/div[1]/div[4]/ul/li[3]')
        buttonRegion.click()
        # Buscamos el botón de confirmación por su XPATH y hacemos clic en él
        buttonConfirm = self.driver.find_element(by=By.XPATH, value='//*[@id="fenquLayer"]/div[1]/div[5]/button')
        buttonConfirm.click()
    # Método para hacer clic en el botón de 'cookies'
    def click_cookies(self):
        # Buscamos el botón por su XPATH y hacemos clic en él
        buttonCookies = self.driver.find_element(by=By.XPATH, value='//*[@id="agree"]')
        buttonCookies.click()
    # Método para establecer el nombre de usuario en el campo correspondiente
    def set_username(self, username):
        # Buscamos el campo de nombre de usuario por su XPATH
        username_field = self.driver.find_element(by=By.XPATH, value='//*[@id="userName-id"]')
        # Introducimos el nombre de usuario en el campo
        username_field.send_keys(username)

    # Método para establecer la contraseña en el campo correspondiente
    def set_password(self, password):
        # Buscamos el campo de contraseña por su XPATH
        password_field = self.driver.find_element(by=By.XPATH, value='//*[@id="passWd-id"]')
        # Introducimos la contraseña en el campo
        password_field.send_keys(password)

    # Método para hacer clic en el botón de inicio de sesión
    def click_login(self):
        # Buscamos el botón de inicio de sesión por su XPATH
        clickLogin = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div[2]/div[5]/input')
        # Hacemos clic en el botón de inicio de sesión
        clickLogin.click()

    # Método para hacer clic en la lista de dispositivos
    def device_list_click(self):
        # Esperamos 5 segundos para asegurarnos de que la página se ha cargado completamente
        time.sleep(5)
        # Buscamos la lista de dispositivos por su XPATH
        device_list = self.driver.find_element(by=By.XPATH, value='//*[@id="ul_menu_left_main"]/li[2]/ul/a[2]/li')
        # Hacemos clic en la lista de dispositivos
        device_list.click()
    def export_data(self):
        # Hacemos una pausa de 5 segundos para asegurarnos de que la página se haya cargado completamente
        time.sleep(5)
        # Esperamos hasta que el botón de exportar datos sea clickeable y luego hacemos clic en él
        export_data = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_contentWin"]/div[1]/div[3]/div[1]/div[3]/div/div[1]/div[2]/div')))
        export_data.click()
        # Esperamos hasta que la opción de exportar generación sea clickeable y luego hacemos clic en ella
        export_generation = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_contentWin"]/div[1]/div[3]/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/span')))
        export_generation.click()
        # Hacemos una pausa de 5 segundos para asegurarnos de que la página se haya cargado completamente
        time.sleep(5)

        # Esperamos hasta que el botón de exportar mes sea clickeable y luego hacemos clic en él
        export_month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form_exportEnergyMultiple"]/table/tbody/tr[1]/td[2]/div[2]/i')))
        export_month.click()
        # Hacemos una pausa de 10 segundos para asegurarnos de que la página se haya cargado completamente
        time.sleep(10)

        # Esperamos hasta que el selector de mes sea clickeable y luego hacemos clic en él
        select_month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="val_date_exportEnergyMultiple_month"]')))
        select_month.click()
        # Si el mes actual es Enero
        if (monthDate == "January"):
            # Esperamos hasta que el botón del año anterior sea clickeable
            previousYear = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layui-laydate15"]/div[1]/div[1]/i[1]')))
            # Hacemos clic en el botón del año anterior
            previousYear.click()
            # Esperamos hasta que el botón del mes (en este caso Diciembre, representado por '11') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="11"]')))
            # Hacemos clic en el botón del mes
            month.click()
        # Si el mes actual es Febrero
        elif (monthDate == "February"):
            # Esperamos hasta que el botón del mes anterior (Enero, representado por '0') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="0"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Marzo
        elif (monthDate == "March"):
            # Esperamos hasta que el botón del mes anterior (Febrero, representado por '1') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="1"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Abril
        elif (monthDate == "April"):
            # Esperamos hasta que el botón del mes anterior (Marzo, representado por '2') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="2"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Mayo
        elif (monthDate == "May"):
            # Esperamos hasta que el botón del mes anterior (Abril, representado por '3') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="3"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Junio
        elif (monthDate == "June"):
            # Esperamos hasta que el botón del mes anterior (Mayo, representado por '4') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="4"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Julio
        elif (monthDate == "July"):
            # Esperamos hasta que el botón del mes anterior (Junio, representado por '5') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="5"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Agosto
        elif (monthDate == "August"):
            # Esperamos hasta que el botón del mes anterior (Julio, representado por '6') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="6"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Septiembre
        elif (monthDate == "September"):
            # Esperamos hasta que el botón del mes anterior (Agosto, representado por '7') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="7"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Octubre
        elif (monthDate == "October"):
            # Esperamos hasta que el botón del mes anterior (Septiembre, representado por '8') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="8"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Noviembre
        elif (monthDate == "November"):
            # Esperamos hasta que el botón del mes anterior (Octubre, representado por '9') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="9"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Si el mes actual es Diciembre
        elif (monthDate == "December"):
            # Esperamos hasta que el botón del mes anterior (Noviembre, representado por '10') sea clickeable
            month = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@lay-ym="10"]')))
            # Hacemos clic en el botón del mes anterior
            month.click()
        # Esperamos hasta que el botón de confirmación sea clickeable
        confirm = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layui-laydate16"]/div[2]/div/span[2]')))        
        # Hacemos clic en el botón de confirmación
        confirm.click()
        # Esperamos hasta que el campo para el nombre del archivo xls sea clickeable
        namexls_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="val_fileName_exportEnergyMultiple"]')))
        # Ingresamos el nombre del archivo xls, que es el mes anterior seguido de la palabra 'Generacion'
        namexls_field.send_keys(f'{monthPrevious}Generacion')
        # Esperamos hasta que el botón de confirmación de datos sea clickeable
        confirm_data = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog_exportEnergyMultiple"]/div[3]/span[2]')))  
        # Hacemos clic en el botón de confirmación de datos
        confirm_data.click()
    def download_list(self):
        # Creamos el nombre del archivo xls que vamos a descargar, que es el mes anterior seguido de la palabra 'Generacion' y el año y el mes
        text = f'{monthPrevious}Generacion_{year_month}.xls' 
        # Esperamos hasta que el enlace de descarga sea clickeable
        download_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_contentWin"]/div[1]/div[3]/div[1]/div[1]/div[2]/a')))
        # Hacemos clic en el enlace de descarga
        download_link.click()
        # Hacemos una pausa de 10 segundos para asegurarnos de que la descarga se haya iniciado
        time.sleep(10)
        # Esperamos hasta que el botón de descarga del archivo xls sea clickeable
        download_xls = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterManage_asyncExport"]/div[2]/div')))
        # Hacemos clic en el botón de descarga del archivo xls
        download_xls.click()
        # Esperamos hasta que el botón para abrir el archivo sea clickeable, es el boton para descargar el archivo en growatt
        open_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterManage_asyncExport"]/div[2]/div/div[3]/div[1]')))
        # Hacemos clic en el botón para descargar el archivo
        open_file.click()
        # Devolvemos el nombre del archivo xls
        return text