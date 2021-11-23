"""Template robot with Python."""
from RPA.Browser.Selenium import Selenium
import pandas as pd
import os
import csv

from config import AGENCY

browser = Selenium()


def extract_information(self, html_tag, link=False):

    if link:
        return f'https://itdashboard.gov{html_tag.get("href")}'

    return html_tag.get_text().strip()


# abrir a webpage
    # clicar em dive in

# capturar nomes e valores das agencias


# armazenar em um csv


def minimal_task():
    browser.open_chrome_browser("https://itdashboard.gov/")

    browser.click_element(f'//*[contains(text(), "DIVE IN")]')

    browser.wait_until_element_is_visible(f'//div[@id="agency-tiles-widget"]')

    for i in range(1, 99):

        for n in range(1, 4):

            agencies_element = f'//div[@id="agency-tiles-widget"]/div/div[{i}]/div[{n}] //span[@class="h4 w200"]'
            amount_element = f'//div[@id="agency-tiles-widget"]/div/div[{i}]/div[{n}] //span[@class=" h1 w900"]'

            if not browser.is_element_visible(agencies_element):
                break

            browser.scroll_element_into_view(agencies_element)

            agency = browser.get_element_attribute(
                agencies_element, "innerText")
            amount = browser.get_element_attribute(amount_element, "innerText")

            print(f'agencia {agency} - {amount}')

            fieldnames = ['Agency Name', 'Spend Amount']

            with open('data/agencies.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                
                if (os.stat("data/agencies.csv").st_size == 0):
                    writer.writeheader()

                writer.writerow(
                    {'Agency Name': agency, 'Spend Amount': amount})

    with pd.ExcelWriter('agencies.xlsx') as ew:

        pd.read_csv('data/agencies.csv').to_excel(ew, sheet_name="Agencies")

    


def select_individual_agencie():

    agency = f'//div[@id="agency-tiles-container"] //span[contains(text(), "{AGENCY}")]/.'

    browser.scroll_element_into_view(agency)

    browser.click_element(agency)


    browser.scroll_element_into_view(f'//h4[contains(text(),"Individual Investments")]')
    browser.wait_until_element_is_visible(f'//*[@id="investments-table-container"]', 20)


    #show all
    browser.click_element(f'//*[@id="investments-table-object_length"] //option[@value="-1"]')
    
    browser.wait_until_element_is_not_visible(f'//*[@id="investments-table-object_paginate"]/span/a[@data-dt-idx="3"]', 60)

    # element = f'//*[@id="investments-table-object"]/tbody'
    # lista = browser.get_list_items(element)
    for i in range(1, 9999):



        uii_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[1]'
        bureau_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[2]'
        investment_title_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[3]'
        total_spending_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[4]'
        i_type_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[5]'
        cio_rating_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[6]'
        of_projects_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[7]'

        if not browser.is_element_visible(uii_element):
            break

        browser.scroll_element_into_view(uii_element)

        # print(lista)
        _id = i
        uii = browser.get_element_attribute(uii_element, "innerText")
        bureau = browser.get_element_attribute(bureau_element, "innerText")
        investment_title = browser.get_element_attribute(investment_title_element, "innerText")
        total_spending = browser.get_element_attribute(total_spending_element, "innerText")
        i_type = browser.get_element_attribute(i_type_element, "innerText")
        cio_rating = browser.get_element_attribute(cio_rating_element, "innerText")
        of_projects = browser.get_element_attribute(of_projects_element, "innerText")

        fieldnames = ["UII", "Bureau", "Investment Title", "Total Spending", "Type", "CIO Rating","of Projects"
        ]

        title_file = AGENCY.lower().replace(" ", "_")

        with open(f'data/ii_{title_file}.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if (os.stat(f'data/ii_{title_file}.csv').st_size == 0):
                writer.writeheader()

            writer.writerow(
                {
                    "UII" : uii, 
                    "Bureau" : bureau , 
                    "Investment Title": investment_title, 
                    "Total Spending": total_spending, 
                    "Type": i_type, 
                    "CIO Rating": cio_rating,
                    "of Projects": of_projects
                })



    with pd.ExcelWriter(f'data/ii_{title_file}.xlsx') as ew:

        pd.read_csv(f'data/ii_{title_file}.csv').to_excel(ew, sheet_name=AGENCY)


if __name__ == "__main__":
    minimal_task()
    select_individual_agencie()
