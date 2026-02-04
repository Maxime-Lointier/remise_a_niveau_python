from enum import Enum


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
        self._age = age  # Utiliser l'attribut privé _age
        self._poids = poids  # Utiliser l'attribut privé _poids
        self._panse = 0  # Utiliser l'attribut privé _panse
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
        return (f"Nom : {self._petitNom}\n"
                f"Âge : {self._age} ans\n"
                f"Poids : {self._poids} kg\n"
                f"Panse : {self._panse} kg")

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
            gain = self.RENDEMENT_RUMINATION * panseAvant
            self._poids += gain
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


class VacheALait(Vache):
    RENDEMENT_LAIT: float = 1.1
    PRODUCTION_LAIT_MAX: float = 40.0

    lait_disponible: float
    lait_total_produit: float
    lait_total_traite: float

    def __init__(self, petitNom, age, poids):
        super().__init__(petitNom, age, poids)

        self.lait_disponible = 0.0
        self.lait_total_produit = 0.0
        self.lait_total_traite = 0.0

    def ruminer(self):
        if (self._panse <= 0):
            raise InvalidVacheException()
        else:

            panseAvant = self._panse
            gain = self.RENDEMENT_RUMINATION * panseAvant
            lait_produit = self.RENDEMENT_LAIT * panseAvant

            if self.lait_disponible + lait_produit > self.PRODUCTION_LAIT_MAX:
                raise InvalidVacheException()

            self._poids += gain
            lait = self.RENDEMENT_LAIT * panseAvant
            self.lait_disponible += lait
            self.lait_total_produit += lait
            self._panse = 0

    def __str__(self):
        base = super().__str__()  # ✅ Récupère la représentation de Vache
        return (f"{base}\n"
                f"Lait disponible : {self.lait_disponible} L\n"
                f"Lait total produit : {self.lait_total_produit} L\n"
                f"Lait total trait : {self.lait_total_traite} L")

    @property
    def getLaitDisponible(self):
        return self.lait_disponible

    @property
    def getLaitTotalProduit(self):
        return self.lait_total_produit

    @property
    def getLaitTotalTraite(self):
        return self.lait_total_traite

    def traire(self, litre):
        if self.getLaitDisponible < litre or litre <= 0:
            raise InvalidVacheException
        else:
            self.lait_disponible -= litre
            lait = litre
            self.lait_total_traite += litre
            return lait


class TypeNourriture(Enum):
    MARGUERITE = "marguerite"
    HERBE = "herbe"
    FOIN = "foin"
    PAILLE = "paille"
    CEREALES = "cereales"


COEFFICIENT_NUTRITIONNEL = {
    TypeNourriture.MARGUERITE: 1.1,
    TypeNourriture.HERBE: 1.0,
    TypeNourriture.FOIN: 0.8,
    TypeNourriture.PAILLE: 0.5,
    TypeNourriture.CEREALES: 1.5,
}


class Ration:
    def __init__(self, quantite: float, type_nourriture: TypeNourriture):
        self.quantite = quantite
        self.type_nourriture = type_nourriture


class PieNoire(VacheALait):
    _nombreTacheNoire: int
    _nombreTacheBlanche: int
    COEFFICIENT_LAIT_PAR_NOURRITURE: dict < TypeNourriture > float

    def __init__(self, petitNom, age, poids, nombreTacheNoire, nombreTacheBlanche):
        super().__init__(petitNom, age, poids)
        self._nombreTacheNoire = nombreTacheNoire
        self._nombreTacheBlanche = nombreTacheBlanche

    @property
    def nombreTacheNoire(self):
        return self._nombreTacheNoire

    @property
    def nombreTacheBlanche(self):
        return self._nombreTacheBlanche

    def brouter(self, quantite: float, nourriture: TypeNourriture = None):

        if nourriture is None:
            raise InvalidVacheException()

        if quantite <= 0:
            raise InvalidVacheException()

        coeff = COEFFICIENT_NUTRITIONNEL.get(nourriture, 1.0)
        quantite_effective = quantite * coeff

        if self._panse + quantite_effective > self.PANSE_MAX:
            raise InvalidVacheException()

        self._panse += quantite_effective

    def ruminer(self):
        """
        Override ruminer() pour utiliser le coefficient de lait par nourriture
        """
        if self._panse <= 0:
            raise InvalidVacheException()

        panseAvant = self._panse

        gain_poids = self.RENDEMENT_RUMINATION * panseAvant

        lait_produit = self.RENDEMENT_LAIT * panseAvant

        if self.lait_disponible + lait_produit > self.PRODUCTION_LAIT_MAX:
            raise InvalidVacheException()

        self._poids += gain_poids
        self.lait_disponible += lait_produit
        self.lait_total_produit += lait_produit
        self._panse = 0

        return lait_produit


class InvalidVacheException(Exception):
    pass
