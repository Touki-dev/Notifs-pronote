from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .Fonctions import *
import random

def crawl(user_id):
    driver = webdriver.Firefox()
    options = Options()
    options.headless = True
    driver.get('https://0782562l.index-education.net/pronote/')

    # brouillage
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    ]

    # Sélectionner un agent utilisateur aléatoire
    user_agent = random.choice(user_agents)
    options.set_preference("general.useragent.override", user_agent)
    options.add_argument("--private")

    res = dict()
    IDs = get_IDs(user_id)
    if IDs:
        id_ent, passwd = IDs
    else:
        return "User doesn't exist"

    try:
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'username')))
        username_field.send_keys(id_ent)
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
        password_field.send_keys(passwd)
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'kc-login')))
        submit_button.click()
                
        res["homeworks"] = get_homeworks(driver)
        res["notes"], res["moyennes"], res["notifs_note"] = get_notes(driver, user_id)

    except Exception as e:
        print("Une erreur s'est produite :", e)
    finally:
        driver.quit()
    return res