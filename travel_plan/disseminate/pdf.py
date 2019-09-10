from typing import Optional, Any

from fpdf import fpdf


class PDF(fpdf.FPDF):

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)

        self.height = 6

        # self.label_font = 'Arial'
        # self.label_style = 'b'
        # self.label_size = 8
        #
        # self.label_font = 'Arial'
        # self.label_style = ''
        # self.label_size = 6

    def set_label_font(self, font: str = 'Arial', style: str = 'b', size: int = 8):
        self.label_font = font
        self.label_style = style
        self.label_size = size

    def set_value_font(self, font: str = 'Arial', style: str = '', size: int = 5):
        self.label_font = font
        self.label_style = style
        self.label_size = size

    def add_cell(self,  w: int, txt: str = '', roll: str = 'V', wrap: bool = False,
             border: int = 0, ln: int = 0, align: str = '', fill: int = 0, link: str = '') -> Optional[Any]:
        '''
        Fits and formats the text to the cell that it's supposed to fit into.

        :param width: Width of the cell in mm.
        :type width: int
        :param text: The string that is to be put in the cell
        :type text: str
        :param roll: Specifies whether the text is a Label or Value: "L" or "V" is expected
        :type roll:
        :param wrap: Whether or not the text should wrap within the cell.
        :return:
        :rtype:
        '''
        mm_per_letter = {1.667: 10,
                         1.486: 9,
                         1.31: 8,
                         1.122: 7,
                         0.932: 6
                         }

        if roll.strip().lower() == 'l':
            font_size = 8
            font_style = 'B'
        elif roll.strip().lower() == 'v':
            font_size = 5
            font_style = ''

            if not wrap:
                space_per_letter = w / len(txt)
                for mm, size in mm_per_letter.items():
                    if space_per_letter > mm:
                        font_size = size
                        break
            else:
                pass

        self.set_font('Arial', font_style, size=font_size)
        # self.set_font('Arial', '', size=8)

        self.cell(w, self.height, txt, border, ln, align, fill, link)
