from pathlib import Path
import pandas as pd
import re
from datetime import datetime


def parse_csv(
    input_file: Path,
    output_file: Path,
) -> None:
    
    if not input_file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {input_file}")

    # LECTURE DU FICHIER
    df = pd.read_csv(
        input_file,
        sep=";",
        encoding="utf-8-sig",
        dtype=str,
        na_values=["", "NaN", "N/A", "NA", "nan", "--", "inf"],
        keep_default_na=True,
    )

    # RENOMMAGE DES COLONNES
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]
    
    cols_to_keep = [col for col in df.columns if col and not col.startswith('unnamed')]
    df = df[cols_to_keep]

    # NETTOYAGE DES LIGNES VIDES
    df = df.replace(r'^\s*$', None, regex=True)
    df = df.dropna(how='all')
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    
    if 'nom' in df.columns:
        df = df[df['nom'].notna() & (df['nom'] != '')]
    
    # CONVERSION DE LA COLONNE AGE
    if 'age' in df.columns:
        def clean_age(age_str):
            if pd.isna(age_str) or age_str in ['', 'NaN', 'N/A', 'NA']:
                return None
            age_clean = re.sub(r'[^\d-]', '', str(age_str))
            if age_clean == '' or age_clean == '-':
                return None
            try:
                age = int(age_clean)
                if age < 0 or age > 120:
                    return None
                return age
            except:
                return None
        
        df['age'] = df['age'].apply(clean_age)
    
    # CONVERSION DE LA COLONNE MONTANT
    if 'montant_total_eur' in df.columns:
        def clean_montant(montant_str):
            if pd.isna(montant_str) or montant_str in ['', 'NaN', 'N/A', 'NA', 'inf']:
                return None
            try:
                montant_clean = str(montant_str).strip()
                montant_clean = re.sub(r'[€\s]', '', montant_clean)
                
                if ',' in montant_clean and '.' in montant_clean:
                    pos_virgule = montant_clean.index(',')
                    pos_point = montant_clean.index('.')
                    if pos_point < pos_virgule:
                        montant_clean = montant_clean.replace('.', '').replace(',', '.')
                    else:
                        montant_clean = montant_clean.replace(',', '')
                elif ',' in montant_clean:
                    montant_clean = montant_clean.replace(',', '.')
                
                montant = float(montant_clean)
                if montant < 0 or montant > 10000000:
                    return None
                return round(montant, 2)
            except:
                return None
        
        df['montant_total_eur'] = df['montant_total_eur'].apply(clean_montant)
    
    # CONVERSION DE LA COLONNE ACTIF
    if 'actif' in df.columns:
        def clean_actif(val):
            if pd.isna(val):
                return None
            val_lower = str(val).strip().lower()
            if val_lower in ['oui', 'yes', '1', 'true', 'vrai']:
                return True
            elif val_lower in ['non', 'no', '0', 'false', 'faux']:
                return False
            return None
        
        df['actif'] = df['actif'].apply(clean_actif)
    
    # CONVERSION DE LA COLONNE NEWSLETTER
    if 'newsletter_ok' in df.columns:
        def clean_newsletter(val):
            if pd.isna(val):
                return None
            val_clean = str(val).strip().replace(' ', '').upper()
            if val_clean in ['TRUE', 'T', 'YES', 'OUI', '1']:
                return True
            elif val_clean in ['FALSE', 'F', 'NO', 'NON', '0']:
                return False
            return None
        
        df['newsletter_ok'] = df['newsletter_ok'].apply(clean_newsletter)
    
    # CONVERSION DE LA COLONNE DATE INSCRIPTION
    if 'date_inscription' in df.columns:
        def clean_date(date_str):
            if pd.isna(date_str) or date_str == '':
                return None
            try:
                for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
                    try:
                        dt = datetime.strptime(str(date_str).strip(), fmt)
                        if 1900 <= dt.year <= 2030:
                            return dt.strftime('%Y-%m-%d')
                    except:
                        continue
                return None
            except:
                return None
        
        df['date_inscription'] = df['date_inscription'].apply(clean_date)
    
    # CONVERSION DE LA COLONNE DERNIERE CONNEXION
    if 'derniere_connexion' in df.columns:
        def clean_datetime(dt_str):
            if pd.isna(dt_str) or dt_str == '':
                return None
            try:
                dt_str = str(dt_str).strip()
                for fmt in ['%d/%m/%Y %H:%M', '%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M:%S']:
                    try:
                        dt = datetime.strptime(dt_str, fmt)
                        return dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        continue
                return None
            except:
                return None
        
        df['derniere_connexion'] = df['derniere_connexion'].apply(clean_datetime)
    
    # SUPPRESSION DES DOUBLONS
    df = df.drop_duplicates()
    
    # SAUVEGARDE
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"✓ Fichier nettoyé sauvegardé: {output_file}")
    print(f"  Lignes d'origine: {pd.read_csv(input_file, sep=';', encoding='utf-8-sig').shape[0]}")
    print(f"  Lignes après nettoyage: {df.shape[0]}")
    print(f"  Lignes supprimées: {pd.read_csv(input_file, sep=';', encoding='utf-8-sig').shape[0] - df.shape[0]}")


if __name__ == "__main__":
    parse_csv(
        input_file=Path("/mnt/user-data/uploads/data.csv"),
        output_file=Path("/home/claude/output/clean_data.csv"),
    )