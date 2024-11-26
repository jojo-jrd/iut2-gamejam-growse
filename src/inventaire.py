from src.animate_element import AnimateElement
from src.objet import Objet
from src.image import Image

class Inventaire(AnimateElement):


    def __init__(self,max_quantite,selectionnee,position):
        super().__init__('main',position)
        self._contenu = {}
        self._indexs = {}
        self.__backgrounds = []
        self._list = ["weed", "water", "teq", "rose", "engrais", "piece"]
        self._max_quantite = max_quantite
        self._selectionnee = selectionnee

        self.initSprites()

    def initSprites(self):
        self.alignment = "middle"

        bg = Image((0,0), 'src/images/Personnage/inventaire-fr-' + str(1) + '.png', (-1,115))
        bg.loadBackground('src/images/Personnage/inventaire-en-' + str(1) + '.png', (-1,115), 'en')
        self.addSprite("main", bg)

        self.size = (-1, 115)

        self.add_contenu("piece",0)
        self.add_contenu("weed",0)
        self.add_contenu("water",0)
        self.add_contenu("teq",0)
        self.add_contenu("rose",0)
        self.add_contenu("engrais",0)


    def get_contenu(self):
        return self._contenu

    def get_indexs(self):
        return self._indexs

    def get_valeur_objet(self,obj):
        return self._contenu[obj]

    def get_max_quantite(self):
        return self._max_quantite

    def get_selectionnee(self):
        return self._selectionnee

    def loadImages(self,obj):
        if(self._contenu[obj] > 9):
            images = []
            i = 0
            concat = str(self._contenu[obj])
            for number in concat:
                images.append(Image((51 + self._list.index(obj) * 115 + i*7,0), 'src/images/chiffre/' + number + '.png'))
                images[i].size = (-1,15)
                self.addSprite('main',images[i])
                i += 1

            self._indexs[obj] = images
        else:
            img = Image((51 + self._list.index(obj) * 115,0), 'src/images/chiffre/' + str(self._contenu[obj]) + '.png')
            img.size = (-1,15)
            self.addSprite('main',img)
            self._indexs[obj] = [ img ]

    def add_contenu(self,obj,quantite):
        if not obj in self._contenu:
            self._contenu[obj] = 0
            self._indexs[obj] = []

        for img in self._indexs[obj]:
            self.removeSprite("main", img)

        self._contenu[obj] = max(self._contenu[obj] + quantite, 0)
        self.loadImages(obj)

    def soustraire_contenu(self,obj,quantite):
        self.add_contenu(obj, -quantite)

    def set_max_quantite(self,max_quantite):
        self._max_quantite = max_quantite

    def set_selectionnee(self,selectionnee):
        self.removeMode("main")

        bg = Image((0,0), 'src/images/Personnage/inventaire-fr-' + str(self._list.index(selectionnee) + 1) + '.png', (-1,115))
        bg.loadBackground('src/images/Personnage/inventaire-en-' + str(self._list.index(selectionnee) + 1) + '.png', (-1,115), 'en')
        self.addSprite("main", bg)
        self.size = (-1,115)

        for item in self._list:
            self.loadImages(item)

        self._selectionnee = selectionnee
