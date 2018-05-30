from textanalyticsfunction import AnalyticsFunction


if __name__== "__main__":
    print("HKHR")
    af = AnalyticsFunction()
    text_data = af.read_data()
    #print(text_data)

    entities = af.get_entities()
    print(entities)
    print("\n\n")

    pos_entity_relations = af.get_generic_relations_extraction()
    for relation in pos_entity_relations:
        print(relation)
    print("\n\n")

    concepts = af.text_concept_summary()
    print(concepts)