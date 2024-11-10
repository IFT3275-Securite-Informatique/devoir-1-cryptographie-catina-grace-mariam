import re
from collections import Counter

def load_text(file_path):
    #charger texte d un fichier local
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().lower()
    except FileNotFoundError:
        print("fichier pas trouvé.")
        return None

def frequency_analysis(text):
    #efffectuer analyse de freq des caractères et des bigrammes dans le texte
    # Comptage des caractères
    char_freq = Counter(cleaned_text)
    
    # Comptage des bigrammes
    bigrams = [cleaned_text[i:i+2] for i in range(len(cleaned_text)-1)]
    bigram_freq = Counter(bigrams)
    
    return char_freq, bigram_freq

def create_decryption_map(cipher_freq, reference_freq):
    #crée carte de décryptage en associant les symboles les plus fréquents du texte chiffré avec ceux de référence."""
    cipher_sorted = sorted(cipher_freq.items(), key=lambda item: item[1], reverse=True)
    reference_sorted = sorted(reference_freq.items(), key=lambda item: item[1], reverse=True)
    
    # Associer les elem de cipher_sorted à reference_sorted
    return {cipher[0]: reference[0] for cipher, reference in zip(cipher_sorted, reference_sorted)}

def decrypt_text(ciphertext, decrypt_map):
    #Déchiffre texte en utilisant la carte de décryptage 

    # Déchiffrer caractères
    decrypted_text = ''.join(decrypt_map.get(char, char) for char in ciphertext)
    
    return decrypted_text

# Chargement des textes
cipher_text = load_text('chemin/vers/texte_chiffre.txt')
reference_text = load_text('chemin/vers/texte_reference.txt')

# Analyse des fréquences
cipher_char_freq, cipher_bigram_freq = frequency_analysis(cipher_text)
reference_char_freq, reference_bigram_freq = frequency_analysis(reference_text)

# Création des cartes de décryptage
char_decrypt_map = create_decryption_map(cipher_char_freq, reference_char_freq)
bigram_decrypt_map = create_decryption_map(cipher_bigram_freq, reference_bigram_freq)

# Déchiffrement du texte
decrypted_text = decrypt_text(cipher_text, {**char_decrypt_map, **bigram_decrypt_map})



print("Texte déchiffré:", decrypted_text)
