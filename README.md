# fhir-universal

java -jar validator_cli.jar patient.xml -transform http://hl7.org/fhir/StructureMap/idk -ig test.map -version 4.0.1 -ig
sd.xml -output idk.xml

curl https://fhir.simplifier.net/bbmri.de/StructureDefinition/Specimen?_elements=snapshot | jq '.snapshot.element[] |
.id, .definition'

Current status: It can generate a StructureMap using the python FHIR library, for some reason the XML needs to have a
namespace (TODO)
Next step: Dynamic Generation using CLI
java -jar validator_cli.jar BBM211219230002-000079.XML -transform http://hl7.org/fhir/StructureMap/idk -ig de.bbmri.fhir
-ig 4map.json -version 4.0.1 -ig 2sd.json -output test.json -log log.txt

curl https://www.hl7.org/fhir/humanname.profile.json?_summary=true | jq '.snapshot.element[] | {name: .id,type: .type[]
?.code}' | jq --slurp '.'

curl https://fhir.simplifier.net/bbmri.de/StructureDefinition/Specimen?_summary=true | jq '.snapshot.element[] | .id,
.type[]?.code'

 java -jar validator_cli.jar TestData/LF1.xml -transform http://hl7.org/fhir/StructureMap/idk -ig de.bbmri.fhir -ig Tes
tData/structure_map.json -version 4.0.1 -ig TestData/structure_definition.json -output TestData/output.json

WORKING: src.id to patient.id
