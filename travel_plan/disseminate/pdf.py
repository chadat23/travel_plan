from typing import Optional, Any

from fpdf import fpdf
from PIL import ImageFont


class PDF(fpdf.FPDF):

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)

        self.height = 6

    def add_cell(self, w: int, txt: str = '', roll: str = 'V', wrap: bool = False,
                 border: int = 0, ln: int = 0, align: str = '', fill: int = 0, link: str = '',
                 font_size: int = None) -> Optional[Any]:
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

        if roll.strip().lower() == 'l':
            _font_size = 8
            _font_style = 'B'
        elif roll.strip().lower() == 'v':
            _font_size = 5
            _font_style = ''

            if not wrap:
                for size in range(10, 5, -1):
                    font = ImageFont.truetype('arial.ttf', size)
                    dims = font.getsize(txt)[0]/75*25.4
                    if dims < w - 2:
                        _font_size = size
                        break
            else:
                pass

        if font_size:
            _font_size = font_size

        self.set_font('Arial', _font_style, size=_font_size)

        self.cell(w, self.height, txt, border, ln, align, fill, link)
