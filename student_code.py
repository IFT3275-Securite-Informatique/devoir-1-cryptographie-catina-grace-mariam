from crypt import *


def compter_frequences(texte, symboles):
    compteur = Counter()
    for symbole in symboles:
        compteur[symbole] = texte.count(symbole)
    return compteur
    

def calculer_frequences_relatives(compteur, total):
    return {symbole: compte / total for symbole, compte in compteur.items()}


def calculer_frequences_moyennes(urls, symboles):
    compteur_global = Counter()
    total_global = 0

    for url in urls:
        texte = load_text_from_web(url)
        if texte:
            compteur = compter_frequences(texte, symboles)
            total = sum(compteur.values())
            compteur_global.update(compteur)
            total_global += total

    frequences_moyennes = calculer_frequences_relatives(compteur_global, total_global)
    return frequences_moyennes


def analyser_frequences_chiffrees(C, longueur_sequence=8):
    """
    Analyse les fréquences des séquences de longueur donnée dans le texte chiffré.
    """
    compteur = Counter()
    for i in range(0, len(C), longueur_sequence):
        segment = C[i:i + longueur_sequence]
        compteur[segment] += 1
    total = sum(compteur.values())
    frequences_chiffrees = {segment: count / total for segment, count in compteur.items()}
    return frequences_chiffrees


def construire_dictionnaire_dechiffrement(freq_chiffrees, freq_moyennes):
    """
    Associe les séquences chiffrées aux symboles français basés sur leurs fréquences.
    """
    # Trier les séquences chiffrées par fréquence décroissante
    sequences_tries = [k for k, v in sorted(freq_chiffrees.items(), key=lambda x: x[1], reverse=True)]
    
    # Trier les symboles français par fréquence décroissante
    symboles_tries = [k for k, v in sorted(freq_moyennes.items(), key=lambda x: x[1], reverse=True)]
    
    # Créer le dictionnaire de correspondance
    dictionnaire_dechiffrement = {seq: sym for seq, sym in zip(sequences_tries, symboles_tries)}
    return dictionnaire_dechiffrement


def decrypt(C):
    """
    Déchiffre un texte chiffré en utilisant les fréquences moyennes pré-calculées.
    """
    # Liste des symboles à analyser
    symboles_fixes = symboles

    # URLs des textes pour calculer les fréquences moyennes
    urls = [
        "https://www.gutenberg.org/ebooks/135.txt.utf-8",  # Les Misérables - Victor Hugo
        "https://www.gutenberg.org/ebooks/19942.txt.utf-8",  # Candide - Voltaire
        "https://www.gutenberg.org/cache/epub/5423/pg5423.txt",
        "https://www.gutenberg.org/cache/epub/6318/pg6318.txt",
        "https://www.gutenberg.org/cache/epub/58698/pg58698.txt",
        "https://www.gutenberg.org/cache/epub/63144/pg63144.txt",
        "https://www.gutenberg.org/cache/epub/54873/pg54873.txt",
        "https://www.gutenberg.org/cache/epub/41211/pg41211.txt",
        "https://www.gutenberg.org/cache/epub/70891/pg70891.txt",
        "https://www.gutenberg.org/cache/epub/20262/pg20262.txt"
    ]

    # Étape 1 : Calculer les fréquences moyennes des symboles
    frequences_moyennes = calculer_frequences_moyennes(urls, symboles)

    # Étape 2 : Analyser les fréquences des séquences dans le texte chiffré
    freq_chiffrees = analyser_frequences_chiffrees(C)

    # Étape 3 : Construire le dictionnaire de déchiffrement
    dictionnaire_dechiffrement = construire_dictionnaire_dechiffrement(freq_chiffrees, frequences_moyennes)

    # Étape 4 : Déchiffrer le texte
    texte_dechiffre = ""
    for i in range(0, len(C), 8):
        segment = C[i:i + 8]
        if segment in dictionnaire_dechiffrement:
            texte_dechiffre += dictionnaire_dechiffrement[segment]
        else:
            texte_dechiffre += '?'  # Pour les séquences non reconnues

    return texte_dechiffre
