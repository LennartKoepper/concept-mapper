from typing import Tuple, Dict, List

from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Concept(BaseModel):
    concept_id: str = Field(description="the identifier of the concept")
    type: str = Field(description="a generic type to which the concept can be assigned")
    properties: Dict[str, str] = Field(description='a dictionary of additional properties, must at least contain a '
                                                   '"name"-property, that describes the concept')


class Relation(BaseModel):
    from_concept: str = Field(description="the identifier of the relations subject (a concept)")
    to_concept: str = Field(description="the identifier of the relations object (a concept)")
    predicate: str = Field(description="a generic predicative expression describing the relation between the concepts")
    properties: Dict[str, str] = Field(description='a dictionary of additional properties')


class ConceptMap(BaseModel):
    concepts: List[Concept] = Field(description="a list of all found concepts")
    relations: List[Relation] = Field(description="a list of all found relations")


def get_default_extraction_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=ConceptMap)

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are a data scientist and expert in concept mapping working for a company that is building graph 
                databases, knowledge graphs and concept maps. Your task is to examine a previously generated JSON, that 
                summarizes the  subject and importance of a text focussing on an arbitrary topic, and convert it into a 
                structured (also JSON) collection of concepts and relations that will be transformed into a concept 
                map. As an orientation the summary includes a list of the main concepts and a rather unstructured 
                representation of important relations. Furthermore, the summary provides a focussing_question that 
                specifies the problem or issue the concept map should help to resolve. Rely on the information provided 
                in the JSON-summary! 
                
                Your output must contain:
                - A "concepts" set, where each element is a JSON object with:
                  * "concept_id": A UNIQUE identifier for the concept.
                  * "type": A generic type/category for the concept.
                  * "properties": A JSON object containing AT LEAST a "name" property. Add other suitable and 
                  concise (no descriptions or sentences) properties with respect to the concept.
                - A "relations" array, where each element is a JSON object with:
                  * "from_concept": The concept id of the relations subject/source concept. Listed in the "concepts" 
                  set.
                  * "to_concept": The concept id of the relations object/target concept. Listed in the "concepts" set.
                  * "predicate": A SHORT predicative expression describing the relation. Should not contain more than 
                  three words!
                  * "properties": A JSON object containing suitable and concise (no descriptions or sentences) 
                  properties that clarify the relation between the two mentioned concepts.
                
                Important details:
                - Each relation described in the 'relations' field of the input JSON should result in one or more  
                corresponding relations in the output JSON. If there are multiple equally directed relations 
                between two concepts that are similar in content, unite them into a single and short relation!
                - Of course the "concepts" and "relations" fields of the input JSON should be used as a point of 
                reference. However, as an expert you should be critical and therefore check the given relations against 
                the context provided by the "title", "summary" and "importance" fields. Further check, if 
                important relations between found concepts remain unmentioned. If so, add them! 
                - For bidirectional relationships, provide a separate relation object for each of the two directions!
                - It is very important that "from_concept" and "to_concept" within a relation are listed as concepts
                with a matching "concept_id". If you can't pair both concept ids of a relation with concepts listed in 
                the "concepts" set, don´t add it!
                - Prioritize representing information as concepts and relations over storing it in properties. Use 
                properties only for additional information, that is hard to represent through concepts and relations!
                
                Remember, your task is to build a clear concept map, so all found concepts and relations 
                must result in a single connected graph, where each concept-node is somehow connected to each other, 
                either through direct relations or indirectly via related concepts!
                
                Example for expected output format:
                {{
                  "concepts": [
                    {{
                      "concept_id": "concept_a",
                      "type": "entity",
                      "properties": {{
                        "name": "Concept A"
                      }}
                    }},
                    {{
                      "concept_id": "concept_b",
                      "type": "idea",
                      "properties": {{
                        "name": "Concept B"
                      }}
                    }}
                  ],
                  "relations": [
                    {{
                      "from_concept": "concept_a",
                      "to_concept": "concept_b",
                      "predicate": "supports",
                      "properties": {{}}
                    }},
                    {{
                      "from_concept": "concept_b",
                      "to_concept": "concept_a",
                      "predicate": "builds upon",
                      "properties": {{}}
                    }}
                  ]
                }}"""
            ),
            (
                "human",
                "{input}"
            )
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt, parser
