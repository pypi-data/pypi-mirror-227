import qrcode
from PIL import Image, ImageDraw
from path import Path


class QRCode:
    BLACK_LINE = (0, 0, 0, 230)
    WHITE_LINE_BEFORE = (255, 255, 255, 50)
    WHITE_LINE_AFTER = (255, 255, 255, 230)

    def __init__(self, text: str, coeff: int = 10) -> None:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        qr.add_data(text)
        qr.make(fit=True)
        self.img = qr.get_matrix()
        self.coeff = coeff
        self.coeff_small = round(self.coeff / 3)
        self.length_qr = len(self.img) * self.coeff
        self.back_im = Image.new("RGBA", (self.length_qr, self.length_qr), (0, 0, 0, 0))
        self.idraw = ImageDraw.Draw(self.back_im, "RGBA")

    def gen_qr_code(self, path_to_download: Path, path_to_save: Path = None) -> bool:
        try:
            background = (
                Image.open(path_to_download)
                .resize((self.length_qr, self.length_qr))
                .convert("RGBA")
            )
        except:
            return False

        background = self.__get_qr_code_with_img(background)
        if path_to_save is not None:
            path_to_download = path_to_save

        background.save(path_to_download)
        return True

    def __get_qr_code_with_img(self, background):
        x = 0
        y = 0
        for string in self.img:
            for i in string:
                fill = self.BLACK_LINE if i else self.WHITE_LINE_AFTER
                self.idraw.rectangle(
                    (
                        x + self.coeff_small,
                        y + self.coeff_small,
                        x + self.coeff - self.coeff_small,
                        y + self.coeff - self.coeff_small,
                    ),
                    fill=fill,
                )
                x += self.coeff
            x = 0
            y += self.coeff

        operations = (
            (
                (0, 0, self.coeff * 9, self.coeff * 9),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (self.length_qr - self.coeff * 9, 0, self.length_qr, self.coeff * 9),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (0, self.length_qr - self.coeff * 9, self.coeff * 9, self.length_qr),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 9,
                    self.length_qr - self.coeff * 6,
                    self.length_qr - self.coeff * 6,
                ),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (self.coeff, self.coeff, self.coeff * 8, self.coeff * 2),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 8,
                    self.coeff,
                    self.length_qr - self.coeff,
                    self.coeff * 2,
                ),
                self.BLACK_LINE,
            ),
            (
                (self.coeff, self.coeff * 7, self.coeff * 8, self.coeff * 8),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 8,
                    self.coeff * 7,
                    self.length_qr - self.coeff,
                    self.coeff * 8,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.coeff,
                    self.length_qr - self.coeff * 8,
                    self.coeff * 8,
                    self.length_qr - self.coeff * 7,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.coeff,
                    self.length_qr - self.coeff * 2,
                    self.coeff * 8,
                    self.length_qr - self.coeff,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 8,
                    self.length_qr - self.coeff * 8,
                    self.length_qr - self.coeff * 7,
                    self.length_qr - self.coeff * 7,
                ),
                self.BLACK_LINE,
            ),
            (
                (self.coeff * 3, self.coeff * 3, self.coeff * 6, self.coeff * 6),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 6,
                    self.coeff * 3,
                    self.length_qr - self.coeff * 3,
                    self.coeff * 6,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.coeff * 3,
                    self.length_qr - self.coeff * 6,
                    self.coeff * 6,
                    self.length_qr - self.coeff * 3,
                ),
                self.BLACK_LINE,
            ),
            (
                (self.coeff, self.coeff, self.coeff * 2, self.coeff * 8),
                self.BLACK_LINE,
            ),
            (
                (self.coeff * 7, self.coeff, self.coeff * 8, self.coeff * 8),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 2,
                    self.coeff,
                    self.length_qr - self.coeff,
                    self.coeff * 8,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 8,
                    self.coeff,
                    self.length_qr - self.coeff * 7,
                    self.coeff * 8,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.coeff,
                    self.length_qr - self.coeff * 8,
                    self.coeff * 2,
                    self.length_qr - self.coeff,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.coeff * 7,
                    self.length_qr - self.coeff * 8,
                    self.coeff * 8,
                    self.length_qr - self.coeff,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 9,
                    self.length_qr - self.coeff * 5,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 6,
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 5,
                    self.length_qr - self.coeff * 5,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 6,
                    self.length_qr - self.coeff * 9,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.length_qr - self.coeff * 10,
                    self.length_qr - self.coeff * 6,
                    self.length_qr - self.coeff * 6,
                    self.length_qr - self.coeff * 5,
                ),
                self.BLACK_LINE,
            ),
        )

        for xy, fill in operations:
            self.idraw.rectangle(
                xy,
                fill=fill,
            )

        background.paste(self.back_im, (0, 0), self.back_im)
        return background
