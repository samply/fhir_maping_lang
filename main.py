import parser.xml_parser
import struc_def.generator
from struc_map.generator import build_map, get_all_attributes

if __name__ == "__main__":
    test_xml = 'TestData/LF1.xml'
    struc_def_output = 'TestData/structure_definition.json'
    struc_map_output = 'TestData/structure_map.json'
    struc_def.generator.build_structure_definition(parser.xml_parser.loadMetaData(test_xml), struc_def_output)
    target_resource = input("Enter target resource profile: ")
    get_all_attributes(target_resource)
    source_attribute = input("Enter source attribute: ")
    target_attribute = input("Enter target attribute: ")
    build_map(struc_map_output, source_attribute, target_attribute)
