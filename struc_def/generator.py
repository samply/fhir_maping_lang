import collections
import json
import re

import fhirclient.models.elementdefinition
import fhirclient.models.extension
import fhirclient.models.group
import fhirclient.models.meta
import fhirclient.models.structuredefinition
import fhirclient.models.structuremap
import fhirclient.models.structuremap


def build_structure_definition(ordered_dict: collections.OrderedDict, output_file: str):
    """Creates a FHIR structure map for any XML"""
    sm = fhirclient.models.structuremap.StructureMap()
    sm.group = fhirclient.models.group.Group()
    sd = fhirclient.models.structuredefinition.StructureDefinition()
    name = next(iter(ordered_dict.keys())).replace('/', '')
    sd.id = name
    sd.extension = [fhirclient.models.extension.Extension()]
    sd.extension[0].url = "http://hl7.org/fhir/StructureDefinition/elementdefinition-namespace"
    sd.extension[0].valueUri = "http://hl7.org/fhir/idk"
    sd.url = "http://hl7.org/fhir/StructureDefinition/IDK"
    sd.name = name
    sd.kind = "logical"
    sd.abstract = True
    sd.status = "draft"
    sd.type = name
    sd.baseDefinition = "http://hl7.org/fhir/StructureDefinition/Element"
    sd.derivation = "specialization"
    sd.differential = fhirclient.models.structuredefinition.StructureDefinitionDifferential()
    sd.differential.element = []
    # print(ordered_dict.keys())
    for item in ordered_dict.keys():
        element = fhirclient.models.elementdefinition.ElementDefinition()
        parent_path = item.replace('/', '.')
        if parent_path[0] == '.':
            parent_path = parent_path[1:]
        element.path = parent_path
        element.id = parent_path
        sd.differential.element.append(element)
        if len(ordered_dict.get(item)) > 0:
            for att in ordered_dict.get(item):
                element = fhirclient.models.elementdefinition.ElementDefinition()
                path = str(parent_path + '.' + att).replace('/', '.')
                element.id = path
                element.path = path
                element.representation = ["xmlAttr"]
                element.min = 1
                element.max = '1'
                element.type = [fhirclient.models.elementdefinition.ElementDefinitionType()]
                element.type[0].code = 'string'
                sd.differential.element.append(element)
        counter = 0
        for k in ordered_dict.keys():
            if re.search(item, k):
                counter = counter + 1
        if counter == 1:
            element = fhirclient.models.elementdefinition.ElementDefinition()
            element.id = parent_path + '.txt'
            element.path = parent_path + '.txt'
            element.representation = ["xmlText"]
            element.min = 1
            element.max = '1'
            element.type = [fhirclient.models.elementdefinition.ElementDefinitionType()]
            element.type[0].code = 'string'
            sd.differential.element.append(element)
    with open(output_file, 'w') as f:
        json_string = json.dumps(sd.as_json(), indent=4)
        f.write(json_string)
    f.close()
