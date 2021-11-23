from RPA.Browser.Selenium import Selenium
import time
import pandas as pd
import csv
import os

from config import AGENCY, DOWNLOADS_PATH

driver = Selenium()

def get_agency_expenses():
    """Get the agency's expenses and save it in an excel file
    """

    url = "https://itdashboard.gov/"
    btn_dive_in = f'//*[contains(text(), "DIVE IN")]'
    title = f'//div[@id="agency-tiles-widget"]'

    driver.open_chrome_browser(url, preferences={"download.default_directory": DOWNLOADS_PATH})

    driver.click_element(btn_dive_in)

    driver.wait_until_element_is_visible(title)

    for i in range(1, 99):
        for n in range(1, 4):

            agencies_element = f'//div[@id="agency-tiles-widget"]/div/div[{i}]/div[{n}] //span[@class="h4 w200"]'
            amount_element = f'//div[@id="agency-tiles-widget"]/div/div[{i}]/div[{n}] //span[@class=" h1 w900"]'

            if not driver.is_element_visible(agencies_element):
                break

            driver.scroll_element_into_view(agencies_element)

            agency = driver.get_element_attribute(agencies_element, "innerText")

            amount = driver.get_element_attribute(amount_element, "innerText")

            fieldnames = ['Agency Name', 'Spend Amount']

            with open('data/agencies.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if (os.stat("data/agencies.csv").st_size == 0):
                    writer.writeheader()

                writer.writerow(
                    {
                        'Agency Name': agency, 
                        'Spend Amount': amount
                    })

    with pd.ExcelWriter('output/agencies.xlsx') as ew:
        pd.read_csv('data/agencies.csv').to_excel(ew, sheet_name="Agencies")



def select_individual_agencie():

    agency = f'//div[@id="agency-tiles-container"] //span[contains(text(), "{AGENCY}")]/.'
    ii_element = f'//h4[contains(text(),"Individual Investments")]'
    container = f'//*[@id="investments-table-container"]'
    btn_show_all = f'//*[@id="investments-table-object_length"] //option[@value="-1"]'
    pagination = f'//*[@id="investments-table-object_paginate"]/span/a[@data-dt-idx="3"]'

    driver.scroll_element_into_view(agency)

    driver.click_element(agency)

    driver.scroll_element_into_view(ii_element)

    driver.wait_until_element_is_visible(container, 20)

    driver.click_element(btn_show_all)

    driver.wait_until_element_is_not_visible(pagination, 60)

    for i in range(1, 9999):
        uii_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[1]'
        bureau_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[2]'
        investment_title_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[3]'
        total_spending_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[4]'
        i_type_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[5]'
        cio_rating_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[6]'
        of_projects_element = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[7]'

        if not driver.is_element_visible(uii_element):
            break

        driver.scroll_element_into_view(uii_element)

        uii = driver.get_element_attribute(uii_element, "innerText")
        bureau = driver.get_element_attribute(bureau_element, "innerText")
        investment_title = driver.get_element_attribute(investment_title_element, "innerText")
        total_spending = driver.get_element_attribute(total_spending_element, "innerText")
        i_type = driver.get_element_attribute(i_type_element, "innerText")
        cio_rating = driver.get_element_attribute(cio_rating_element, "innerText")
        of_projects = driver.get_element_attribute(of_projects_element, "innerText")

        fieldnames = ["UII", "Bureau", "Investment Title", "Total Spending", "Type", "CIO Rating", "of Projects"]

        title_file = AGENCY.lower().replace(" ", "_")

        with open(f'data/{title_file}.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if (os.stat(f'data/{title_file}.csv').st_size == 0):
                writer.writeheader()

            writer.writerow(
                {
                    "UII": uii,
                    "Bureau": bureau,
                    "Investment Title": investment_title,
                    "Total Spending": total_spending,
                    "Type": i_type,
                    "CIO Rating": cio_rating,
                    "of Projects": of_projects
                })

        uii_link = f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[1]/a'
        pdf_btn = f'//*[@id="business-case-pdf"]'
        generating_pdf_img = f'//img[@alt="Generating PDF"]'



        if driver.is_element_visible(uii_link):

            uui_url = driver.get_element_attribute(uii_link, "href")
            
            driver.open_chrome_browser(uui_url, preferences={"download.default_directory": DOWNLOADS_PATH})

            driver.wait_until_element_is_visible(pdf_btn)

            driver.click_element(pdf_btn)

            driver.wait_until_element_is_visible(generating_pdf_img, 5)

            driver.wait_until_element_is_not_visible(generating_pdf_img, 60)

            while any([filename.endswith(".crdownload") for filename in os.listdir(DOWNLOADS_PATH)]):
                time.sleep(2)
                print(".", end="")

            print("Download Completed!")

            driver.switch_browser(1)

    with pd.ExcelWriter(f'output/{title_file}.xlsx') as ew:

        pd.read_csv(
            f'data/{title_file}.csv').to_excel(ew, sheet_name=AGENCY)


if __name__ == "__main__":
    get_agency_expenses()
    select_individual_agencie()
