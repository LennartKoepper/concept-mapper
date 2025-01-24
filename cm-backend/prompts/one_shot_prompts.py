from typing import Dict, List, Tuple

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


def get_default_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=ConceptMap)

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are a data scientist working for a company that is building a concept map. Your task is to 
                extract the main ideas from an unstructured text and convert it into a structured (json) collection 
                of concepts and relations, that will later be transformed into a graph database. Therefore, 
                first provide a set of concepts where each concept has an CONCEPT_ID, TYPE and PROPERTIES attribute. 
                Concepts can either represent real entities (e.g. persons, organizations, etc.) or abstract concepts 
                (e.g. technologies, ideas, approaches, roadmaps, theories, etc.). Further provide a set of relations, 
                where each relation has an FROM_CONCEPT, TO_CONCEPT, PREDICATE, and PROPERTIES attribute. It is very 
                important that FROM_CONCEPT and TO_CONCEPT within a relation are listed as concepts with a matching 
                CONCEPT_ID. So if you can't pair both CONCEPT_IDs of a relation with concepts listed in the concept 
                set, don´t add it! For bidirectional relations provide one relation for each of the two directions. 
                When you found a concept or relation you want to add, create a generic TYPE or PREDICATE for it that 
                describes it. You may use the PROPERTIES to provide further information about concepts and their 
                relations (just if this information is mentioned in the text), but it is important that you 
                prioritize providing concepts and relations over storing information in properties wherever possible. 
                However, for concepts you must at least provide a "name"-property.
                
                Remember, your task is to build a clear concept map, so all found concepts and relations 
                must result in a single connected graph, where each concept-node is somehow connected to each other, 
                either through direct relations or indirectly via related concepts!
                
                {example}
                """
            ),
            (
                "human",
                "{input}"
            )
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt, parser


def get_scientific_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=ConceptMap)

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are a data scientist working at an university as an scientific assistant. One of your jobs is 
                to create concept maps that clearly depict complex topics to the students of your faculty. You will 
                therefore be provided with unstructured text (e.g. a scientific paper, abstract, article, 
                etc.) focussing on a specific scientific topic. Your task is to extract the main ideas from this text 
                and convert them into a structured (json) collection of concepts and relations, that will later be 
                transformed into a concept map. Your approach should be as follows: First provide a set of concepts 
                where each concept has an CONCEPT_ID, TYPE and PROPERTIES attribute. Concepts may be real entities ( 
                e.g. persons, organizations, etc.) but more likely they represent abstract concepts (e.g. 
                technologies, ideas, approaches, roadmaps, theories, etc.) that are presented in the scientific text. 
                Further provide a set of relations, where each relation has an FROM_CONCEPT, TO_CONCEPT, PREDICATE, 
                and PROPERTIES attribute. It is very important that FROM_CONCEPT and TO_CONCEPT within a relation are 
                listed as concepts with a matching CONCEPT_ID. So if you can't pair both CONCEPT_IDs of a relation 
                with concepts listed in the concept set, don´t add it! For bidirectional relations provide one 
                relation for each of the two directions. When you found a concept or relation you want to add, 
                create a generic TYPE or PREDICATE for it that describes it. You may use the PROPERTIES to provide 
                further information about concepts and their relations (just if this information is mentioned in the 
                text), but it is important that you prioritize providing concepts and relations over storing 
                information in properties wherever possible. However, for concepts you must at least provide a 
                "name"-property.
                
                Remember, your task is to build a clear concept map depicting the main ideas of a scientific text, 
                so all found concepts and relations must result in a single connected graph, where each concept-node 
                is somehow connected to each other, either through direct relations or indirectly via related concepts!
                
                Use the following example to understand the expected output scheme. However, do not base your 
                methodology on the provided example, since it doesnt reflect any scientific claims. 
                
                {example}"""
            ),
            (
                "human",
                "{input}"
            )
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt, parser


def get_wiki_text_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=ConceptMap)

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are a data scientist and journalist working for an agency, that creates visualizations for 
                magazines and journals. Your job is to create concept maps that clearly depict different topics to 
                the readers of this journals. You will therefore be provided with unstructured wiki-text (e.g. 
                scraped text from wikipedia) focussing on a specific topic. Your task is to extract the main ideas 
                from this text and convert them into a structured (json) collection of concepts and relations that 
                will later be transformed into a concept map. Your approach should be as follows: First provide a set 
                of concepts where each concept has an CONCEPT_ID, TYPE and PROPERTIES attribute. Concepts can either 
                represent real entities (e.g. persons, organizations, etc.) or abstract concepts (e.g. technologies, 
                ideas, approaches, roadmaps, theories etc.). Further provide a set of relations, where each relation 
                has an FROM_CONCEPT, TO_CONCEPT, PREDICATE, and PROPERTIES attribute. It is very important that 
                FROM_CONCEPT and TO_CONCEPT within a relation are listed as concepts with a matching CONCEPT_ID. So 
                if you can't pair both CONCEPT_IDs of a relation with concepts listed in the concept set, 
                don´t add it! For bidirectional relations provide one relation for each of the two directions. When 
                you found a concept or relation you want to add, create a generic TYPE or PREDICATE for it that 
                describes it. You may use the PROPERTIES to provide further information about concepts and their 
                relations (just if this information is mentioned in the text), but it is important that you 
                prioritize providing concepts and relations over storing information in properties wherever possible. 
                However, for concepts you must at least provide a "name"-property.
                
                Remember, your task is to build a clear concept map depicting the main ideas of a wiki text, 
                so all found concepts and relations must result in a single connected graph, where each concept-node 
                is somehow connected to each other, either through direct relations or indirectly via related concepts!
                
                Use the following example to understand the expected output scheme. However, do not base your 
                methodology on the provided example, since it doesnt reflect a wiki text but rather a simpler toy 
                example.
                
                {example}"""
            ),
            (
                "human",
                "{input}"
            )
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt, parser


def get_mathematical_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=ConceptMap)

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are an mathematician and data scientist working at an university as an scientific assistant 
                within the faculty of mathematics. One of your jobs is to create concept maps that clearly depict 
                complex mathematical relationships to the students of your faculty. You will therefore be provided 
                with unstructured text (e.g. a scientific paper, article, etc) focussing on a specific topic and 
                containing mathematical definitions, statements and proofs. Your task is to extract the main concepts 
                and their relations from the given text and convert them into a structured (json) collection, 
                that will later be transformed into a concept map.
                
                Approach: First provide a set of mathematical concepts where each concept has an CONCEPT_ID, 
                TYPE and PROPERTIES attribute. Concepts may be Numbers, Symbols, Representations, Sets, Ring, 
                Function, and so on. Further provide a set of relations, where each relation has an FROM_CONCEPT, 
                TO_CONCEPT, PREDICATE, and PROPERTIES attribute. It is very important that FROM_CONCEPT and 
                TO_CONCEPT within a relation are listed as concepts with a matching CONCEPT_ID. So if you can't pair 
                both CONCEPT_IDs of a relation with concepts listed in the concept set, don´t add it! For 
                bidirectional relations provide one relation for each of the two directions. When you found a concept 
                or relation you want to add, create a generic TYPE or PREDICATE for it that describes it. For 
                concepts, type examples are "set", "symbol", "number", "representation", "function" and "ring". You 
                may use the PROPERTIES to provide further information about concepts and relations (but just if this 
                information is mentioned in the text), but it is important that you prioritize providing concepts and 
                relations over storing information in properties wherever possible. However, for concepts you must at 
                least provide a "name"-property, which may be a sole symbol were applicable. Furthermore provide a 
                "formula"-property if a concept and relation is related to a formula or definition. Provide all 
                mathematical symbols and formulas as Latex-Code. Other properties may involve adjectives, 
                which describe mathematical properties of objects, e.g. "finite" or "one-to-one".
                
                Remember, your task is to build a clear concept map, so all found concepts and relations 
                must result in a single connected graph, where each concept-node is somehow connected to each other, 
                either through direct relations or indirectly via related concepts!
                
                {example}
                """
            ),
            (
                "human",
                "{input}"
            )
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt, parser
