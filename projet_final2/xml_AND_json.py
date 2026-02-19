import json
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_json(filepath):
    if filepath.stat().st_size == 0:
        raise ValueError("Fichier JSON vide")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        raise ValueError("Données JSON vides")

    return data


def parse_xml(filepath):
    if filepath.stat().st_size == 0:
        raise ValueError("Fichier XML vide")

    tree = ET.parse(filepath)
    root = tree.getroot()

    data = []

    for elem in root:
        item = {}
        for child in elem:
            if child.text is None:
                raise ValueError("Clé XML manquante")
            item[child.tag] = child.text
        data.append(item)

    if not data:
        raise ValueError("Données XML vides")

    return data


def main():
    json_file = Path("data.json")
    xml_file = Path("data.xml")

    try:
        if json_file.exists():
            print("Format détecté : JSON")
            data = parse_json(json_file)

        elif xml_file.exists():
            print("Format détecté : XML")
            data = parse_xml(xml_file)

        else:
            raise FileNotFoundError("Aucun fichier data.json ou data.xml trouvé")

        print("Données Python standardisées :")
        print(data)

    except FileNotFoundError as e:
        print("Erreur :", e)
    except json.JSONDecodeError:
        print("Erreur : JSON invalide")
    except ET.ParseError:
        print("Erreur : XML mal formé")
    except ValueError as e:
        print("Erreur :", e)
    except Exception as e:
        print("Erreur inattendue :", e)


if __name__ == "__main__":
    main()
