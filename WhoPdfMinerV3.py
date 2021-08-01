"""

V1 ->   Convert a single file from input folder (pdf) to output folder (csv).
        Generates a single CSV from a single PDF.

V2 ->   Convert All Files from input folder (pdf) to output folder (csv).
        Generates 1 CSV for each PDF File.

V3 ->   Convert All Files from input folder (pdf) to output folder (csv).
        Generates 1 CSV for all PDF Files.
"""

import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from collections import defaultdict
import pandas as pd
import os

# INPUT VALUES
pdf_input_folder = "inputs/"
csv_output_full_path = "outputs/covid-data.csv"


# Begin Code
def who_str_date_format(date_str):
    return date_str[0:4] + "/" + date_str[4:6] + "/" + date_str[6:8]


# PDF Mining Functions (majority from Lain)
def extract_layout_by_page(pdf_path):
    """
    Extracts LTPage objects from a pdf file.

    slightly modified from
    https://euske.github.io/pdfminer/programming.html
    """
    laparams = LAParams()

    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    layouts = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layouts.append(device.get_result())
    return layouts


getFolderFiles = [f for f in os.listdir(pdf_input_folder) if os.path.isfile(os.path.join(pdf_input_folder, f))]
filesList = []
for fileItem in getFolderFiles:
    last = fileItem.split('-')
    # Check if valid data
    if len(last[0]) == 8 and last[0].isnumeric():
        filesList.append({'file_name': fileItem, 'file_date': who_str_date_format(last[0])})
    else:
        filesList.append({'file_name': fileItem, 'file_date': '2020/01/01'})

print("Starting conversion for ", len(filesList), " file(s)...")

dict_final_data = defaultdict(list)

for fileDetail in filesList:
    # Set Final Input/Output Patch
    pdf_file_name_full = pdf_input_folder + fileDetail['file_name']
    csv_file_name_full = csv_output_full_path

    page_layouts = extract_layout_by_page(pdf_file_name_full)

    for page_num in range(0, len(page_layouts)):
        objects_on_page = set(type(o) for o in page_layouts[page_num])

        TEXT_ELEMENTS = [
            pdfminer.layout.LTTextBox,
            pdfminer.layout.LTTextBoxHorizontal,
            pdfminer.layout.LTTextLine,
            pdfminer.layout.LTTextLineHorizontal
        ]


        def flatten(lst):
            """Flattens a list of lists"""
            return [subelem for elem in lst for subelem in elem]


        def extract_characters(element):
            """
            Recursively extracts individual characters from
            text elements.
            """
            if isinstance(element, pdfminer.layout.LTChar):
                return [element]

            if any(isinstance(element, i) for i in TEXT_ELEMENTS):
                return flatten([extract_characters(e) for e in element])

            if isinstance(element, list):
                return flatten([extract_characters(l) for l in element])

            return []


        current_page = page_layouts[page_num]

        texts = []
        rects = []

        # seperate text and rectangle elements
        for e in current_page:
            if isinstance(e, pdfminer.layout.LTTextBoxHorizontal):
                texts.append(e)
            elif isinstance(e, pdfminer.layout.LTRect):
                rects.append(e)

        # sort them into
        characters = extract_characters(texts)

        box_char_dict = defaultdict(list)
        box_char_dict2 = defaultdict(list)

        for c in characters:
            if str(c.y0) in box_char_dict:
                if abs(float(box_char_dict[str(c.y0)]) - float(c.x0)) > 10:
                    box_char_dict2[str(c.y0)].append("$%*")
                    box_char_dict2[str(c.y0)].append(c.get_text())
                else:
                    box_char_dict2[str(c.y0)].append(c.get_text())
                box_char_dict[str(c.y0)] = c.x1
            else:
                box_char_dict[str(c.y0)] = c.x1
                box_char_dict2[str(c.y0)].append(c.get_text())

        for k, v in box_char_dict2.items():
            country = ""
            conf = ""
            conf_new = ""
            death = ""
            death_new = ""
            start = 0
            item = 0
            while item < len(v):
                if item + 1 == len(v):
                    break
                if v[item] == "$%*":
                    start = start + 1
                    item = item + 1
                if v[item] != " ":
                    if start == 0:
                        country = country + v[item]
                    if start == 1:
                        conf = conf + v[item]
                    if start == 2:
                        conf_new = conf_new + v[item]
                    if start == 3:
                        death = death + v[item]
                    if start == 4:
                        death_new = death_new + v[item]
                item = item + 1
            try:
                # This Try Block allows that the code stores only VALID table rows from WHO (and discard all invalid/corrupted data rows)
                conf = int(conf)
                conf_new = int(conf_new)
                death = int(death)
                death_new = int(death_new)
                if not country.isdecimal() and country != "":
                    dict_final_data['date'].append(fileDetail['file_date'])
                    dict_final_data['country_territory_area'].append(country)
                    dict_final_data['total_confirmed_cases'].append(conf)
                    dict_final_data['total_confirmed_new_cases'].append(conf_new)
                    dict_final_data['total_deaths'].append(death)
                    dict_final_data['total_new_deaths'].append(death_new)
            except:
                continue

    print("File: " + fileDetail['file_name'] + " -> Done!")

# Save all valid table rows in a CSV file
df = pd.DataFrame(dict_final_data,
                  columns=['date', 'country_territory_area', 'total_confirmed_cases', 'total_confirmed_new_cases',
                           'total_deaths', 'total_new_deaths'])
df = df.sort_values(by=['date', 'country_territory_area'])
df.to_csv(csv_file_name_full, encoding='utf-8-sig', date_format='%Y%m%d', index=False, header=True)

print("Complete!\nCSV File has been saved.")
