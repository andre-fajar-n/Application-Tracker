import json


def getErrorMessageFromForm(errorStr):
    errorJson = json.loads(errorStr.errors.as_json(True))
    errorMsg = ""
    for key in errorJson:
        errorVal = errorJson[key]
        for _, v in enumerate(errorVal):
            errorMsg = f"({key}) {v['message']}"
            break
        break
    return errorMsg
