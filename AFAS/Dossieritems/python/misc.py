import json

def HubbiData2JsonObject(headers, row):
    output = {}
    for i in range(len(headers)):
        val = int(row[i]) if type(row[i]).__name__ == 'Int64' else row[i]
        output[headers[i]] = val
    output = json.dumps(output)
    return output


def IsEven(num):
    return True if int(num) % 2 == 0 else False