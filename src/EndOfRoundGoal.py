class EndOfRoundGoal:

    #===================================================================================================================
    def __init__(self, name, expansion, duet, condition, explanatory_text, id):
        self.name = name
        self.expansion = expansion
        self.duet = duet
        self.condition = condition
        self.explanatory_text = explanatory_text
        self.id = id
    
    #===================================================================================================================
    def __repr__(self):
        return f"EndOfRoundGoal: {self.name}"