import json

def HubbiData2JsonObject(headers, row, add_result_as_header=None):
    # VOEG TOE: import json
    # We kijken naar de lengte van de RIJ om te bepalen hoeveel data er is.
    # Dit voorkomt dat een eerder toegevoegde header de boel verstoort.
    current_row_length = len(row)
    output_dict = {}
    for i in range(current_row_length):
        val = int(row[i]) if type(row[i]).__name__ == 'Int64' else row[i]
        output_dict[headers[i]] = val
    json_string = json.dumps(output_dict)
    if add_result_as_header is not None:
        # Check of de header al bestaat om dubbele headers te voorkomen
        if add_result_as_header not in headers:
            headers.append(add_result_as_header)
        # Voeg de JSON string toe aan de huidige rij
        row.append(json_string)
    return json_string


def IsEven(num):
    return True if int(num) % 2 == 0 else False


'''
Functies ValueFromLabel en CastValue werken samen

    ValueFromLabel fungeert als een "zoekmachine" die kolommen vindt, zelfs als HubBI ze hernoemt (zoals Dossieritem1, Dossieritem2) 
    bij het koppelen van meerdere bronnen. Het identificeert automatisch de gevulde bronkolom.

    CastValue dient als een veiligheidsfilter dat de gevonden data direct converteert naar het gewenste type (int, date, decimal, etc.). 
    Het voorkomt script-crashes door ongeldige invoer of lege velden (None) op te vangen met logische standaardwaarden.

Samen resultaat: Je kunt gegevens opvragen op basis van de functionele naam, zonder je druk te maken over de exacte kolomindex, bronvolgorde of datatypen.

'''
from datetime import datetime
from decimal import Decimal

def ValueFromLabel(rij, label, forceAsType = None):
    hdrs = GetHeaders()
    
    # 1. Directe match check
    if label in hdrs:
        val = GetColumnValue(rij, label)
        return CastValue(val, forceAsType)
            
    # 2. Zoeken naar genummerde varianten (bijv. Dossieritem1, Dossieritem2)
    for hdr in hdrs:
        if hdr.startswith(label):
            suffix = hdr[len(label):] # Haal het gedeelte na de label tekst op
            
            # Controleer of suffix leeg is of alleen uit cijfers bestaat
            if suffix == "" or suffix.isdigit():
                val = GetColumnValue(rij, hdr)
                
                # Als de waarde gevuld is (niet None en niet een lege string), geef deze terug
                if val is not None and str(val).strip() != "":
                    return CastValue(val, forceAsType)

    # 3. Fallback als er niets gevonden is
    return CastValue(None, forceAsType)


def CastValue(val, forceAsType=None):
    """Hulpfunctie om de meest voorkomende datatypes consistent af te handelen"""
    
    # Als de waarde al None is en we geen specifiek type forceren, direct teruggeven
    if forceAsType is None:
        return val

    try:
        if forceAsType == 'int':
            return int(val) if val not in (None, '') else 0
            
        elif forceAsType == 'float':
            return float(val) if val not in (None, '') else 0.0
            
        elif forceAsType == 'decimal':
            # Veilig voor financiële berekeningen
            return Decimal(str(val)) if val not in (None, '') else Decimal('0.00')
            
        elif forceAsType == 'str':
            return str(val) if val is not None else ''
            
        elif forceAsType == 'bool':
            # Handelt 'True', 1, '1', 'yes' etc. af
            if isinstance(val, bool): return val
            return str(val).lower() in ('true', '1', 't', 'y', 'yes')
            
        elif forceAsType == 'date' or forceAsType == 'datetime':
            if isinstance(val, datetime): return val
            if val in (None, ''): return None
            # Past de string-parser aan op basis van het formaat in HubBI (vaak ISO)
            return datetime.fromisoformat(str(val))
            
    except (ValueError, TypeError):
        # Fallback als conversie mislukt (bijv. tekst in een int veld)
        return val 

    return val
