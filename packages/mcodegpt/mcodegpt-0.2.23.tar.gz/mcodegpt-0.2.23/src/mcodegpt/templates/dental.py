""" ================================= 1. Do not touch ================================= """

"""GO-CAM template."""
from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional

from pydantic.v1 import BaseModel as BaseModel
from pydantic.v1 import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
):
    pass


""" ================================= 1. Throw away ================================= """

# class GeneLocationEnum(str, Enum):
#     dummy = "dummy"


# class GOCellComponentType(str, Enum):
#     dummy = "dummy"


# class CellType(str, Enum):
#     dummy = "dummy"

""" ================================= 2. Replace ================================= """

class DentalAnnotations(ConfiguredBaseModel):
    people: Optional[List[str]] = Field(
        default_factory= list, description="""the name of a person"""
    )


    gingival_diseases_non_dental_biofilm_induced: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival diseases non dental biofilm induced?"""
    )
    

    periodontitis_stage_iv: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Periodontitis Stage IV?"""
    )
    

    gingival_diseases__inflammatory_and_immune_conditions: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival diseases  Inflammatory and immune conditions?"""
    )
    

    necrotizing_periodontal_diseases: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Necrotizing Periodontal Diseases?"""
    )
    

    traumatic_occlusal_forces: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Traumatic Occlusal forces?"""
    )
    

    gingival_diseases_non_plaque_induced: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival Diseases Non Plaque induced?"""
    )
    

    gingival_diseases__neoplasms: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival diseases Neoplasms?"""
    )
    

    periodontitis_stage_iii: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Periodontitis Stage III?"""
    )
    

    chronic_periodontitis: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Chronic Periodontitis?"""
    )
    

    periodontal_health: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Periodontal Health?"""
    )
    

    other_periodontal_or_endo_lesion: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Other Periodontal or Endo Lesion?"""
    )
    

    gingival_diseases_traumatic_lesions: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival diseases Traumatic lesions?"""
    )
    

    peri_implant_diseases_and_conditions: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Peri Implant Diseases and Conditions?"""
    )
    

    prosth_or_tooth_related_modify_or_predispose_gingivitis_or_perio: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Prosth or tooth related modify or predispose gingivitis or perio?"""
    )
    

    periodontitis_stage_i: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Periodontitis Stage I?"""
    )
    

    mucogingival_deformities: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Mucogingival Deformities?"""
    )
    

    periodontitis_stage_ii: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Periodontitis Stage II?"""
    )
    

    gingival_diseases__specific_infections: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival diseases  Specific infections?"""
    )
    

    gingival_diseases_plaque_induced: Optional[List[str]] = Field(
        default_factory= list, description="""Does the patient have Gingival Diseases Plaque induced?"""
    )
    

    people_gingival_diseases_non_dental_biofilm_induced_interaction: Optional[List[People_Gingival_Diseases_Non_Dental_Biofilm_Induced_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival diseases non dental biofilm induced, separated by semi-colons"""
    )
    

    people_periodontitis_stage_iv_interaction: Optional[List[People_Periodontitis_Stage_Iv_Interaction]] = Field(
        default_factory=list, description="""list of what people has Periodontitis Stage IV, separated by semi-colons"""
    )
    

    people_gingival_diseases__inflammatory_and_immune_conditions_interaction: Optional[List[People_Gingival_Diseases__Inflammatory_And_Immune_Conditions_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival diseases  Inflammatory and immune conditions, separated by semi-colons"""
    )
    

    people_necrotizing_periodontal_diseases_interaction: Optional[List[People_Necrotizing_Periodontal_Diseases_Interaction]] = Field(
        default_factory=list, description="""list of what people has Necrotizing Periodontal Diseases, separated by semi-colons"""
    )
    

    people_traumatic_occlusal_forces_interaction: Optional[List[People_Traumatic_Occlusal_Forces_Interaction]] = Field(
        default_factory=list, description="""list of what people has Traumatic Occlusal forces, separated by semi-colons"""
    )
    

    people_gingival_diseases_non_plaque_induced_interaction: Optional[List[People_Gingival_Diseases_Non_Plaque_Induced_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival Diseases Non Plaque induced, separated by semi-colons"""
    )
    

    people_gingival_diseases__neoplasms_interaction: Optional[List[People_Gingival_Diseases__Neoplasms_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival diseases  Neoplasms, separated by semi-colons"""
    )
    

    people_periodontitis_stage_iii_interaction: Optional[List[People_Periodontitis_Stage_Iii_Interaction]] = Field(
        default_factory=list, description="""list of what people has Periodontitis Stage III, separated by semi-colons"""
    )
    

    people_chronic_periodontitis_interaction: Optional[List[People_Chronic_Periodontitis_Interaction]] = Field(
        default_factory=list, description="""list of what people has Chronic Periodontitis, separated by semi-colons"""
    )
    

    people_periodontal_health_interaction: Optional[List[People_Periodontal_Health_Interaction]] = Field(
        default_factory=list, description="""list of what people has Periodontal Health, separated by semi-colons"""
    )
    

    people_other_periodontal_or_endo_lesion_interaction: Optional[List[People_Other_Periodontal_Or_Endo_Lesion_Interaction]] = Field(
        default_factory=list, description="""list of what people has Other Periodontal or Endo Lesion, separated by semi-colons"""
    )
    

    people_gingival_diseases_traumatic_lesions_interaction: Optional[List[People_Gingival_Diseases_Traumatic_Lesions_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival diseases Traumatic lesions, separated by semi-colons"""
    )
    

    people_peri_implant_diseases_and_conditions_interaction: Optional[List[People_Peri_Implant_Diseases_And_Conditions_Interaction]] = Field(
        default_factory=list, description="""list of what people has Peri Implant Diseases and Conditions, separated by semi-colons"""
    )
    

    people_prosth_or_tooth_related_modify_or_predispose_gingivitis_or_perio_interaction: Optional[List[People_Prosth_Or_Tooth_Related_Modify_Or_Predispose_Gingivitis_Or_Perio_Interaction]] = Field(
        default_factory=list, description="""list of what people has Prosth or tooth related modify or predispose gingivitis or perio, separated by semi-colons"""
    )
    people_periodontitis_stage_i_interaction: Optional[List[People_Periodontitis_Stage_I_Interaction]] = Field(
        default_factory=list, description="""list of what people has Periodontitis Stage I, separated by semi-colons"""
    )
    

    people_mucogingival_deformities_interaction: Optional[List[People_Mucogingival_Deformities_Interaction]] = Field(
        default_factory=list, description="""list of what people has Mucogingival Deformities, separated by semi-colons"""
    )
    

    people_periodontitis_stage_ii_interaction: Optional[List[People_Periodontitis_Stage_Ii_Interaction]] = Field(
        default_factory=list, description="""list of what people has Periodontitis Stage II, separated by semi-colons"""
    )
    

    people_gingival_diseases__specific_infections_interaction: Optional[List[People_Gingival_Diseases__Specific_Infections_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival diseases  Specific infections, separated by semi-colons"""
    )
    

    people_gingival_diseases_plaque_induced_interaction: Optional[List[People_Gingival_Diseases_Plaque_Induced_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gingival Diseases Plaque induced, separated by semi-colons"""
    )

""" ============================================ 3. Do NOT Touch ============================ """
class ExtractionResult(ConfiguredBaseModel):
    """A result of extracting knowledge on text."""

    input_id: Optional[str] = Field(None)
    input_title: Optional[str] = Field(None)
    input_text: Optional[str] = Field(None)
    raw_completion_output: Optional[str] = Field(None)
    prompt: Optional[str] = Field(None)
    extracted_object: Optional[Any] = Field(
        None, description="""The complex objects extracted from the text"""
    )
    named_entities: Optional[List[Any]] = Field(
        default_factory=list, description="""Named entities extracted from the text"""
    )


class NamedEntity(ConfiguredBaseModel):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")

""" ============================================ 4. Replace ============================ """
class Gingival_Diseases_Non_Dental_Biofilm_Induced(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival diseases non dental biofilm induced?""")
    

class Periodontitis_Stage_Iv(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Periodontitis Stage IV?""")
    

class Gingival_Diseases__Inflammatory_And_Immune_Conditions(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival diseases  Inflammatory and immune conditions?""")
    

class Necrotizing_Periodontal_Diseases(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Necrotizing Periodontal Diseases?""")
    

class Traumatic_Occlusal_Forces(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Traumatic Occlusal forces?""")
    

class Gingival_Diseases_Non_Plaque_Induced(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival Diseases Non Plaque induced?""")
    

class Gingival_Diseases__Neoplasms(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival diseases Neoplasms?""")
    

class Periodontitis_Stage_Iii(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Periodontitis Stage III?""")
    

class Chronic_Periodontitis(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Chronic Periodontitis?""")
    

class Periodontal_Health(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Periodontal Health?""")
    

class Other_Periodontal_Or_Endo_Lesion(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Other Periodontal or Endo Lesion?""")
    

class Gingival_Diseases_Traumatic_Lesions(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival diseases Traumatic lesions?""")
    

class Peri_Implant_Diseases_And_Conditions(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Peri Implant Diseases and Conditions?""")
    

class Prosth_Or_Tooth_Related_Modify_Or_Predispose_Gingivitis_Or_Perio(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Prosth or tooth related modify or predispose gingivitis or perio?""")
    

class Periodontitis_Stage_I(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Periodontitis Stage I?""")
    

class Mucogingival_Deformities(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Mucogingival Deformities?""")
    

class Periodontitis_Stage_Ii(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Periodontitis Stage II?""")
    

class Gingival_Diseases__Specific_Infections(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival diseases  Specific infections?""")
    

class Gingival_Diseases_Plaque_Induced(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Does the patient have Gingival Diseases Plaque induced?""")
    

""" ============================================ 5. Do NOT Touch ============================ """

class CompoundExpression(ConfiguredBaseModel):
    pass


""" ============================================ 6. Replace ============================ """
class People_Gingival_Diseases_Non_Dental_Biofilm_Induced_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases_non_dental_biofilm_induced: Optional[str] = Field(None)
    

class People_Periodontitis_Stage_Iv_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    periodontitis_stage_iv: Optional[str] = Field(None)
    

class People_Gingival_Diseases__Inflammatory_And_Immune_Conditions_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases__inflammatory_and_immune_conditions: Optional[str] = Field(None)
    

class People_Necrotizing_Periodontal_Diseases_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    necrotizing_periodontal_diseases: Optional[str] = Field(None)
    

class People_Traumatic_Occlusal_Forces_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    traumatic_occlusal_forces: Optional[str] = Field(None)
    

class People_Gingival_Diseases_Non_Plaque_Induced_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases_non_plaque_induced: Optional[str] = Field(None)
    

class People_Gingival_Diseases__Neoplasms_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases__neoplasms: Optional[str] = Field(None)
    

class People_Periodontitis_Stage_Iii_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    periodontitis_stage_iii: Optional[str] = Field(None)
    

class People_Chronic_Periodontitis_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    chronic_periodontitis: Optional[str] = Field(None)
    

class People_Periodontal_Health_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    periodontal_health: Optional[str] = Field(None)
    

class People_Other_Periodontal_Or_Endo_Lesion_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    other_periodontal_or_endo_lesion: Optional[str] = Field(None)
    

class People_Gingival_Diseases_Traumatic_Lesions_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases_traumatic_lesions: Optional[str] = Field(None)
    

class People_Peri_Implant_Diseases_And_Conditions_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    peri_implant_diseases_and_conditions: Optional[str] = Field(None)
    

class People_Prosth_Or_Tooth_Related_Modify_Or_Predispose_Gingivitis_Or_Perio_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    prosth_or_tooth_related_modify_or_predispose_gingivitis_or_perio: Optional[str] = Field(None)
    

class People_Periodontitis_Stage_I_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    periodontitis_stage_i: Optional[str] = Field(None)
    

class People_Mucogingival_Deformities_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    mucogingival_deformities: Optional[str] = Field(None)
    

class People_Periodontitis_Stage_Ii_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    periodontitis_stage_ii: Optional[str] = Field(None)
    

class People_Gingival_Diseases__Specific_Infections_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases__specific_infections: Optional[str] = Field(None)
    

class People_Gingival_Diseases_Plaque_Induced_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gingival_diseases_plaque_induced: Optional[str] = Field(None)


""" ============================================ 7. Do NOT Touch ============================ """
        
class Triple(CompoundExpression):
    """Abstract parent for Relation Extraction tasks."""

    subject: Optional[str] = Field(None)
    predicate: Optional[str] = Field(None)
    object: Optional[str] = Field(None)
    qualifier: Optional[str] = Field(
        None, description="""A qualifier for the statements, e.g. \"NOT\" for negation"""
    )
    subject_qualifier: Optional[str] = Field(
        None,
        description="""An optional qualifier or modifier for the subject of the statement,\
            e.g. \"high dose\" or \"intravenously administered\"""",
    )
    object_qualifier: Optional[str] = Field(
        None,
        description="""An optional qualifier or modifier for the object of the statement,\
            e.g. \"severe\" or \"with additional complications\"""",
    )


class TextWithTriples(ConfiguredBaseModel):
    publication: Optional[Publication] = Field(None)
    triples: Optional[List[Triple]] = Field(default_factory=list)


class RelationshipType(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")


class Publication(ConfiguredBaseModel):
    id: Optional[str] = Field(None, description="""The publication identifier""")
    title: Optional[str] = Field(None, description="""The title of the publication""")
    abstract: Optional[str] = Field(None, description="""The abstract of the publication""")
    combined_text: Optional[str] = Field(None)
    full_text: Optional[str] = Field(None, description="""The full text of the publication""")


class AnnotatorResult(ConfiguredBaseModel):
    subject_text: Optional[str] = Field(None)
    object_id: Optional[str] = Field(None)
    object_text: Optional[str] = Field(None)


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
""" ============================================ 6. Replace ============================ """
# GoCamAnnotations.update_forward_refs() 
""" ============================================ Do NOT touch ============================ """
ExtractionResult.update_forward_refs()
NamedEntity.update_forward_refs()
""" ============================================ 6. Replace ============================ """
# Gene.update_forward_refs()
# Pathway.update_forward_refs()
# CellularProcess.update_forward_refs()
# MolecularActivity.update_forward_refs()
# GeneLocation.update_forward_refs()
# Organism.update_forward_refs()
# Molecule.update_forward_refs()
""" ============================================ Do NOT touch ============================ """
CompoundExpression.update_forward_refs()
""" ============================================ 6. Replace ============================ """
# GeneOrganismRelationship.update_forward_refs()
# GeneMolecularActivityRelationship.update_forward_refs()
# GeneMolecularActivityRelationship2.update_forward_refs()
# GeneSubcellularLocalizationRelationship.update_forward_refs()
# GeneGeneInteraction.update_forward_refs()
""" ============================================ Do NOT touch ============================ """
Triple.update_forward_refs()
TextWithTriples.update_forward_refs()
RelationshipType.update_forward_refs()
Publication.update_forward_refs()
AnnotatorResult.update_forward_refs()


DentalAnnotations.update_forward_refs()

Gingival_Diseases_Non_Dental_Biofilm_Induced.update_forward_refs()
    

Periodontitis_Stage_Iv.update_forward_refs()
    

Gingival_Diseases__Inflammatory_And_Immune_Conditions.update_forward_refs()
    

Necrotizing_Periodontal_Diseases.update_forward_refs()
    

Traumatic_Occlusal_Forces.update_forward_refs()
    

Gingival_Diseases_Non_Plaque_Induced.update_forward_refs()
    

Gingival_Diseases__Neoplasms.update_forward_refs()
    

Periodontitis_Stage_Iii.update_forward_refs()
    

Chronic_Periodontitis.update_forward_refs()
    

Periodontal_Health.update_forward_refs()
    

Other_Periodontal_Or_Endo_Lesion.update_forward_refs()
    

Gingival_Diseases_Traumatic_Lesions.update_forward_refs()
    

Peri_Implant_Diseases_And_Conditions.update_forward_refs()
    

Prosth_Or_Tooth_Related_Modify_Or_Predispose_Gingivitis_Or_Perio.update_forward_refs()
    

Periodontitis_Stage_I.update_forward_refs()
    

Mucogingival_Deformities.update_forward_refs()
    

Periodontitis_Stage_Ii.update_forward_refs()
    

Gingival_Diseases__Specific_Infections.update_forward_refs()
    

Gingival_Diseases_Plaque_Induced.update_forward_refs()
    

People_Gingival_Diseases_Non_Dental_Biofilm_Induced_Interaction.update_forward_refs()
    

People_Periodontitis_Stage_Iv_Interaction.update_forward_refs()
    

People_Gingival_Diseases__Inflammatory_And_Immune_Conditions_Interaction.update_forward_refs()
    

People_Necrotizing_Periodontal_Diseases_Interaction.update_forward_refs()
    

People_Traumatic_Occlusal_Forces_Interaction.update_forward_refs()
    

People_Gingival_Diseases_Non_Plaque_Induced_Interaction.update_forward_refs()
    

People_Gingival_Diseases__Neoplasms_Interaction.update_forward_refs()
    

People_Periodontitis_Stage_Iii_Interaction.update_forward_refs()
    

People_Chronic_Periodontitis_Interaction.update_forward_refs()
    

People_Periodontal_Health_Interaction.update_forward_refs()
    

People_Other_Periodontal_Or_Endo_Lesion_Interaction.update_forward_refs()
    

People_Gingival_Diseases_Traumatic_Lesions_Interaction.update_forward_refs()
    

People_Peri_Implant_Diseases_And_Conditions_Interaction.update_forward_refs()
    

People_Prosth_Or_Tooth_Related_Modify_Or_Predispose_Gingivitis_Or_Perio_Interaction.update_forward_refs()
    

People_Periodontitis_Stage_I_Interaction.update_forward_refs()
    

People_Mucogingival_Deformities_Interaction.update_forward_refs()
    

People_Periodontitis_Stage_Ii_Interaction.update_forward_refs()
    

People_Gingival_Diseases__Specific_Infections_Interaction.update_forward_refs()
    

People_Gingival_Diseases_Plaque_Induced_Interaction.update_forward_refs()