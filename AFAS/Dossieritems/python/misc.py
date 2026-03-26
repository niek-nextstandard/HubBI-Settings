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