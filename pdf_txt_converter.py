import os
import sys
from payload.work_horse import files_writer


def script_summary() -> None:
    print('''
               ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                     \t***------------------------------------------------------------------------***\n

        \t"PDF<-->TXT~CONVERTER" Version 1.0.0\n

        This bot will help you convert a pdf file to a txt (text based) file and create a pdf
        file from a txt file. All you need to do is provide the name of the file you want 
        to read / convert.

        Cheers!!
    ''')


def pdf_txt_bot(file_name: str) -> None:
    try:
        files_writer(file_name)

    except FileNotFoundError:
        if FileNotFoundError:
            print(
                '\n\t*** Unable to locate your file. Please make sure you provide a valid file name & '
                'file extension within this folder. ***')

    input('\nPress Enter to Exit.')
    sys.exit(0)


def main() -> None:
    script_summary()
    file_name: str = input('\nPlease type file name (with extension) and Press Enter: ')

    if len(file_name.strip()) >= 5:
        if not os.path.splitext(file_name)[-1].casefold() == '.pdf' and not os.path.splitext(file_name)[-1].casefold() \
                                                                            == '.txt':
            input('\nPlease provide a valid pdf or txt file name.')
        else:
            pdf_txt_bot(file_name)

    elif len(file_name.strip()) < 5 or os.path.splitext(file_name.strip()[-1]) == '':
        print('\nPlease provide a valid file name.')
        input('\nPress Enter to Exit: ')
        sys.exit(1)


if __name__ == '__main__':
    main()
