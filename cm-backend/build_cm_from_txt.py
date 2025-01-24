#! /usr/bin/env python
"""
Simple Console-Script that creates a Concept-Map from a given text file.
Usage: python build_cm_from_txt.py <txt_file_path> <output_dir_path> <output_file_name>
"""
import json
import sys
import os

from dotenv import load_dotenv

from llm.models import OpenAiLLM
from prompts.one_shot_prompts import get_default_prompt
from utils import create_timestamp_str
from visualize.graphviz_builder import build_graph_from_json

# load environment variables from .env-file in parent directory
load_dotenv(".env")

if __name__ == '__main__':
    # check if required arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python build_cm_from_txt.py <txt_file_path> <output_dir_path> <output_file_name>")
        sys.exit(1)

    # check if provided textfile exists
    if not os.path.exists(sys.argv[1]):
        print(f"{sys.argv[1]} does not exist!")
        sys.exit(2)

    # check write permissions
    if not os.access(sys.argv[2], os.W_OK):
        print(f"Permission denied: write {sys.argv[2]}!")
        sys.exit(3)

    # check name for file-extension
    if "." in sys.argv[3]:
        sys.argv[3] = sys.argv[3].split(".")[0]

    # create timestamp
    stamp = create_timestamp_str()

    # provide paths
    input_path = sys.argv[1]
    output_dir = f"{sys.argv[2]}/{sys.argv[3]}_{stamp}"
    output_scheme_path = f"{output_dir}/{sys.argv[3]}_scheme.json"
    output_pdf_path = f"{output_dir}/{sys.argv[3]}.gv"

    # read text
    with open(input_path, "r", encoding="utf8") as f:
        text = f.read()

    # initialize LLM
    open_ai_key = os.getenv("OPENAI_API_KEY")

    llm = OpenAiLLM(
        openai_api_key=open_ai_key
    )

    # TODO handle large inputs

    # extract concept map scheme from text
    prompt, parser = get_default_prompt()
    json_scheme = llm.generate(prompt, params={"input": text}, parser=parser)

    # make output dir
    os.mkdir(output_dir)

    # write scheme
    with open(output_scheme_path, "w") as f:
        f.write(json.dumps(json_scheme))

    # visualize and save concept map
    dot = build_graph_from_json(json_scheme)
    dot.render(output_pdf_path)

    sys.exit(0)
