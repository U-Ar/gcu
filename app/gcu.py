import getpass
import os
import sys
import time
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Setting:
    def __init__(self):
        self.map = dict()
        self.include_star = True 

def left_padding(msg, digit):
    for c in msg:
        if unicodedata.east_asian_width(c) in ('F','W'):
            digit -= 2
        else:
            digit -= 1
    return msg + ' ' * digit

def print_desc():
    print()
    print("-- Description -------------------------------------------------")
    print("Automatically calculate your GPA from UTAS with several weights.")
    print()
    print("Type")
    print("1. Student ID")
    print("2. Password")
    print("following the prompt.")
    print()
    print("Rerun this program without passing command line arguments.")
    print("----------------------------------------------------------------")
    print()

# read setting from settings.txt
def read_setting():
    setting = Setting()
    with open("settings.txt",mode="r") as f:
        # comment line
        f.readline()

        setting.map["優上"] = float(f.readline().split()[0])
        setting.map["優"] = float(f.readline().split()[0])
        setting.map["良"] = float(f.readline().split()[0])
        setting.map["可"] = float(f.readline().split()[0])
        setting.map["不可"] = float(f.readline().split()[0])

        setting.include_star = int(f.readline().split()[0])
    
    return setting

# process one entry of the score table
def calc_entry(sum_score, num_credit, entry, setting):
    cols = entry.find_elements_by_xpath('.//td')

    # TODO: columns of the score tables seem to differ according to faculties
    #       now implemented for the faculty of Liveral Arts and Engineering, 
    #       but others are not considered (maybe same as Engineering)

    if len(cols) == 9: # Liberal Arts
        grade = cols[7].text
        if grade in setting.map:
            c = float(cols[6].text)
            print(left_padding(cols[2].text,40) + " " + str(c).center(9) + " " + "{:.1f}".format(setting.map[grade]).center(6))
            sum_score += setting.map[grade] * c
            num_credit += c 
        return sum_score, num_credit
    elif len(cols) == 15: # Engineering
        grade = cols[7].text
        if setting.include_star or cols[9].text != "*":
            if grade in setting.map:
                c = float(cols[6].text)
                print(left_padding(cols[2].text,40) + " " + str(c).center(9) + " " + "{:.1f}".format(setting.map[grade]).center(6))
                sum_score += setting.map[grade] * c
                num_credit += c 
        return sum_score, num_credit
    else:
        print("Encountered the unknown case.")
        return sum_score, num_credit

# main function
def calc(driver, student_id, student_pass):
    driver.implicitly_wait(1)

    # access to the portal page
    driver.get("https://utas.adm.u-tokyo.ac.jp/campusweb/campusportal.do")

    # move to the login page
    submit_button = driver.find_element_by_xpath("//button[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url != "https://utas.adm.u-tokyo.ac.jp/campusweb/campusportal.do?page=main":
        # type ID&password and login
        id_input = WebDriverWait(driver,timeout=3).until(lambda d: d.find_element_by_id("userNameInput"))
        id_input.send_keys(student_id)
        pass_input = driver.find_element_by_id("passwordInput")
        pass_input.send_keys(student_pass)
        submit_button = driver.find_element_by_id("submitButton")
        submit_button.click()

    time.sleep(1)

    # move to the tab of personal score
    driver.get("https://utas.adm.u-tokyo.ac.jp/campusweb/campusportal.do?page=main&tabId=si")

    # click all elements of the list of affiliations 
    WebDriverWait(driver,timeout=3).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe")))
    belong_list = WebDriverWait(driver,timeout=3).until(lambda d: d.find_elements_by_xpath(".//input[@name='shozokuCd']"))
    driver.find_element_by_xpath(".//body").click() # focus the iframe
    for b in belong_list:
        b.click()

    # submit and make the page print your score table
    driver.find_element_by_xpath("//input[@value=' 画面に表示する ']").click()

    time.sleep(1)

    # read setting file
    print()
    print("Reading setting.txt ...")
    setting = read_setting()
    print("Successfully read setting.txt.")

    sum_score = 0
    num_credit = 0

    # get all entries of the score tables
    entries = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements_by_xpath("//tr[@onmouseout='TRMouseOut(this)']"))
    
    print()
    print("Successfully accessed to UTAS and got score tables.")
    print()
    print("Courses taken into account".ljust(40) + "| credits | score")

    # calculate the number of credits and the sum of the scores
    for entry in entries:
        sum_score, num_credit = calc_entry(sum_score, num_credit, entry, setting)
            
    print()
    print("--- Result ---------------------")
    print("Number of credits: {:.2f}".format(num_credit))
    print("Sum of scores    : {:.2f}".format(sum_score))
    print("GPA              : {:.2f}".format(sum_score/num_credit))
    print("--------------------------------")


if __name__ == "__main__":
    print("--- GPA Calculator for UTAS (GCU) v1.0 powered by Python & selenium ---")
    
    if len(sys.argv) > 1:
        print_desc()
        sys.exit(0)

    student_id = input("student ID: ")
    student_pass = getpass.getpass("password: ")

    # set options to start Firefox
    options = webdriver.FirefoxOptions()
    options.headless = True 

    # open the new window of the browser
    print("connecting to the remote browser...")
    driver = webdriver.Remote(
        command_executor=os.environ["SELENIUM_URL"],
        desired_capabilities=options.to_capabilities(),
        options=options
    )

    try:
        calc(driver,student_id,student_pass)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
