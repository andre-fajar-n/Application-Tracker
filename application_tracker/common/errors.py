import json


def getErrorMessageFromForm(errorStr):
    errorJson = json.loads(errorStr.errors.as_json(True))
    errorMsg = ""
    for key in errorJson:
        errorVal = errorJson[key]
        for k, v in enumerate(errorVal):
            errorMsg = v['message']
            break
        break
    return errorMsg
