import graphviz


def get_property_string(value):
    # join list elements
    if isinstance(value, list):
        return ", ".join(value)

    return str(value)


def build_graph_from_json(scheme, extension=".pdf", show_labels=True,
                          show_node_props=False, show_edge_props=False) -> graphviz.Digraph:
    dot = graphviz.Digraph(format=extension[1:])

    concepts = scheme['concepts']
    relations = scheme['relations']

    for concept in concepts:
        # decode some special characters for html-like graphviz-labeling
        concept_name = (concept['properties']['name'].replace('&', '&amp;')
                                                     .replace('<', '&lt;')
                                                     .replace('>', '&gt;')
                                                     .replace('_', ' '))
        content = '<<TABLE CELLBORDER="0" BORDER="0">'

        if show_labels:
            # add label of concept to node-content
            concept_type = concept['type'].replace('_', ' ')
            content += f'<TR><TD COLSPAN="2" CELLPADDING="0" CELLSPACING="0"><I>{concept_type}</I></TD></TR>'

        # add name of concept to node-content
        content += f'<TR><TD COLSPAN="2" CELLPADDING="0" CELLSPACING="0"><B>{concept_name}</B></TD></TR>'

        if show_node_props:
            properties = concept['properties']

            if len(properties.keys()) > 1:  # more properties than "name"
                # add a horizontal rule
                content += "<HR/>"

                # add additional properties to node content
                for key in properties.keys():
                    if key == "name":
                        continue

                    content += f'<TR><TD ALIGN="left">{key}:</TD><TD>{get_property_string(properties[key])}</TD></TR>'

        content += '</TABLE>>'

        # add concept-node to graph
        dot.node("co_" + concept['concept_id'], content, fontname="Arial", shape="box")

    concept_ids = list(map(lambda x: x['concept_id'], concepts))
    edges = list()

    for rel in relations:
        # discard edges mentioning non-existing concepts
        if rel["from_concept"] in concept_ids and rel["to_concept"] in concept_ids:
            source = "co_" + rel["from_concept"]
            target = "co_" + rel["to_concept"]
            predicate = rel["predicate"].replace('_', ' ')

            # pred_id (id of predicate-node) initially only involves source-concept of relation
            pred_id = "pred_" + rel["from_concept"] + "_" + predicate.replace(' ', '_')

            # add predicate to node content
            content = f'<<TABLE CELLBORDER="0" BORDER="0">'
            content += f'<TR><TD COLSPAN="2" CELLPADDING="0" CELLSPACING="0"><I>{predicate}</I></TD></TR>'

            if show_edge_props:
                # extend pred_id by target concept of relation (preventing that relations with the same predicate
                # but different properties are merged)
                pred_id += "_" + rel["to_concept"]
                properties = rel['properties']

                if len(properties.keys()) >= 1:
                    # add a horizontal rule
                    content += "<HR/>"

                    # add additional properties to node content
                    for key in properties.keys():
                        content += f'<TR><TD ALIGN="left">{key}:</TD><TD>{get_property_string(properties[key])}</TD></TR>'

                content += '</TABLE>>'

                # introduce new predicate-node for every relation and use pred_id to identify this relation
                dot.node(pred_id, content, fontname="Arial", shape="plaintext")
                dot.edge(source, pred_id, arrowhead="none")
                dot.edge(pred_id, target)

            else:
                content += '</TABLE>>'

                # introduce new predicate-node for every unseen relation (relations with the same predicate and
                # source-concept are merged)
                dot.node(pred_id, content, fontname="Arial", shape="plaintext")

                if (source, pred_id) not in edges:
                    dot.edge(source, pred_id, arrowhead="none")
                    edges.append((source, pred_id))

                if (pred_id, target) not in edges:
                    dot.edge(pred_id, target)
                    edges.append((pred_id, target))

    # add a disclaimer
    dot.attr(fontname="Arial")
    dot.attr(fontsize='10')
    dot.attr(fontcolor='grey')
    dot.attr(label="Concept map by concept-mapper • This concept map is AI-generated. Be aware that it likely "
                   "contains errors and/or false information.")

    return dot
