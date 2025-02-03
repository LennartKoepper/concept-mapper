
from typing import List, Tuple

from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class SummaryTest(BaseModel):
    title: str               = Field(description="a title for the summary")
    summary: str             = Field(description="short summary of the text")
    importance: str          = Field(description="short discussion why the subject matters")
    focusing_question: str   = Field(description="the dynamic focusing question, that clearly specifies the problem or"
                                                 "issue the concept map should help to resolve")
    main_concepts: List[str] = Field(description="a list containing the most important concepts in the text in order "
                                                 "of importance")
    relations: List[str]     = Field(description="a list containing elements that describe how each concept in the "
                                                 "MAIN CONCEPTS list relates to each of the other concepts in that "
                                                 "list")


def get_summary_test_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=SummaryTest)


    # Prompt by jorgearango, see https://github.com/jorgearango/llmapper.
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are a panel of expert readers, Bob, Laurence, and Laura. You will each examine a {text_type}.  
                Your task is to produce a list of the most important concepts about the {text_type} and a list of 
                relations between those concepts. This concepts and relationships are later used to build a concept map. 
                In the context of concept mapping, there is a difference between dynamic and static focusing questions.
                
                You will do this as a panel. At each step of the process, you will 
                review and critique each other's work. Point out and correct any possible errors. As experts, you must 
                decide why this subject matters, and focus on presenting concepts that highlight its importance.
                
                The {text_type} will be the sole source of information for your outline. Treat everything in the 
                {text_type} as factual. Do not include any details that don't appear there. 
                
                Methodology:
                1. Start by reading the {text_type}.
                2. Write a dynamic focusing question about the {text_type} that explores its relevance to humanity in 
                general.
                3. Make a list of all concepts described in the {text_type} that help answer this dynamic question.
                    - A concept is a common or proper noun
                    - A concept cannot include more than one noun (it cannot include lists of nouns)
                4. Focus only on the concepts that are most relevant to what this {text_type} is about and why it 
                matters — how they help answer the dynamic focusing question.
                5. The first concept in the list is the main subject of the {text_type}
                6. Take the first concept in the list and consider its relationship to every other concept in the list
                7. Do the same thing for the second concept, and then every remaining concept in the list.
                
                Expected Output:
                The expected output is structured as json and contains the following fields: title, summary, importance, 
                focusing_question, main_concepts, relations.
                
                - title: a title for the summary. The title is what the {text_type} is about.
                - summary: Combine all of your understanding of the subject being summarized into a single, 
                20-word sentence. Focus only on the subject.
                - importance: Speculate about why this subject matters and write a single 20-word sentence that explains 
                it.
                - focusing_question: the dynamic focusing question.
                - main_concepts: a list containing the {nr_concepts} MOST IMPORTANT concepts in the {text_type} in order 
                of importance. A concept is a common or proper noun that is a key part of the {text_type}. The most 
                important concepts are those that help explain what this is and why it matters. Only include one 
                concept per list element. Don't include descriptions of each concept; only the concepts themselves. 
                Include concepts that explain why this subject matters. The first concept in the list is the main 
                subject of the article.
                - relations: a list containing elements that describe how each concept in the MAIN CONCEPTS list relates 
                to each of the other concepts in that list. ONLY USE CONCEPTS FROM THE CONCEPTS LIST. Do not introduce 
                new concepts. Add each relation to a list in the format "noun verb noun." DO NOT WRITE SENTENCES, only 
                noun-verb-noun. Only include one object and subject in each element. Consider how this concept relates 
                to the main subject. Include relations that help explain why this subject matters.

                This is the format for the RELATIONSHIPS section:
                ["Bytedance owns TikTok", "Bytedance owns Douyin", "TikTok expanded globally"]

                Only include ONE SUBJECT, ONE OBJECT, and ONE PREDICATE per element. Do not include adjectives or 
                adverbs. Do not include lists in elements.

                Include as many relations as necessary to represent ALL the concepts in the concepts list. Include no 
                fewer than {nr_concepts} relationships in this list. DO NOT INCLUDE CONCEPTS THAT AREN'T PRESENT IN 
                THE CONCEPTS LIST ABOVE.
                
                Further rules:
                - Do not mention the {text_type} itself
                - Do not mention references
                - Do not mention the authors or the institution/organization they are working for
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


class Summary(BaseModel):
    title: str               = Field(description="a good fitting title for this summary")
    summary: str             = Field(description="a summary of the input text")
    importance: str          = Field(description="a short discussion why the subject matters")
    focusing_question: str   = Field(description="the dynamic focusing question, that clearly specifies the problem or "
                                                 "issue the concept map should help to resolve")
    main_concepts: List[str] = Field(description="a set containing the most important concepts in the text in order of "
                                                 "importance")
    relations: List[str]     = Field(description="a list containing elements that describe how each concept in the "
                                                 "MAIN CONCEPTS set relates to each of the other concepts in that list")


def get_default_summary_prompt() -> Tuple[ChatPromptTemplate, BaseOutputParser]:
    parser = JsonOutputParser(pydantic_object=Summary)

    # Prompt inspired by jorgearangos llmapper-project, see https://github.com/jorgearango/llmapper.
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are an expert reader, that helps creating summaries of {text_type}. Your task is to examine 
                a given text focussing on an arbitrary topic, extract its essence, and produce a JSON-formatted summary 
                that will serve as a basis for the creation of a concept map. This concept map should depict the main 
                ideas of the given text in the form of concepts and relations. As an expert, you must decide why the 
                given subject matters, and focus on presenting concepts and relation that highlight its importance. 
                
                The {text_type} will be the main source of information for your outline. Treat every information in the 
                text as factual.  
                
                Follow these instructions carefully and strictly:
                - The output MUST be valid JSON.
                - The output MUST contain the following fields and no others:
                    * "title": A good fitting title for the summary.
                    * "summary": A concise summary of the input text, capturing the most important ideas mentioned in 
                    the {text_type}.
                    * "importance": A short discussion why this subject matters.
                    * "focusing_question": A dynamic focusing question, that clearly specifies the problem or issue the 
                    concept map should help to resolve.
                    * "main_concepts": A set containing up to {nr_concepts} of the MOST IMPORTANT concepts of 
                    the {text_type} in order of importance. Concepts can represent real entities (e.g. persons, 
                    organizations, etc.) or more abstract concepts (e.g. technologies, ideas, approaches, roadmaps, 
                    theories, etc.) usually  mentioned as a common or proper noun that is a key element of the 
                    {text_type}. The most important concepts are those that help explain what the subject of the text is 
                    about and why it matters — concepts that help answering the focusing question. 
                    * "relations": A list containing sentences that describe how each concept in the MAIN CONCEPTS set 
                    relates to each of the other concepts in that set. Each sentence MUST feature two distinct 
                    concepts, except relations, that describe how concepts are related to themselves. It is important 
                    that you ONLY USE CONCEPTS FROM THE CONCEPTS SET. Do not introduce new concepts. Only include one 
                    object and one subject in each sentence. For bidirectional relations provide one relation for each 
                    of the two directions. Include relations that help explain why the subject of the {text_type}
                    matters. You should at least include enough relations to represent ALL the concepts in the concept
                    set. However, more relations with a large variance of associated concepts will result in better 
                    concept map, so focus on finding as many meaningful relations as possible!
                - Further restrictions:        
                    * Do not mention given references.
                    * Do not mention the authors of the {text_type} nor the institution they are working for.
                    * Be aware that {nr_concepts} is an upper bound for the number of concepts! If you believe that 
                    there are less than {nr_concepts} concepts which are relevant for understanding the subject, DONT 
                    introduce new or add irrelevant concepts to the main_concepts!

                For example:
                {{
                  "title": "...",
                  "summary": "...",
                  "importance": "...",
                  "focusing_question": "...",
                  "main_concepts": ["ConceptA", "ConceptB", "ConceptC"],
                  "relations": [
                    "ConceptA supports ConceptB by ...",
                    "ConceptB contrasts with ConceptC in ...",
                    "ConceptC started ConceptA on..."
                  ]
                }}
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
