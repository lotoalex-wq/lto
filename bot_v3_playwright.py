import asyncio
from playwright.async_api import async_playwright
import os

# Données personnelles
user_data = {
    "name": "Alexandre Ranson",
    "email": "lotoalext@gmail.com",
    "phone": "0611744681"
}

# Historique
history_file = "participation_history.txt"
if not os.path.exists(history_file):
    with open(history_file, "w") as f:
        pass

async def main():
    url = "https://www.concours-du-net.com/"
    with open(history_file, "r") as f:
        treated_urls = set(f.read().splitlines())

    if url in treated_urls:
        print("⏭️ Ce concours a déjà été traité.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Remplissage des champs
        form_fields = {
            "name": ["name", "nom", "full_name", "fullname"],
            "email": ["email", "mail"],
            "phone": ["phone", "tel", "mobile"]
        }

        for field_type, keywords in form_fields.items():
            for keyword in keywords:
                try:
                    input_el = await page.query_selector(f'input[name*="{keyword}"]')
                    if input_el:
                        await input_el.fill(user_data[field_type])
                        break
                except:
                    continue

        # CAPTCHA
        captcha_keywords = ["captcha", "recaptcha"]
        captcha_found = False
        for keyword in captcha_keywords:
            if await page.query_selector(f'[id*="{keyword}"], [class*="{keyword}"]'):
                print("🚫 CAPTCHA détecté — intervention requise.")
                captcha_found = True
                break

        if not captcha_found:
            # Soumission
            submit_keywords = ["submit", "envoyer", "valider", "send"]
            for keyword in submit_keywords:
                try:
                    btn = await page.query_selector(f'button:text("{keyword}")')
                    if not btn:
                        btn = await page.query_selector(f'input[type="submit"][value*="{keyword}"]')
                    if btn:
                        await btn.click()
                        print(f"✅ Formulaire soumis via : {keyword}")
                        break
                except:
                    continue

            await page.wait_for_timeout(3000)
            content = await page.content()
            if any(msg in content.lower() for msg in ["merci", "confirmation", "validée", "thank you", "successfully"]):
                print("🎉 Participation réussie détectée.")
                with open(history_file, "a") as f:
                    f.write(url + "\n")
            else:
                print("❌ Aucune confirmation détectée.")

        await browser.close()

asyncio.run(main())