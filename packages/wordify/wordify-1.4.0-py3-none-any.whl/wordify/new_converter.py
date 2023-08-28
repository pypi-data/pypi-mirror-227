class ConvertBehavior:
    _position_names = [
        "", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion",
        "septillion", "octillion", "nonillion", "decillion", "un-decillion", "duo-decillion",
        "tre-decillion", "quattuor-decillion", "quin-decillion", "sex-decillion", "septen-decillion",
        "octo-decillion", "novem-decillion", "vigintillion", "un-vigintillion", "duo-vigintillion",
        "tres-vigintillion", "quattuor-vigintillion", "quin-vigintillion", "ses-vigintillion",
        "septen-vigintillion", "octo-vigintillion", "novem-vigintillion", "trigintillion",
        "un-trigintillion", "duo-trigintillion", "tres-trigintillion", "quattour-trigintillion",
        "quin-trigintillion", "ses-trigintillion", "septen-trigintillion", "otcto-trigintillion",
        "novem-trigintillion", "quadragintillion", "un-quadragintillion", "duo-quadragintillion",
        "tre-quadragintillion", "quattuor-quadragintillion", "quin-quadragintillion",
        "sex-quadragintillion", "septen-quadragintillion", "octo-quadragintillion",
        "novem-quadragintillion", "quinquagintillion", "un-quinquagintillion", "duo-quinquagintillion",
        "tre-quinquagintillion", "quattuor-quinquagintillion", "quin-quinquagintillion",
        "sex-quinquagintillion", "septen-quinquagintillion", "octo-quinquagintillion",
        "novem-quinquagintillion", "sexagintillion", "un-sexagintillion", "duo-sexagintillion",
        "tre-sexagintillion", "quattuor-sexagintillion", "quin-sexagintillion", "sex-sexagintillion",
        "septen-sexagintillion", "octo-sexagintillion", "novem-sexagintillion", "septuagintillion",
        "un-septuagintillion", "duo-septuagintillion", "tre-septuagintillion",
        "quattuor-septuagintillion", "quin-septuagintillion", "sex-septuagintillion",
        "septen-septuagintillion", "octo-septuagintillion", "novem-septuagintillion", "octogintillion",
        "un-octogintillion", "duo-octogintillion", "tre-octogintillion", "quattuor-octogintillion",
        "quin-octogintillion", "sex-octogintillion", "septen-octogintillion", "octo-octogintillion",
        "novem-octogintillion", "nonagintillion", "un-nonagintillion", "duo-nonagintillion",
        "tre-nonagintillion", "quattuor-nonagintillion", "quin-nonagintillion", "sex-nonagintillion",
        "septen-nonagintillion", "octo-nonagintillion", "novem-nonagintillion", "centillion"
    ]

    _names = {
        '9': 'nine', '8': 'eight', '7': 'seven', '6': 'six', '5': 'five',
        '4': 'four', '3': 'three', '2': 'two', '1': 'one', '0': '',
        '19': 'nineteen', '18': 'eighteen', '17': 'seventeen', '16': 'sixteen',
        '15': 'fifteen', '14': 'fourteen', '13': 'thirteen', '12': 'twelve',
        '11': 'eleven', '10': 'ten',
        '90': 'ninety', '80': 'eighty', '70': 'seventy', '60': 'sixty', '50': 'fifty',
        '40': 'forty', '30': 'thirty', '20': 'twenty',
    }

    def __init__(self):
        self.position = 0

    def _convert_group_to_word(self, group):
        res = ""
        if group[0] != '0':
            res += f"{self._names[group[0]]} hundred "
        if group[1] != '0':
            if group[1] != '1':
                res += f"{self._names[group[1]+'0']} {self._names[group[2]]} "
            else:
                res += f"{self._names[group[1]+group[2]]} "
        else:
            res += f"{self._names[group[2]]} "
        res += f"{self._position_names[self.position]} and "
        self.position += 1
        return res

    def _convert_to_token(self, number):
        if number == '0':
            return 'zero'
        return self._names[str(number)]

    def convert(self, number, is_negative=False):
        pass


class TokenConverter(ConvertBehavior):
    def convert(self, number, is_negative=False):
        result = ""
        for n in number:
            result += f"{self._convert_to_token(n)} "
        while result.startswith("zero "):
            result = result[5:]
        if is_negative:
            result = f"negative {result}"
        return result[:-1]


class IntegerConverter(ConvertBehavior):
    def convert(self, number, is_negative=False):
        result = ""
        for i in range(len(number) - 3, -1, -3):
            group = number[i:i + 3]
            result = self._convert_group_to_word(group) + result
        if is_negative:
            result = f"negative {result}"
        return result[:-6]


class DecimalConverter(ConvertBehavior):
    def convert(self, number, is_negative=False):
        decimal_part = None
        if '.' in number:
            integer_part, decimal_part = str(number).split('.')
        else:
            integer_part = str(number)
        result = ""
        for i in range(len(integer_part) - 3, -1, -3):
            group = integer_part[i:i + 3]
            result = self._convert_group_to_word(group) + result
        if decimal_part:
            result = f"{result[:-6]} point"
            for n in decimal_part:
                result += f" {self._convert_to_token(n)}"
            return result
        if is_negative:
            result = f"negative {result}"
        return result[:-6]


class NumberHandler:
    def __init__(self, converter, number=0):
        self.original_number = ''
        self.padded_number = ''
        self.is_negative = False
        self.converter = converter
        self.set_number(number)

    def set_converter(self, converter):
        self.converter = converter

    def _pad_number(self):
        padding = (3 - len(self.original_number) % 3) % 3
        return '0' * padding + self.original_number

    def set_number(self, number):
        self.converter.position = 0
        self.is_negative = number < 0
        self.original_number = str(number)
        if self.original_number.startswith('-'):
            self.original_number = self.original_number[1:]
        self.padded_number = self._pad_number()

    def convert(self):
        return self.converter.convert(self.padded_number, self.is_negative)

    def convert_to_tokens(self):
        self.converter = TokenConverter()
        return self.converter.convert(self.padded_number, self.is_negative)


class IntegerNumber(NumberHandler):
    def __init__(self):
        super().__init__(IntegerConverter())

    def set_number(self, number):
        if not isinstance(number, int):
            raise TypeError("Invalid input type. Number must be an integer.")
        super().set_number(number)


class DecimalNumber(NumberHandler):
    def __init__(self):
        super().__init__(DecimalConverter())

    def set_number(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Invalid input type. Number must be an integer or float.")
        super().set_number(number)
