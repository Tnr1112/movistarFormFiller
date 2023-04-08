import sys
import subprocess
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import time
from multiprocessing import Pool

nombres = open('nombres.txt',encoding="utf8").read().splitlines()
proxies = open('proxies.txt',encoding="utf8").read().splitlines()

def fillFormMovistar(numeroCalle,proxy):
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	proxyChrome = Proxy()
	proxyChrome.proxy_type = ProxyType.MANUAL
	proxyChrome.http_proxy = proxy
	capabilities = webdriver.DesiredCapabilities.CHROME
	proxyChrome.add_to_capabilities(capabilities)

	driver = webdriver.Chrome(options=chrome_options,desired_capabilities=capabilities)
	driver.get("https://tienda.movistar.com.ar/hogarinternet/")
	driver.find_element(By.XPATH,f'//*[@id="slick-slide0{random.randint(0, 2)}"]//button[contains(@class, "check-availability-button")]').send_keys("\n")
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="movistarUserNoOption"]'))).click()

	inputs = driver.find_elements(By.XPATH, '//div[@class="isNotMovistarUser"]/div[@class="form-container"]/div[@class="table-container"]/div[@class="field"]//input')
	inputNroContacto = inputs[0]
	inputCalle = inputs[1]
	inputNumero = inputs[2]
	inputProvincia = inputs[3]
	inputLocalidad =inputs[4]
	inputEntreCalles = inputs[5]
	inputCP = inputs[6]

	nroTelefonoRandom = random.randint(11111111,99999999)
	inputNroContacto.send_keys(f'11{nroTelefonoRandom}')
	inputCalle.send_keys("Alberti")
	inputNumero.send_keys(numeroCalle)
	inputProvincia.send_keys("Capital Federal")
	inputLocalidad.send_keys("Parque Patricios")
	inputEntreCalles.send_keys("Rondeau y 15 de noviembre")
	inputCP.send_keys(1247)

	# Edificio
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'buildingNoOption'))).click()

	time.sleep(3)

	# Barrio cerrado
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'countryNoOption'))).click()

	# Botón de verificar
	WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="isNotMovistarUser"]/div[@class="action-button"]/button[@data-role="verify-stepper"]'))).click()

	# Confirmar dirección (Modal)
	WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="movistar-address-modal"]/div[contains(@class,"address-confirmation")]/div[@class="action-button"]/button[@data-role="confirm-modal"]'))).click()

	time.sleep(3)

	# No hay fibra en tu zona (Modal)
	inputs = driver.find_elements(By.XPATH, '//form[@id="no-prefa-form"]/div[@class="form-container"]/div[@class="table-container"]/div[@class="field"]//input')
	inputNombre = inputs[0]
	inputEmail = inputs[2]

	nombre = random.choice(nombres)
	inputNombre.send_keys(nombre)
	nombresTemp = nombre.split(" ")
	email = subprocess.getoutput(f'python namely.py -n {unidecode(nombresTemp[0].lower())} {unidecode(nombresTemp[1].lower())} -df mails.txt | head -{random.randint(1,30)} | tail -1')
	inputEmail.send_keys(email)

	# Aceptar confirmación datos
	WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'submit-contact-information-action'))).click()

	finishText = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(@class,"no-prefa-information-submited")]//div[@class="title"]/strong'))).text

	if finishText == "¡Listo!":
		print("Successful execution")
		driver.quit()
		sys.exit(0)

if __name__ == "__main__":
	parametros = []
	for i in range(2000,2101):
		proxy = random.choice(proxies)
		parametros.append((i,proxy))

	with Pool(100) as p:
		p.starmap(fillFormMovistar,parametros)
