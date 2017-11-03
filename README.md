# ProjetCombinatoire



Pour générer les tests avec `unittest`:

    cd rules/test/
    python3 -m unittest

L'option -m permet d'exécuter un module spécifique (ici unittest).
Quand appelé directement depuis Python, unittest cherche les tests unitaires présents dans le dossier courant.
Vous pouvez aussi lui donner un chemin de test à exécuter,
par exemple `unittest.test_Abstract.AbstractRuleTest.test__set_grammar`:

reférence: [OpenClassrooms](https://openclassrooms.com/courses/apprenez-a-programmer-en-python/les-tests-unitaires-avec-unittest#/id/r-2235381)

--------------------------------------------------------

Pour générer les tests classique, chaque fichier du package *rules* contient
des _asserts tests_ qui seront effectuées au lancement de:

    python3 AbstractRule.py

On peut tester l'ensemble des fichiers en utilisant la commande:

    python3 test_classic.py

Si aucune exception n'est levé alors le fichier passe les tests





