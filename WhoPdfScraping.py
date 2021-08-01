from bs4 import BeautifulSoup
import requests
import os

# PDF Save Folder
download_folder = "inputs/"

who_url = "https://www.who.int/"
who_covid_url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"

# World Health Organization - COVID PDFs Page
html_page = requests.get(who_covid_url).content
soup = BeautifulSoup(html_page, features="lxml")

pdf_url_list = []
# Get all <a> elements from page
for link in soup.find_all('a'):
    element_link = link.get('href')
    # Check if href attribute contains pdf (only pdf links)
    if "pdf" in element_link:
        # print(element_link)
        # Check if the pdf link is unique in the list ( avoiding duplicates )
        if element_link not in pdf_url_list:
            pdf_url_list.append(element_link)

pdf_url_list.sort()

print("Found " + str(len(pdf_url_list)) + " PDFs.")
download = input("Download All Files and Save in '" + download_folder + "' folder? (y/n): ")


def get_file_name(file):
    aux = os.path.splitext(file)[0]
    aux = os.path.basename(aux+".pdf")
    return aux


sucess_count = 0
if download == "y" or download == "Y":
    for pdf_link in pdf_url_list:
        file_name = get_file_name(pdf_link)
        print("Downloading " + file_name + "...")
        pdf_file = requests.get(who_url + pdf_link)
        try:
            file = open(download_folder+file_name, 'wb')
            file.write(pdf_file.content)
            file.close()
            sucess_count += 1
        except:
            print("Error when saving file: " + file_name + "!")
    print("Successfully Downloaded ( " + str(sucess_count) + " of " + str(len(pdf_url_list)) + ") PDF Files.")
else:
    print("Exit")


