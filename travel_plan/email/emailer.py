import os
import shutil
import tempfile

from fpdf import FPDF


def email_pdf(start_date: str, entry_point: str, end_date: str, exit_point: str, tracked: str, plb: str,
              name0: str, call_sign0: str, pack_color0: str,
              name1: str, call_sign1: str, pack_color1: str,
              name2: str, call_sign2: str, pack_color2: str,
              name3: str, call_sign3: str, pack_color3: str,
              date0: str, start0: str, end0: str, route0: str, mode0: str,
              date1: str, start1: str, end1: str, route1: str, mode1: str,
              date2: str, start2: str, end2: str, route2: str, mode2: str,
              contact0: str, contact1: str,
              ):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    # pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")

    cell_height = 8

    pdf.cell(24, cell_height, 'Start Date: ', 1, 0, align='C')
    pdf.cell(40, cell_height, 'Entry Point: ', 1, 0, align='C')
    pdf.cell(24, cell_height, 'End Date: ', 1, 0, align='C')
    pdf.cell(40, cell_height, 'Exit Point: ', 1, 1, align='C')

    pdf.cell(24, cell_height, start_date, 1, 0, align='L')
    pdf.cell(40, cell_height, entry_point, 1, 0, align='L')
    pdf.cell(24, cell_height, end_date, 1, 0, align='L')
    pdf.cell(40, cell_height, exit_point, 1, 1, align='L')

    pdf.output('simple_table.pdf')

    # dirpath = tempfile.mkdtemp()
    # working_directory = os.getcwd()
    # # ... do stuff with dirpath
    # try:
    #     os.chdir(dirpath)
    #     pdf.output("simple_demo.pdf")
    # finally:
    #     os.chdir(working_directory)
    #     shutil.rmtree(dirpath)
