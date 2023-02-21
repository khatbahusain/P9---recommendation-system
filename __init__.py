import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    if name:
        return func.HttpResponse(f"Helloooooooo world mais sans hahaha, {name}!")
    else:
        return func.HttpResponse("Please provide a name parameter in the query string.", status_code=400)
