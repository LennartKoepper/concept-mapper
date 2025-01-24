def get_default_example() -> str:
    return """Example: 
    Data: Alice is a lawyer and 25 years old and Bob is her roommate since 2001. Bob works as a 
    journalist. Alice owns the webpage www.alice.com and Bob owns the webpage www.bob.com.
    
    Output: {
        "concepts": [
            {
                "concept_id": "alice",
                "type": "Person",
                "properties": {
                    "name": "Alice",
                    "age": 25,
                    "occupation": "lawyer"
                }
            },
            {
                "concept_id": "bob",
                "type": "Person",
                "properties": {
                    "name": "Bob",
                    "occupation": "journalist"
                }
            },
            {
                "concept_id": "alice.com",
                "type": "Webpage",
                "properties": {
                    "name": "www.alice.com",
                    "url": "www.alice.com"
                }
            },
            {
                "concept_id": "bob.com",
                "type": "Webpage",
                "properties": {
                    "name": "www.bob.com",
                    "url": "www.bob.com"
                }
            }
        ],
        "relations": [
            {
                "from_concept": "alice",
                "predicate": "is_roommate_of",
                "to_concept": "bob",
                "properties": {
                    "start": 2021
                }
            },
            {
                "from_concept": "bob",
                "predicate": "is_roommate_of",
                "to_concept": "alice",
                "properties": {
                    "start": 2021
                }
            },
            {
                "from_concept": "alice",
                "predicate": "owns",
                "to_concept": "alice.com",
                "properties": {}
            },
            {
                "from_concept": "bob",
                "predicate": "owns",
                "to_concept": "bob.com",
                "properties": {}
            }
        ]
    }"""


def get_mathematical_example():
    return r"""Example: 
    Data: A complex number is an expression of the form a + bi, where a and b are real numbers, 
    and i is an abstract symbol, the so-called imaginary unit, introduced to solve equations like 
    {\displaystyle x^{2}=-1} and defined solely by the property that its square is −1: 
    {\displaystyle i^{2}=-1.}. For example, 2 + 3i is a complex number. For a complex number a + bi, the real number 
    a is called its real part, and the real number b (not the complex number bi) is its imaginary part. The real 
    part of a complex number z is denoted Re(z), the imaginary part is Im(z). Addition: Two complex numbers {\displaystyle 
    a=x+yi} and {\displaystyle b=u+vi} are added by separately adding their real and imaginary parts. That is to say: 
    {\displaystyle a+b=(x+yi)+(u+vi)=(x+u)+(y+v)i.} Similarly, subtraction can be performed as {\displaystyle a-b=(
    x+yi)-(u+vi)=(x-u)+(y-v)i.} The complex conjugate of the complex number z = a + bi is defined as
    {\displaystyle {\overline {z}}=a-bi.}
    
    Output: {
        "concepts": [
            {
                "concept_id": "complex_number",
                "type": "expression",
                "properties": {
                    "name": "Complex Number $z$",
                    "formula": "$z = a + bi$"
                }
            },
            {
                "concept_id": "real_number_a",
                "type": "real number",
                "properties": {
                    "name": "Real Part $a$",
                    "formula": "$Re(z) = a$"
                }
            },
            {
                "concept_id": "real_number_b",
                "type": "real number",
                "properties": {
                    "name": "Imaginary Part $b$",
                    "formula": "$Im(z) = b$"
                }
            },
            {
                "concept_id": "imaginary_unit",
                "type": "abstract symbol",
                "properties": {
                    "name": "Imaginary Unit $i$",
                    "formula": "$i^{2}=-1$"
                }
            },
            {
                "concept_id": "addition",
                "type": "operation",
                "properties": {
                    "name": "Addition",
                    "formula": "$a=x+yi$\n$b=u+vi$$a+b=(x+yi)+(u+vi)=(x+u)+(y+v)i.$"
                }
            },
            {
                "concept_id": "subtraction",
                "type": "operation",
                "properties": {
                    "name": "Subtraction",
                    "formula": "$a=x+yi$\n$b=u+vi$\n$a-b=(x+yi)-(u+vi)=(x-u)+(y-v)i$"
                }
            },
            {
                "concept_id": "complex_conjugate",
                "type": "expression",
                "properties": {
                    "name": "Complex Conjugate ${\\overline {z}}$",
                    "formula": "${\\overline {z}}=a-bi$"
                }
            }
        ],
        "relations": [
            {
                "from_concept": "complex_number",
                "predicate": "has ",
                "to_concept": "real_number_a",
                "properties": {}
            },
            {
                "from_concept": "complex_number",
                "predicate": "has",
                "to_concept": "real_number_b",
                "properties": {}
            },
            {
                "from_concept": "complex_number",
                "predicate": "introduces",
                "to_concept": "imaginary_unit",
                "properties": {}
            },
            {
                "from_concept": "complex_number",
                "predicate": "added with",
                "to_concept": "addition",
                "properties": {}
            },
            {
                "from_concept": "complex_number",
                "predicate": "subtracted with",
                "to_concept": "subtraction",
                "properties": {}
            },
            {
                "from_concept": "complex_number",
                "predicate": "can be conjugated to",
                "to_concept": "complex_conjugate",
                "properties": {}
            },
            {
                "from_concept": "complex_conjugate",
                "predicate": "can be conjugated to",
                "to_concept": "complex_number",
                "properties": {}
            }
        ]
    }"""
