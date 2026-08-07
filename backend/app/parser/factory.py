from app.parser.hdfc.parser import HDFCParser
from app.parser.pnb.parser import PNBParser


class ParserFactory:

    _parsers = {
        "HDFC": HDFCParser,
        "PNB": PNBParser,
    }

    @classmethod
    def get_parser(cls, bank: str):

        parser_class = cls._parsers.get(bank)

        if parser_class is None:
            raise ValueError(
                f"Unsupported bank: {bank}"
            )

        return parser_class()
