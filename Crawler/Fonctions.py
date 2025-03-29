from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
import json

# Sqlite
def get_IDs(user_id):
    connexion = sqlite3.connect('./Database/database.db')
    cursor = connexion.cursor()
    cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    connexion.close()
    return user[2:4]

def get_notes_saved(user_id):
    connexion = sqlite3.connect('./Database/database.db')
    cursor = connexion.cursor()
    cursor.execute('SELECT * FROM Notes WHERE user_id = ?', (user_id,))
    notes = cursor.fetchone()
    connexion.close()
    return notes[1] if notes else None

def save_notes(user_id, notes):
    connexion = sqlite3.connect('./Database/database.db')
    cursor = connexion.cursor()
    cursor.execute('INSERT OR REPLACE INTO Notes (user_id, notes_json) VALUES (?, ?)', (user_id, notes))
    connexion.commit()
    connexion.close()
    
# Pronote
def get_homeworks(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="wrap conteneur-item"]')))
    homeworks = driver.find_elements(By.XPATH, '//div[@class="wrap conteneur-item"]')
    res = []
    for hw in homeworks:
        matiere = hw.find_element(By.CSS_SELECTOR, '.titre-matiere').text
        contenu = hw.find_element(By.CSS_SELECTOR, '.description.widgetTAF.tiny-view div').text
        res.append({"matiere": matiere, "contenu": contenu})
    return res

def get_notes(driver, user_id):
    notes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'GInterface.Instances[0].Instances[1]_Combo2')))
    notes_button.click()
    # Check Notes
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'note-devoir')))
    notes_elements = driver.find_elements(By.CLASS_NAME, 'note-devoir')
    all_notes = []
    for note in notes_elements:
        parent_element = note.find_element(By.XPATH, '../../..')
        matiere = parent_element.find_element(By.CLASS_NAME, 'ie-ellipsis')
        matiere = driver.execute_script("return arguments[0].textContent;", matiere)
        note = driver.execute_script("return arguments[0].textContent;", note)
        all_notes.append([matiere, note])

    notifs_note = []
    notes_saved = get_notes_saved(user_id)
    all_notes_copy = all_notes.copy()
    if notes_saved:
        notes_saved = json.loads(notes_saved)
        if all_notes != notes_saved:
            for i in range(len(notes_saved)):
                if notes_saved[i] != all_notes[i]:
                    notifs_note.append(all_notes[i])
                    all_notes.pop(i)
    else:
        notifs_note = all_notes

    if notifs_note:
        save_notes(user_id, json.dumps(all_notes_copy))

    # Check Moyennes
    by_matiere_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.iecb.iecbrbgauche.m-left.as-chips')))
    by_matiere_button.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.flex-contain .ie-titre-gros')))
    notes = driver.find_elements(By.CSS_SELECTOR, '.flex-contain .ie-titre-gros')
    moyennes = {}
    for moyenne in notes:
        parent_element = moyenne.find_element(By.XPATH, '../../..')
        matiere = parent_element.find_element(By.CSS_SELECTOR, '.zone-principale span')
        matiere = driver.execute_script("return arguments[0].textContent;", matiere)
        moyenne = driver.execute_script("return arguments[0].textContent;", moyenne)
        if moyenne != 'Abs' and moyenne != '0':
            moyenne = moyenne.split(',')
            moyennes[matiere] = float(".".join(moyenne))
            
    return all_notes, moyennes, notifs_note