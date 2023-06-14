import os
import sys
from textwrap import wrap
from PyPDF2 import PdfReader
from reportlab.lib.units import cm
from PyPDF2.errors import PdfReadError
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph


def files_writer(file_name: str) -> None:

    """
    Handle all the file writing for both file types conversions
    :param file_name: The file to be read / converted. The original file name will also be used for the new file
    :return: None
    """

    # Converting TXT File to PDF File
    if os.path.splitext(file_name.strip())[1].casefold() == '.txt':

        txt_file_content: [str] = txt_reader(file_name)  # Fetch the txt content

        document_template: SimpleDocTemplate = SimpleDocTemplate(resource_path(f"{os.path.splitext(file_name)[0]}.pdf"))
        full_text: [Paragraph, Spacer] = []  # "Paragraph" means paragraph and "Spacer" adds space

        # This works save for the fact that I have to append a "Spacer" with each iteration but seem to be unable to
        # [full_text.append(Paragraph('\n'.join(wrap(line, 95, drop_whitespace=False)))) for line in txt_file_content]

        # So I will use this instead of the list comprehension above :(
        for line in txt_file_content:
            paragraph: Paragraph = Paragraph('\n'.join(wrap(line, 95, drop_whitespace=False)))  # paragraph each line
            # of text
            full_text.append(paragraph)  # add the paragraph to the full text
            full_text.append(Spacer(1, 0.2 * cm))  # Add Line Spacing after each paragraph

        document_template.build(full_text, onFirstPage=pdf_page_template, onLaterPages=pdf_page_template)  # Create our
        # document using the defined settings / templates

        print('\n\tSUCCESS! Your PDF file has been successfully created!')

    # Converting PDF File to TXT File
    elif os.path.splitext(file_name.strip())[-1].casefold() == '.pdf':

        pdf_file_content: [str] = pdf_reader(file_name)  # Fetch the PDF content

        # Write the extracted data to a txt file
        with open(resource_path(f"{os.path.splitext(file_name)[0]}.txt"), "w", encoding='UTF-8') as new_txt_file:
            new_txt_file.writelines(pdf_file_content)

        print('\n\tSUCCESS! Your text file has been successfully created!')


def pdf_page_template(canvas, document):

    """
    Handle the settings and the overall page(s) structure
    :param canvas: The pdf generator to access the settings methods below
    :param document: The actual document / page object
    :return: None
    """

    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, f"Page {document.page}")  # Our Footer / Page Numbering
    canvas.restoreState()


def pdf_reader(pdf_file_name: str) -> [str]:

    """
    Open the PDF in read-binary mode & return its full contents for writing
    :param pdf_file_name: The file to be read / converted
    :return: The pdf contents as a list of string
    """

    with open(resource_path(f"{pdf_file_name}"), 'rb') as pdf_file:
        # Read the pdf (object)
        try:
            pdfreader: PdfReader = PdfReader(pdf_file)
            total_pages: int = len(pdfreader.pages)  # Get the number of pages
            full_text: [str] = []

            # Read data from all the pages
            [full_text.append(pdfreader.pages[page].extract_text()) for page in range(total_pages)]

            return full_text

        except PdfReadError as pdf_read_error:
            if 'EOF marker not found' in str(pdf_read_error):
                print('\n\tERROR! Unable to read your PDF file, it seems to be corrupt.')
            else:
                print('\n\tERROR! ', str(pdf_read_error))
            input('\nPress Enter to exit & try another file.')
            sys.exit(1)


def txt_reader(txt_file_name: str) -> [str]:

    """
    Read the text file and return the file content as a list of string
    :param: txt_file_name: The text file to be read / converted
    :return: The lines of the text file as a list of string
    """

    try:
        with open(resource_path(f"{txt_file_name}"), 'r', encoding='UTF-8') as txt_file:
            return [content for content in txt_file.readlines()]
    except UnicodeEncodeError:
        raise


def resource_path(relative_path) -> [bytes, str]:

    """
    For managing file resources.
    :param: relative_path: The relative path (relative to the script file) of the target file as a string
    :return: A list of bytes (file content) and string (file path)
    """

    base_path: [] = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
