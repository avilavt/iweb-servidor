class Description:

    def __init__(self, description):
        self.description = description

    def getDescription(self):
        descripcion = list()
        desc = self.description.replace('<b>', '#').replace('</b>', '#').replace('<', '#').replace('>', '#').split('#')
        indexK = desc.index('Kilómetros:')
        km = float(desc[indexK+1].replace('&nbsp;',' ').strip().replace(',','.'))
        indexD = desc.index('Descripción:')
        descripcion.append({'kilometers':km,'description':desc[indexD+1].replace('&nbsp;',' ').strip()})
        return descripcion
