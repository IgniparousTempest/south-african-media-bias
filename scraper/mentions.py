from attr import dataclass


@dataclass
class Mentions:
    anc: int
    da: int
    eff: int


class MentionsParser:
    @classmethod
    def calculate_mentions(cls, text: str) -> Mentions:
        anc, da, eff = 0, 0, 0

        # Acronym occurrences
        anc += text.count('ANC')
        da += text.count('DA')
        eff += text.count('EFF')
        return Mentions(anc=anc, da=da, eff=eff)
