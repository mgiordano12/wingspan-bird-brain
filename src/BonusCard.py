class BonusCard:

    #===================================================================================================================
    def __init__(self, name, expansion, automa, condition, explanatory_text, vp, percent, note, vp_average, id, rulings):
        self.name = name
        self.expansion = expansion
        self.automa = automa
        self.condition = condition
        self.explanatory_text = explanatory_text
        self.vp = vp
        self.percent = percent
        self.note = note
        self.vp_average = vp_average
        self.id = id
        self.rulings = rulings

    #===================================================================================================================
    def __repr__(self):
        return f"Bonus: {self.name}"