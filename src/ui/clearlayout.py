def clearLayout(layout):
    ''' Used to clear all children out of layouts before redrawing them
    '''
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clearLayout(child)