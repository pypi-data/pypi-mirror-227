from __future__ import annotations

import re
from abc import ABC
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, field_validator

from .exceptions import RelationshipException, RelMsgErr
from .relationships import RelationshipType, many_to_many, many_to_one, one_to_many
from .types import DataType, SchemaType, all_schemas
from .validators import snake_case_validator


class TemplateModel(BaseModel, ABC):
    """
    Abstract class for classes in main.py.

    Attributes:
        name (str): The name of the model. Name should be snake_case.
        _name_validation (Callable): A validator for the `name` attribute. Names should be snake_case

    Methods:
        __str__(): Returns a string representation of the model.
        __init__(**kwargs): Initializes the model with the given keyword arguments.

    Class Config:
        from pydantic BaseModel
        underscore_attrs_are_private (bool): Whether or not the attributes of the model should be private.
    """

    name: str
    _name_validation = field_validator('name')(snake_case_validator)

    def __str__(self) -> str:
        return f'{type(self).__name__}({super().__str__()})'

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    class ConfigDict:
        underscore_attrs_are_private = True


class Attribute(TemplateModel):
    """
    A class that represents an attribute in a template model.

    Attributes:
        name: str: The name of the model. Name should be snake_case. From TemplateModel
        type: DataType: The type of the attribute.
        default: Any|None: The default value of the attribute. Defaults to None.
        unique: bool: Whether or not the attribute is unique. Defaults to False.
        optional: bool: Whether or not the attribute is optional. Defaults to False.
        validation: list[Callable[[Any],Any]]: A list of validators for the attribute. Defaults to None.
        in_schema: list[SchemaType]: A list of schemas that the attribute is included in. Defaults to all_schemas.

    Methods:
        __init__(name:str, type:DataType, default:Any=None, unique:bool=False,
                 optional: bool = False, validation_rules:list[Callable[[Any],Any]]=[]) -> None:
            Initializes the attribute with the given arguments.
    """

    type: DataType
    default: Any | None = None
    unique: bool = False
    optional: bool = False
    validation: list[Callable[[Any], Any]] = []
    in_schema: list[SchemaType] = all_schemas

    # TODO: add validation for type and default value
    def __init__(
        self,
        name: str,
        type: DataType,
        default: Any = None,
        unique: bool = False,
        optional: bool = False,
        validation_rules: list[Callable[[Any], Any]] = [],
    ) -> None:
        """
        Initializes the attribute with the given arguments.

        Args:
            name: str: The name of the attribute.
            type: DataType: The type of the attribute.
            default: Any: The default value of the attribute. Defaults to None.
            unique: bool: Whether or not the attribute is unique. Defaults to False.
            optional: bool: Whether or not the attribute is optional. Defaults to False.
            validation_rules: list[Callable[[Any],Any]]: List of attribute validators.
        """
        super().__init__(
            name=name,
            type=type,
            default=default,
            unique=unique,
            optional=optional,
            validation_rules=validation_rules,
        )


class Relationship(TemplateModel):
    """
    A class that represents a relationship between two objects.

    Attributes:
        related_object: AppObject: The object that the relationship refers to.
        relationship_type: RelationshipType: The type of the relationship.
        optional: bool: Whether or not the relationship is optional. Defaults to False.

    Methods:
        __init__(name:str, obj:AppObject, type:RelationshipType,
        back_populates_name:Optional[str]=None, optional:bool=False,
        back_populates_optional:bool=False) -> None:
            Initializes the relationship with the given arguments.
    """

    related_object: AppObject
    relationship_type: RelationshipType
    optional: bool = False

    def __init__(
        self,
        name: str,
        obj: AppObject,
        type: RelationshipType,
        optional: bool = False,
    ) -> None:
        """
        Initializes the relationship with the given arguments.

        Args:
            name (str): The name of the relationship.
            obj (AppObject): The object that the relationship refers to.
            type (RelationshipType): The type of the relationship.
            optional (bool): Whether or not the relationship is optional. Defaults to False.
        """
        if type == many_to_many:
            raise RelationshipException(RelMsgErr.MANY_MANY_ERR)
        super().__init__(
            name=name,
            related_object=obj,
            relationship_type=type,
            optional=optional,
        )


class BackpopulatesRelationship(TemplateModel):
    related_object: AppObject
    relationship_type: RelationshipType
    optional: bool = False
    back_populates_name: str
    back_populates_object: AppObject

    def __init__(
        self,
        name: str,
        obj: AppObject,
        type: RelationshipType,
        back_populates_name: str,
        back_populates_object: AppObject,
        optional: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            related_object=obj,
            relationship_type=type,
            optional=optional,
            back_populates_object=back_populates_object,
            back_populates_name=back_populates_name,
        )


def create_relationship(
    name: str,
    obj: AppObject,
    type: RelationshipType,
    back_populates_object: AppObject | None = None,
    back_populates_name: str | None = None,
    optional: bool = False,
) -> Relationship | BackpopulatesRelationship:
    if back_populates_name and back_populates_object:
        return BackpopulatesRelationship(name, obj, type, back_populates_name, back_populates_object, optional)
    return Relationship(name, obj, type)


class AppConfig(BaseModel):
    # TODO:add name validation for these attributes
    route_name: str | None = None
    table_name: str | None = None
    class_name: str | None = None
    plural: str | None = None
    plural_class_name: str | None = None


class AppObject(TemplateModel):
    """
    A class that represents a generic app object.

    Attributes:
        name: str: The name of the model. Name should be snake_case. From TemplateModel
        attributes: list[Attribute]: The list of attributes for the object.
        relationships: list[Relationship]: The list of relationships for the object. Defaults to empty list.
        back_populates_relationships: list[Relationship]: The list of back-populates relationships for the object.
                                                            Defoults to empty list.
        config: AppConfig: The config for the object. Defults to predifined AppConfig.

    Methods:
        __init__(self, name: str, *args: Attribute):
            Initializes the object with the given name and attributes.
        add_relationships(self, *args: Relationship):
            Add the given relationships to the object.
        add_attributes(self, *args: Attribute):
            Add the given attributes to the object.
        is_relationship_self(self, relationship: Relationship):
            Checks if the given relationship is self-referential.
        _class_name(name: str) -> str:
            Converts the given name to a class name.

    Properties:
        _plural(self) -> str:
            Returns the plural form of the object's name.
        plural_class_name(self) -> str:
            Returns the plural class name for the object.
        class_name(self) -> str:
            Returns the class name for the object.
        table_name(self) -> str:
            Returns the table name for the object.
        route_name(self) -> str:
            Returns the route name for the object.
    """

    attributes: list[Attribute]
    relationships: list[Relationship | BackpopulatesRelationship] = []
    back_populates_relationships: list[BackpopulatesRelationship] = []
    config: AppConfig = AppConfig()

    def __init__(
        self,
        name: str,
        *args: Attribute,
        config: AppConfig = AppConfig(),
    ):
        """
        Initialize the object with the given name and attributes.

        Args:
            name: str: The name of the object.
            args: Attribute: A list of attributes for the object.
            relationships: list[Relationship]: A list of relationships for the object. Defaults to empty list.
            config: AppConfig: Configuration class for overwriting calculated names. Defaults to default class.
        """
        super().__init__(name=name, attributes=args, config=config)

    def add_relationship(
        self,
        obj: AppObject,
        type: RelationshipType,
        name: str,
        back_populates_name: str | None = None,
        optional: bool = False,
    ) -> None:
        # TODO: add validation to not have duplicated names in relationships and attributes
        rel = create_relationship(name, obj, type, self, back_populates_name, optional)
        self.relationships.append(rel)
        if isinstance(rel, BackpopulatesRelationship):
            rel.related_object.back_populates_relationships.append(rel)

    def add_attributes(self, *args: Attribute) -> None:
        """
        Add the given attributes to the object.

        Args:
            args: A list of attributes for the object.
        """
        self.attributes += args

    def is_relationship_self(self, rel: Relationship | BackpopulatesRelationship) -> bool:
        """
        Checks if the given relationship is self-referential.

        Args:
            relationship: The relationship to check.

        Returns (bool):
            True if the relationship is self-referential, False otherwise.
        """
        self._check_rel(rel)
        return self.name == rel.related_object.name

    def is_relationship_multiple(self, relationship: Relationship | BackpopulatesRelationship) -> bool:
        check_list: list[str] = [rel.related_object.name for rel in self.relationships]
        if self.is_rel_backref(relationship):
            check_list = [rel.back_populates_object.name for rel in self.back_populates_relationships]

        return check_list.count(relationship.related_object.name) > 1

    def is_relationship_many(self, relationship: Relationship | BackpopulatesRelationship) -> bool:
        self._check_rel(relationship)
        if relationship in self.relationships:
            return relationship.relationship_type in (one_to_many, many_to_many)
        return relationship.relationship_type in (many_to_one, many_to_many)

    def is_rel_backref(self, rel: Relationship | BackpopulatesRelationship) -> bool:
        self._check_rel(rel)
        return rel in self.back_populates_relationships

    def get_rel_name(self, rel: Relationship | BackpopulatesRelationship) -> str:
        if self.is_rel_backref(rel) and isinstance(rel, BackpopulatesRelationship):
            return rel.back_populates_name
        return rel.name

    def get_backpopulates_name(self, rel: BackpopulatesRelationship) -> str:
        if self.is_rel_backref(rel):
            return rel.name
        return rel.back_populates_name

    def get_rel_obj(self, rel: Relationship | BackpopulatesRelationship) -> AppObject:
        if self.is_rel_backref(rel) and isinstance(rel, BackpopulatesRelationship):
            return rel.back_populates_object
        return rel.related_object

    def _check_rel(self, rel: Relationship | BackpopulatesRelationship) -> None:
        if rel not in (self.relationships + self.back_populates_relationships):
            raise AttributeError('Relationship not associated with object!')

    @property
    def all_relationships(self) -> list[Relationship | BackpopulatesRelationship]:
        x: list[Relationship | BackpopulatesRelationship] = list(self.relationships)
        x.extend(self.back_populates_relationships)
        return x

    @staticmethod
    def _class_name(name: str) -> str:
        """
        Converts the given name to a class name.

        Args:
            name: The name to convert.

        Returns:
            The class name.
        Example:
            my_test_name -> MyTestName
        """
        splite_names = name.split('_')
        name = ''.join([split_name.capitalize() for split_name in splite_names])
        return name

    @property
    def _plural(self) -> str:
        """
        Returns the plural form of the object's name.

        Returns:
            The plural form of the object's name.
        """
        if self.config.plural:
            return self.config.plural
        word = self.name
        if re.search('[sxz]$', word) or re.search('[^aeioudgkprt]h$', word):
            return re.sub('$', 'es', word)
        if re.search('[^aeiou]y$', word):
            return re.sub('y$', 'ies', word)
        return word + 's'

    @property
    def plural_class_name(self) -> str:
        """
        Returns the plural class name for the object.

        Returns:
            The plural class name for the object.
        """
        if self.config.plural_class_name:
            return self.config.plural_class_name
        plural = self._plural
        return self._class_name(plural)

    @property
    def class_name(self) -> str:
        """
        Returns the class name for the object.

        Returns:
            The class name for the object.
        """
        if self.config.class_name:
            return self.config.class_name
        return self._class_name(self.name)

    @property
    def table_name(self) -> str:
        """
        Returns the table name for the object.

        Returns:
            The table name for the object.
        """
        if self.config.table_name:
            return self.config.table_name
        if self.config.plural:
            return self.config.plural
        return self._plural

    @property
    def route_name(self) -> str:
        """
        Returns the route name for the object.

        Returns:
            The route name for the object.
        """
        if self.config.route_name:
            return self.config.route_name
        if self.config.plural:
            return self.config.plural.replace('_', '-')
        return self._plural.replace('_', '-')


class AppProject(TemplateModel):
    """
    A class that represents an app project.

    Attributes:
        name: str: The name of the model. Name should be snake_case. From TemplateModel
        app_objects: list[AppObject]: The list of app objects in the project.
    """

    app_objects: list[AppObject]

    def __init__(self, name: str, *args: AppObject):
        """
        Initialize the project with the given name and app objects.

        Args:
            name: The name of the project.
            args: A list of app objects for the project.
        """
        super().__init__(name=name, app_objects=args)
