from attr import dataclass


@dataclass
class Mentions:
    anc: int
    da: int
    eff: int


class MentionsParser:
    @classmethod
    def calculate_mentions(cls, text: str) -> Mentions:
        text_lower = text.lower()
        words = text.split()
        anc, da, eff = 0, 0, 0

        # Acronym occurrences
        anc += words.count('ANC') + text_lower.count('african national congress')
        da += words.count('DA') + text_lower.count('democratic alliance')
        eff += words.count('EFF') + text_lower.count('economic freedom fighters')
        return Mentions(anc=anc, da=da, eff=eff)
