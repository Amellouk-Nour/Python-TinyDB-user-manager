import re
import string
from tinydb import TinyDB, where
from pathlib import Path
# from pprint import pprint

class User :
    """
    La classe User a été créée pour gérer les utilisateurs.
    Avec cette classe, vous pouvez créer des utilisateurs en
    spécifiant leur nom, prénom, numéro et adresse.
    À l'aide de TinyDB, vous pouvez créer une base de données d'utilisateurs
    dans laquelle vous pouvez ajouter, supprimer et interroger des utilisateurs.
    Cette classe offre la possibilité de retrouver les données d'un utilisateur uniquement à
    partir de son nom.

    """
    # le chemin où va être stoker notre base de données des Utilisateur :

    mon_chemin = Path(__file__).resolve().parent / 'db.json'

    # notre connexion à la base de données et à la table Utilisateur :

    db = TinyDB(mon_chemin, indent = 4)
    Utilisateurs = db.table("Users")

    # initialisation des instances de classes :

    def __init__(self, first_name : str, last_name : str, address : str = '', phone_number : str = ''):
        # initialisation des attribut d'instance :

        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number

        # vérification de la validité des données insérer :

        self._check_name()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    # cherche l'utilisateur dans la base de donnée à partir d'une instance donnée :
    @property
    def db_instance(self):
        return User.Utilisateurs.get(
(where('first_name') == self.first_name) & (where('last_name') == self.last_name)
        )
            
    def __str__(self):
        if not self.address and not self.phone_number:
            return f"User({self.full_name})"
        elif not self.address and self.phone_number :
            return f"User({self.full_name}, {self.phone_number})"
        elif self.address and not self.phone_number :
            return f"User({self.full_name}, {self.address})"
        else :
            return f"User({self.full_name}, {self.phone_number}, {self.address})"
    
    def __repr__(self):
        if not self.address and not self.phone_number:
            return f"User({self.full_name})"
        elif not self.address and self.phone_number :
            return f"User({self.full_name}, {self.phone_number})"
        elif self.address and not self.phone_number :
            return f"User({self.full_name}, {self.address})"
        else :
            return f"User({self.full_name}, {self.phone_number}, {self.address})"
    
    # vérification de la validité du numéro :

    def _check_phone_number(self):
            phone_digits = re.sub(r"[+()<\s]*","",self.phone_number)
            if len(phone_digits)<10 or not phone_digits.isdigit():
                    raise ValueError(f"le numero de telephone {self.phone_number} est invalide")
            
    # vérification de la validité des nom :

    def _check_name(self):

        if not self.first_name or not self.last_name :
            raise ValueError(f" le nom ou le prenom ne peuvent pas être vide")

        #vérifer si les nom ne contiennent pas de caractère spéciale :
        special_caracter = string.punctuation + string.digits
        if any(char in special_caracter for char in self.full_name):
            raise ValueError(f"le nom ou le prenom ne peuvent pas contenir de caractère spécial")
    
    # méthode qui vérifier la validité du numero et du nom des utilisateurs :
    def _checks(self):
        self._check_name()
        self._check_phone_number()

    # méthode qui permet d'insérer un utilisateur dans la base de donnée :
    def save(self) -> int:
        if self.exist():
            return -1
        return self.Utilisateurs.insert(self.__dict__)
    
    # méthode qui permet de vérifier si un utilisateur existe dans la base de donnée :
    def exist(self) -> bool:
        return bool(self.db_instance)

    # méthode qui permet de supprimer un utilisateur si il éxiste :
    def delete(self) -> list[int]:
        if self.exist() :
            User.Utilisateurs.remove(doc_ids=[self.db_instance.doc_id])
        return []
    
# retoune tous les utilisateur enregistrée dans la base de donnée :

def get_all_users() -> list[User]:
    return [User(**user) for user in User.Utilisateurs.all()]
# si vous voullez importer se code, sans éxecuter la partie teste, cette condition le permet
if __name__=='__main__':    
    # pprint(get_all_users())
    # from faker import Faker
    # fake = Faker("fr_FR")
    # for _ in range(10):
    #     user = User(fake.first_name(),fake.last_name(), fake.address().replace("\n",', '),fake.phone_number())
    #     print(user.save())
    # test= User("Louise","Marques")
    # test.delete()
    pass