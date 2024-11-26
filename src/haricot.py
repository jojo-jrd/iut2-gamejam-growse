from src.plante import Plante
from src.image import Image

class Haricot(Plante):

    __maxNiveau = 14

    # -- Constructors --

    def __init__(self,nom,niveau,besoins,position):

        super().__init__(nom,niveau,besoins,position)
        # Loadings
        self.loadBackground("src/images/Haricot/haricot-"+str(niveau)+".png")
        self._spritesChiffre = {}
        self.loadSpriteNiveau()


    def __del__(self):
        self.current_mode = 'mort'

    # FONCTIONNALITES

    def loadSpriteNiveau(self):
        if(self.getNiveau() > 9):
            images = []
            i = 0
            concat = str(self.getNiveau())
            for number in concat:
                images.append(Image((55 + (i * 5),1080), 'src/images/chiffre/' + number + '.png'))
                images[i].alignment = "middle"
                images[i].size = (-1,15)
                self.addSprite('main',images[i])
                i += 1

            self._spritesChiffre[self._niveau] = images

        else:
            img = Image((55,1080), 'src/images/chiffre/' + str(self._niveau) + '.png')
            img.alignment = "middle"
            img.size = (-1,15)
            self.addSprite('main',img)
            self._spritesChiffre[self._niveau] = [ img ]

    def monterNiveau(self,inventaire):

        nb_engrais = inventaire.get_valeur_objet('engrais')

        if(self.getNiveau()!=self.__maxNiveau):
            besoins = self.getBesoins()
            for b in besoins.keys():
                if(b=="engrais"):
                    if(besoins[b]<=nb_engrais):
                        for img in self._spritesChiffre[self._niveau]:
                            self.removeSprite('main',img)

                        self.setNiveau(self.getNiveau()+1)

                        self.loadSpriteNiveau()
                        self.loadBackground("src/images/Haricot/haricot-"+str(self.getNiveau())+".png")
                        inventaire.soustraire_contenu("engrais",besoins[b])
                        return True
                    else:
                        return False
        return False



    def estFinie(self):
        return (super().getNiveau()==self.__maxNiveau)
