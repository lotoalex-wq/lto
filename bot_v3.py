from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# Données personnelles
user_data = {
    "name": "Alexandre Ranson",
    "email": "lotoalext@gmail.com",
    "phone": "0611744681"
}

# Historique des URLs déjà traitées
history_file = "participation_history.txt"
if not os.path.exists(history_file):
    with open(history_file, "w") as f:
        pass

with open(history_file, "r") as f:
    treated_urls = set(f.read().splitlines())

# URL cible (à personnaliser)
url = "https://www.concours-du-net.com/"

if url in treated_urls:
    print("⏭️ Ce concours a déjà été traité. On passe.")
    exit()

# Configurer Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(5)

# Remplissage automatique
form_fields = {
    "name": ["name", "nom", "full_name", "fullname"],
    "email": ["email", "mail"],
    "phone": ["phone", "tel", "mobile"]
}

for field_type, keywords in form_fields.items():
    for keyword in keywords:
        try:
            input_el = driver.find_element(By.XPATH, f"//input[contains(translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{keyword}')]")
            input_el.send_keys(user_data[field_type])
            break
        except:
            continue

# Détection CAPTCHA (éléments classiques comme recaptcha ou image captcha)
captcha_keywords = ["captcha", "recaptcha"]
captcha_found = False
for keyword in captcha_keywords:
    try:
        if driver.find_element(By.XPATH, f"//*[contains(@id, '{keyword}') or contains(@class, '{keyword}')]"):
            captcha_found = True
            print("🚫 CAPTCHA détecté — intervention manuelle nécessaire.")
            break
    except:
        continue

if not captcha_found:
    # Soumission automatique
    submit_keywords = ["submit", "envoyer", "valider", "send"]
    clicked = False
    for keyword in submit_keywords:
        try:
            button = driver.find_element(By.XPATH, f"//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{keyword}')] | //input[@type='submit'][contains(translate(@value,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{keyword}')]")
            button.click()
            clicked = True
            print(f"✅ Formulaire soumis via le bouton : {keyword}")
            break
        except:
            continue

    # Vérification de confirmation ou redirection
    time.sleep(3)
    page_text = driver.page_source.lower()
    if any(success in page_text for success in ["merci", "confirmation", "participation validée", "thank you", "successfully"]):
        print("🎉 Participation réussie détectée !")
        with open(history_file, "a") as f:
            f.write(url + "\n")
    else:
        print("❌ Aucune confirmation détectée après soumission.")
else:
    print("🔒 Action interrompue à cause du CAPTCHA.")

driver.quit()