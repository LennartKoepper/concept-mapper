#! /usr/bin/env python
"""Main-Script for hosting a FastAPI application providing the cm-backend-api for the Concept-Mapper-Application. Start
with command `fastapi dev concept_mapper_api.py`.
"""
import json
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pypdf import PdfReader

from prompts.concept_extraction import get_default_extraction_prompt
from prompts.summarization import get_default_summary_prompt
from prompts.examples import get_mathematical_example
from utils import create_timestamp_str, check_if_txt, check_model, check_extension, check_context, get_mediatype
from llm.models import OpenAiLLM, MistralAiLLM
from prompts.one_shot_prompts import get_mathematical_prompt
from evaluate.graph_evaluator import GraphEvaluator
from visualize.graphviz_builder import build_graph_from_json
from scrape.simple_text_scraper import scrape_visible_text

app = FastAPI()

# load environment variables from .env-file in parent directory
load_dotenv(".env")


class Options(BaseModel):
    """Interface for settable options"""
    filename: str
    extension: str
    context: str
    model: str
    temperature: float
    num_nodes: int
    show_node_props: bool
    show_edge_props: bool
    show_labels: bool


class Payload(BaseModel):
    """Interface for JSON-Payloads"""
    payload: str
    options: Options


@app.get("/api")
def read_root():
    return {"online": True}


@app.post("/api/text")
async def post_text(payload: Payload) -> FileResponse:
    input_text = payload.payload
    options = payload.options

    return create_concept_map(input_text, options)


@app.post("/api/file-upload")
async def post_file(file: UploadFile = File(...), options: str = Form(...)) -> FileResponse:
    input_text = ""

    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)

        # extract plain text from pdf
        for page in reader.pages:
            input_text += page.extract_text()

    elif check_if_txt(file.filename):
        # decode bytestream (file) to text
        bytestream = file.file.read()
        input_text = bytestream.decode("utf-8")

    else:
        # throw error if file is neither a .pdf, .txt, .md, or .tex file
        raise HTTPException(status_code=422, detail="File Extension not supported. Either provide a .pdf, .txt, "
                                                    ".md or .tex file!")

    options = Options(**json.loads(options))

    return create_concept_map(input_text, options)


@app.post("/api/url")
async def post_url(payload: Payload):
    # scrape text from website
    input_text = scrape_visible_text(payload.payload)
    options = payload.options

    return create_concept_map(input_text, options)


def create_concept_map(text: str, options) -> FileResponse:
    # set fallback values for options
    filename =    options.filename    if options.filename                   else f"CoMap"
    extension =   options.extension   if check_extension(options.extension) else ".pdf"
    context =     options.context     if check_context(options.context)     else "default"
    model =       options.model       if check_model(options.model)         else "gpt-4o"
    temperature = max(0.0, min(1.0, options.temperature))
    num_nodes =   max(2, min(32, options.num_nodes))
    show_node_props = options.show_node_props
    show_edge_props = options.show_edge_props
    show_labels = options.show_labels

    # create timestamp and output paths
    stamp = create_timestamp_str()

    cm_out_dir = os.getenv("CM_OUT_DIR")
    output_path = f"{cm_out_dir}/{filename}_{stamp}"
    output_gv_path = output_path + f"/{filename}.gv"

    # create output directory
    os.makedirs(output_path, exist_ok=True)

    # initialize LLM
    if "mistral" in model:
        mistral_key = os.getenv("MISTRAL_API_KEY")

        llm = MistralAiLLM(
            mistral_api_key=mistral_key,
            model_name=model,
            temp=temperature
        )

        # TODO handle large inputs (maybe no need for that, since Mistral models use sliding window attention)
    else:
        open_ai_key = os.getenv("OPENAI_API_KEY")

        llm = OpenAiLLM(
            openai_api_key=open_ai_key,
            model_name=model,
            temp=temperature
        )

        # TODO handle large inputs


    # extract concept map scheme from text
    try:
        if context == "mathematical":
            # mathematical context preset is currently still using the one-shot-prompt-approach with a provided example

            prompt, parser = get_mathematical_prompt()

            # generate scheme of concept map directly from the input text
            json_scheme = llm.generate(prompt, parser=parser, params={
                "input": text,
                "example": get_mathematical_example()
            })
        else:
            # other context presets currently use summary-based concept mapping (a summary prompt and an extraction prompt)

            context_dict = {                 # associate context presets with keywords giving some context to the model
                "default": "text",
                "scientific": "scientific text",
                "wiki-text": "wiki text"
            }

            summary_prompt, summary_parser = get_default_summary_prompt()
            extraction_prompt, extraction_parser = get_default_extraction_prompt()

            # first generate a summary-object from the input text
            summary_obj = llm.generate(summary_prompt, parser=summary_parser, params={
                "input": text,
                "text_type": context_dict[context],
                "nr_concepts": num_nodes
            })

            # save summary
            json_summary = json.dumps(summary_obj)

            with open(output_path + f"/{filename}_summary.json", "w") as f:
                f.write(json_summary)

            # then generate the scheme of the concept map from the given summary
            json_scheme = llm.generate(extraction_prompt, parser=extraction_parser, params={
                "input": json_summary,
            })

    except httpx.HTTPStatusError as err:
        if err.response.status_code == 401:
            raise HTTPException(status_code=401, detail=f"Unauthorized: Provided API key invalid for model {model}!")

    # save scheme (extended by options)
    json_scheme["options"] = vars(options)

    with open(output_path + f"/{filename}_scheme.json", "w") as f:
        f.write(json.dumps(json_scheme))

    # evaluate graph
    graph_evaluator = GraphEvaluator(json_scheme)

    # save evaluation
    with open(output_path + f"/{filename}_eval.json", "w") as f:
        f.write(json.dumps(graph_evaluator.get_summary()))

    # visualize and save concept map
    dot = build_graph_from_json(json_scheme, extension, show_labels, show_node_props, show_edge_props)
    dot.render(output_gv_path)

    return FileResponse(path=f"{output_gv_path}{extension}", filename=f"{filename}_{stamp}{extension}",
                        media_type=get_mediatype(extension))
