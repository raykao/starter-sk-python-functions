import azure.functions as func
import json
import logging
import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.search_engine import BingConnector
from semantic_kernel.core_skills import WebSearchEngineSkill

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="generate_market_research")
async def generate_market_research(req: func.HttpRequest) -> func.HttpResponse:
    location = req.params.get('location')
    property_type = req.params.get('property_type')

    if not location:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            location = req_body.get('location')
    if not location:
        return func.HttpResponse(
            "Please pass a `location` on the query string or in the request body",
            status_code=400
        )
    
    if not property_type:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            property_type = req_body.get('property_type')
    if not property_type:
        return func.HttpResponse(
            "Please pass a `property_type` on the query string or in the request body",
            status_code=400
        )

    aoai_deployment_name = os.environ["AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"]
    aoai_endpoint = os.environ["AZURE_OPEN_AI__ENDPOINT"]
    aoai_api_key = os.environ["AZURE_OPEN_AI__API_KEY"]

    kernel = sk.Kernel()
    # Add Azure OpenAI for chat completions
    kernel.add_chat_service(
        "chat_completion",
        AzureChatCompletion(
            deployment_name = aoai_deployment_name,
            endpoint = aoai_endpoint,
            api_key = aoai_api_key,
        ),
    )

    market_research_questions =	[
        f"Write a sentence about {location} and {property_type} leasing",
        f"How to get to and from {location}",
        f"Popular neighborhoods in {location} for {property_type} leasing",
        f"Write a short paragraph about {location}",
        f"Are {property_type} rents going to increase in {location}?",
        f"Write a short meta description for {property_type} for lease in {location} without quotation marks",
        f"Write an optimised meta description for {property_type} for lease in {location} without quotation marks",
	]

    history = ""
    context = sk.ContextVariables()
    answers = []
    market_research = ""

    plugins_directory = "./plugins"
    cw_plugins = kernel.import_semantic_skill_from_directory(
        plugins_directory, "CompanyPlugins"
    )


    for question in market_research_questions:
        history = history + "\nUser: " + question

        context["history"] = history
        context["input"] = question
        answer = await kernel.run_async(
            cw_plugins["GenerateMarketResearch"], 
            input_vars = context
        )

        history = history + "\nAssistant: " + answer.result

        answers.append({
            question: answer.result
        })

        market_research += answer.result

    print(json.dumps(answers))

    # return func.HttpResponse(
    #     json.dumps(answers),
    #     mimetype="application/json",
    # )

    return func.HttpResponse(
        market_research,
        mimetype="text/plain",
    )


@app.route(route="generate_landing_page_content")
async def generate_landing_page_content(req: func.HttpRequest) -> func.HttpResponse:
    location = req.params.get('location')
    property_type = req.params.get('property_type')
    market_data = req.params.get('market_data')

    if not location:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            location = req_body.get('location')
    if not location:
        return func.HttpResponse(
            "Please pass a `location` on the query string or in the request body",
            status_code=400
        )
    
    if not property_type:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            property_type = req_body.get('property_type')
    if not property_type:
        return func.HttpResponse(
            "Please pass a `property_type` on the query string or in the request body",
            status_code=400
        )
    
    if not market_data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            market_data = req_body.get('market_data')
    if not market_data:
        return func.HttpResponse(
            "Please pass a `market_data` on the query string or in the request body",
            status_code=400
        )

    aoai_deployment_name = os.environ["AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"]
    aoai_endpoint = os.environ["AZURE_OPEN_AI__ENDPOINT"]
    aoai_api_key = os.environ["AZURE_OPEN_AI__API_KEY"]

    kernel = sk.Kernel()
    # Add Azure OpenAI for chat completions
    kernel.add_chat_service(
        "chat_completion",
        AzureChatCompletion(
            deployment_name = aoai_deployment_name,
            endpoint = aoai_endpoint,
            api_key = aoai_api_key,
        ),
    )

    context = sk.ContextVariables()

    plugins_directory = "./plugins"
    cw_plugins = kernel.import_semantic_skill_from_directory(
        plugins_directory, "CompanyPlugins"
    )

    context["location"] = location
    context["property_type"] = property_type
    context["market_data"] = market_data

    generated_landing_page_content = await kernel.run_async(
        cw_plugins["GenerateLandingPageContent"], 
        input_vars = context
    )

    print(generated_landing_page_content.result)

    return func.HttpResponse(
        json.dumps({
            "content": generated_landing_page_content.result
        }),
        mimetype="application/json",
    )

@app.route(route="extract_keyword_metadata")
async def extract_keyword_metadata(req: func.HttpRequest) -> func.HttpResponse:
    page_content = req.params.get('page_content')
 
    if not page_content:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            page_content = req_body.get('page_content')
    if not page_content:
        return func.HttpResponse(
            "Please pass a `page_content` on the query string or in the request body",
            status_code=400
        )

    aoai_deployment_name = os.environ["AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"]
    aoai_endpoint = os.environ["AZURE_OPEN_AI__ENDPOINT"]
    aoai_api_key = os.environ["AZURE_OPEN_AI__API_KEY"]

    kernel = sk.Kernel()
    # Add Azure OpenAI for chat completions
    kernel.add_chat_service(
        "chat_completion",
        AzureChatCompletion(
            deployment_name = aoai_deployment_name,
            endpoint = aoai_endpoint,
            api_key = aoai_api_key,
        ),
    )

    context = sk.ContextVariables()

    plugins_directory = "./plugins"
    cw_plugins = kernel.import_semantic_skill_from_directory(
        plugins_directory, "CompanyPlugins"
    )

    context["page_content"] = page_content
    
    extracted_keywords = await kernel.run_async(
        cw_plugins["ExtractKeywordMetadata"], 
        input_vars = context
    )

    print(extracted_keywords.result)

    return func.HttpResponse(
        json.dumps(extracted_keywords.result),
        mimetype="application/json",
    )