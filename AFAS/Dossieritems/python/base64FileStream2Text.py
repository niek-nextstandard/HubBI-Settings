import base64

def safe_b64decode(data: str) -> bytes:
    data = data.strip().replace("\n", "").replace(" ", "")
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return base64.b64decode(data)

headers = [
    'Dossieritem',
    'Toelichting'
]

newData = []

for rij in Bron:
    b64_data = rij.Base64
    if b64_data is not None:
        decoded_bytes = safe_b64decode(b64_data)

        # --- VEILIG DECODEN ---
        try:
            decoded_string = decoded_bytes.decode("utf-8")
        except Exception:
            try:
                decoded_string = decoded_bytes.decode("cp1252")
            except Exception as err:
                # beide decodes mislukken → bestand is niet leesbaar
                Toelichting = (
                    f"Het bestand {rij.Bestandsnaam} bevat onleesbare tekens:{chr(10)}{err}"
                )
                newData.append([rij.Dossieritem, Toelichting])
                continue
        # ------------------------------------

        # Check of het een webformulier is
        if 'webform' not in decoded_string:
            Toelichting = (
                f"Het bestand {rij.Bestandsnaam} is geen webformulier van wijzerbelonen.nl."
            )
        else:
            Toelichting = decoded_string

        newRij = [rij.Dossieritem, Toelichting]
        newData.append(newRij)

SetHeaders(headers)
SetData(newData)
