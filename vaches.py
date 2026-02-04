class Vache:
    AGE_MAX: int = 25
    poids_MAX: float = 1000.0
    PANSE_MAX: float = 50.0
    panse_MIN: float = 2.0

    _id: int
    _petitNom: str
    _age: int
    poids: float
    _panse: float
    RENDEMENT_RUMINATION: float = 0.25

    def __init__(self, petitNom, age, poids):
        self._petitNom = petitNom  # Utiliser l'attribut privé _petitNom
        self._age = age            # Utiliser l'attribut privé _age
        self._poids = poids        # Utiliser l'attribut privé _poids
        self._panse = 0            # Utiliser l'attribut privé _panse
        self.validerEtat()

    @property
    def age(self):
        return self._age

    @property
    def poids(self):
        return self._poids

    @property
    def panse(self):
        return self._panse

    @property
    def petitNom(self):
        return self._petitNom

    def __str__(self):
        pass

    def brouter(self, quantité, nourriture=None):
        if nourriture is not None:
            raise InvalidVacheException()

        if quantité <= 0:
            raise InvalidVacheException()

        if self._panse + quantité > self.PANSE_MAX:
            raise InvalidVacheException()

        self._panse += quantité

    def ruminer(self):
        if (self._panse <= 0):
            raise InvalidVacheException()
        else:
            panseAvant = self._panse
            gain = self.RENDEMENT_RUMINATION*panseAvant
            self._poids+= gain
            self._panse = 0

    def vieillir(self):
        self._age += 1
        self.validerEtat()

    def ajouterPanse(self, ajout):
        self._panse += ajout
        self.validerEtat()

    def validerEtat(self):
        if self._petitNom.strip() == "":
            raise InvalidVacheException()
        if self._age < 0 or self._age > self.AGE_MAX:
            raise InvalidVacheException()
        if self._poids < 0 or self._poids > self.poids_MAX:
            raise InvalidVacheException()
        if self._panse < 0 or self._panse > self.PANSE_MAX:
            raise InvalidVacheException()


class vacheALait(Vache):
    _RENDEMENT_LAIT: float = 1.1
    _PRODUCTION_LAIT: float = 40.0

    _laitDisponible: float
    _laitTotalProduit: float
    _laitTotalTraite: float


    def __init__(self, petitNom, age, poids):
        super().__init__(petitNom, age, poids)

    def ruminer(self):
        super().ruminer()

    @property
    def getLaitDisponible(self):
        return self._laitDisponible

    @property
    def getLaitTotalProduit(self):
        return self._laitTotalProduit

    @property
    def getLaitTotalTraite(self):
        return self._laitTotalTraite

    def traire(self, litre):
        if self.getLaitDisponible < litre or litre < 0:
            raise Exception(InvalidVacheException)
        else:
            self._laitDisponible -= litre
            self._laitTotalProduit += litre


class InvalidVacheException(Exception):
    pass
