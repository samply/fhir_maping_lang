import json

import fhirclient.models.elementdefinition
import fhirclient.models.extension
import fhirclient.models.group
import fhirclient.models.meta
import fhirclient.models.structuredefinition
import fhirclient.models.structuremap
import fhirclient.models.structuremap
import requests


def build_rule_v2(src: str, tgt: str, rule_num: int, attributes: dict):
    rule = fhirclient.models.structuremap.StructureMapGroupRule()
    # Create a nested rule that will be able to create sub resources
    # Maybe try a dictionary with complete FHIRPath and Types?
    # humanName is a datatype same as dateTime, no need to use "create"
    # Good example patient.name.given
    # Has to be a recursive function
    rule.name = src + " to " + tgt
    source = fhirclient.models.structuremap.StructureMapGroupRuleSource()
    target = fhirclient.models.structuremap.StructureMapGroupRuleTarget()
    if rule_num == 0:
        source.context = "source"
        target.context = "target"
    else:
        source.context = "src_" + str(rule_num - 1)
        target.context = "tgt_" + str(rule_num - 1)
    source.element = src
    source.variable = "src_" + str(rule_num)
    target.element = tgt
    target.contextType = "variable"
    target.transform = "copy"
    target.parameter = [
        fhirclient.models.structuremap.StructureMapGroupRuleTargetParameter(
            {"valueId": source.variable})]
    rule.source = [source]
    rule.target = [target]
    return [rule]


def build_rule(src: str, tgt: str, rule_num: int, resources: dict) -> []:
    """Build a transform rule from any XML attribute or element into FHIR"""
    rule = fhirclient.models.structuremap.StructureMapGroupRule()
    shared_vars = []
    tmp_tgt = tgt
    if "." in src:
        rule.name = "rule_" + str(rule_num)
        rule.source = [fhirclient.models.structuremap.StructureMapGroupRuleSource()]
        if rule_num == 1:
            rule.source[0].context = src.split('.')[0]
        else:
            rule.source[0].context = "source_" + str(rule_num - 1)
        rule.source[0].element = src.split('.')[1]
        rule.source[0].variable = "source_" + str(rule_num)
        shared_vars.append(rule.source[0].variable)
        shared_vars.append('tgt')
        if len(tgt.split('.')) == 3 and len(src.split('.')) == 2 and "Patient." + tgt.split('.')[1] in resources.keys():
            rule.target = [fhirclient.models.structuremap.StructureMapGroupRuleTarget(),
                           fhirclient.models.structuremap.StructureMapGroupRuleTarget()]
            rule.target[0].context = tgt.split('.')[0]
            rule.target[0].element = tgt.split('.')[1]
            rule.target[0].variable = "tgt_" + str(rule_num)
            rule.target[0].transform = 'create'
            rule.target[0].parameter = [
                fhirclient.models.structuremap.StructureMapGroupRuleTargetParameter(
                    {"valueString": resources.get("Patient." + tgt.split('.')[1])})]
            rule.target[1].context = "tgt_" + str(rule_num)
            rule.target[1].element = tgt.split('.')[2]
            rule.target[1].transform = 'copy'
            rule.target[1].parameter = [
                fhirclient.models.structuremap.StructureMapGroupRuleTargetParameter(
                    {"valueId": rule.source[0].variable})]
            return [rule]
        elif len(tgt.split('.')) > 3:
            rule.target = [fhirclient.models.structuremap.StructureMapGroupRuleTarget()]
            rule.target[0].context = tgt.split('.')[0]
            rule.target[0].element = tgt.split('.')[1]
            rule.target[0].variable = "tgt_" + str(rule_num)
            shared_vars.append(rule.target[0].variable)
            tmp_tgt = '.'.join(tgt.split('.')[1:])
        if len(src.split('.')) == 2 and len(tgt.split('.')) == 2:
            rule.target = [fhirclient.models.structuremap.StructureMapGroupRuleTarget(),
                           fhirclient.models.structuremap.StructureMapGroupRuleTarget()]
            rule.target[0].context = tgt.split('.')[0]
            rule.target[0].element = tgt.split('.')[1]
            rule.target[0].variable = "tgt_" + str(rule_num)
            rule.target[0].transform = 'copy'
            rule.target[0].parameter = [
                fhirclient.models.structuremap.StructureMapGroupRuleTargetParameter(
                    {"valueId": rule.source[0].variable})]
            return [rule]
        if len(src.split('.')) != 2:
            rule_name = "rule_" + str(rule_num + 1)
            rule.dependent = [fhirclient.models.structuremap.StructureMapGroupRuleDependent({
                "name": rule_name,
                "variable": shared_vars
            })]
            rule.rule = build_rule('.'.join(src.split('.')[1:]), tmp_tgt, rule_num + 1, resources)
        return [rule]


def get_sub_attributes(parent: str, res_type: str):
    r = requests.get("https://www.hl7.org/fhir/" + res_type + ".profile.json?_summary=true")
    if r.status_code == 200:
        js = json.loads(r.text)
        for el in js['snapshot']['element']:
            if 'type' in el:
                for codes in el['type']:
                    if codes['code'][0].isupper():
                        print(codes['code'])
                        get_sub_attributes(el['id'], codes['code'])


def get_all_attributes(target_profile="https://fhir.simplifier.net/bbmri.de/StructureDefinition/Patient?_summary=true"):
    atts = {}
    r = requests.get(target_profile)
    js = json.loads(r.text)
    for el in js['snapshot']['element']:
        if 'type' in el:
            for codes in el['type']:
                atts[el['id']] = codes['code']
                # if codes['code'][0].isupper():
                # get_sub_attributes(atts[el['id']], codes['code'])
    print(json.dumps(atts, indent=4))
    return atts


def build_map(output_file: str, source_attribute="id", target_attribute="id",
              target_profile="https://fhir.bbmri.de/StructureDefinition/Patient"):
    structure_map = fhirclient.models.structuremap.StructureMap()
    structure_map.id = "test_1"
    structure_map.name = "Test"
    structure_map.title = "Test"
    structure_map.status = "draft"
    structure_map.url = "http://hl7.org/fhir/StructureMap/idk"
    structure_map.structure = [fhirclient.models.structuremap.StructureMapStructure(),
                               fhirclient.models.structuremap.StructureMapStructure()]
    structure_map.structure[0].url = "http://hl7.org/fhir/StructureMap/idk"
    structure_map.structure[0].mode = "source"
    structure_map.structure[0].alias = "src"
    structure_map.structure[1].url = target_profile
    structure_map.structure[1].mode = "target"
    structure_map.structure[1].alias = "tgt"
    # for att in js:
    #     attributes[att['name']] = att['type']
    # attributes = get_all_attributes(attributes)
    # with open('resource.json', 'w') as outf:
    #     json.dump(attributes, outf, indent=4)
    structure_map.group = [fhirclient.models.structuremap.StructureMapGroup()]
    structure_map.group[0].name = "map_test"
    structure_map.group[0].typeMode = 'types'
    structure_map.group[0].input = [fhirclient.models.structuremap.StructureMapGroupInput(),
                                    fhirclient.models.structuremap.StructureMapGroupInput()]
    structure_map.group[0].input[0].mode = 'source'
    structure_map.group[0].input[0].name = 'source'
    structure_map.group[0].input[0].type = 'SourceTest'
    structure_map.group[0].input[1].mode = 'target'
    structure_map.group[0].input[1].name = 'target'
    structure_map.group[0].input[1].type = 'TargetTest'
    f = open('resource.json')
    js = json.load(f)
    attributes: dict = js[0]
    f.close()
    structure_map.group[0].rule = build_rule_v2(source_attribute, target_attribute, 0, attributes)
    print(json.dumps(structure_map.as_json(), indent=4))
    with open(output_file, 'w') as f:
        json_string = json.dumps(structure_map.as_json(), indent=4)
        f.write(json_string)
    f.close()
