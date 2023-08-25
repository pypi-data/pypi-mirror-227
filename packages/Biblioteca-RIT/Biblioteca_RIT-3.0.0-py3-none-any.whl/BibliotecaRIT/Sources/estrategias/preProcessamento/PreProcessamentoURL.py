from BibliotecaRIT.Sources.estrategias.preProcessamento.PreProcessamentoStrategy import PreProcessamentoStrategy
from BibliotecaRIT.Sources.enums.EnumTag import EnumTag
import re

class PreProcessamentoURL(PreProcessamentoStrategy):
    _regExp = "(\[[^\]]*\]\()?http(s?):\/\/[^\s\t]+[\s\t]?(\))?"

    @classmethod
    def contem(cls, string: str) -> bool:
        return True if re.search(cls._regExp,string) is not None else False

    @staticmethod
    def getTag() -> EnumTag:
        return EnumTag.LINK

    @classmethod
    def remover(cls,string:str) -> str:
        match = re.search('\[[^\]]*\]\(http(s?):\/\/[^\s\t]+[\s\t]?\)',string)
        if  match is not None:
            particao = match.group().partition("]")
            return re.sub(cls._regExp,particao[0][1:],string)
        return re.sub(cls._regExp," ",string)


