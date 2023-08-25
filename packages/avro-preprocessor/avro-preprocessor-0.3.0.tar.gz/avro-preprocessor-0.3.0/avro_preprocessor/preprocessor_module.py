"""Base class for Avro Preprocessor modules"""

from abc import abstractmethod, ABC
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Generator, List, Optional, Tuple, Union

from avro_preprocessor.avro_domain import Avro
from avro_preprocessor.schemas_container import SchemasContainer

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2018, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"


@dataclass(frozen=True)  # pylint: disable=R0903
class Ancestor:
    """A data class for JSON ancestors"""
    node: Avro.Node
    key: Union[str, int]


class PreprocessorModule(ABC):
    """Base class for Avro Preprocessor modules"""

    def __init__(self, schemas: SchemasContainer) -> None:
        self.schemas: SchemasContainer = schemas
        self.current_schema_name = ""

        self.ancestors: List[Ancestor] = []

    @abstractmethod
    def process(self) -> None:
        """Entry method to process data with a module."""

    def processed_schemas_and_keys_iter(self) \
            -> Generator[Tuple[str, OrderedDict], None, None]:
        """
        A generator to iterate over processed schemas and autogenerated keys.
        It also sets the current schema name, so it can be retrieved by AvroPreprocessor
        in case an exception happens.
        """
        all_schemas = list(self.schemas.processed.items()) \
                      + list(self.schemas.autogenerated_keys.items())

        for schema_name, schema in all_schemas:
            self.current_schema_name = schema_name
            yield schema_name, schema

    def processed_schemas_iter(self) -> \
            Generator[Tuple[str, OrderedDict], None, None]:
        """
        A generator to iterate over processed schemas.
        It also sets the current schema name, so it can be retrieved by AvroPreprocessor
        in case an exception happens.
        """
        for schema_name, schema in self.schemas.processed.items():
            self.current_schema_name = schema_name
            yield schema_name, schema

    def original_schemas_iter(self) -> Generator[Tuple[str, OrderedDict], None, None]:
        """
        A generator to iterate over original schemas.
        It also sets the current schema name, so it can be retrieved by AvroPreprocessor
        in case an exception happens.
        """
        for schema_name, schema in self.schemas.original.items():
            self.current_schema_name = schema_name
            yield schema_name, schema

    def traverse_schema(
            self,
            func: Callable[[Avro.Node], Optional[bool]],
            node: Avro.Node,
    ) -> None:
        """
        Traverse a schema and apply 'func' to chosen elements.
        :param func: The function to apply, can return bool or None
        :param node: The [Avro.Node] to traverse
        """

        self.ancestors.clear()
        self.do_traverse_schema(func, node)

    def do_traverse_schema(
            self,
            func: Callable[[Avro.Node], Optional[bool]],
            node: Avro.Node,
    ) -> Optional[bool]:
        """
        Helper function to recursively traverse a schema and apply 'func' to chosen elements.
        Returns True if it changed the data (so it can be applied again).
        :param func: The function to apply, can return bool or None
        :param node: The [Avro.Node] to traverse
        :return: bool
        """

        res = func(node)

        if isinstance(node, (list, OrderedDict)):

            # modifying node[key] while iterating. Here do not use e.g.
            # for key, value in node.items():
            for key in range(len(node)) if isinstance(node, list) else node.keys():

                self.ancestors.append(Ancestor(node, key))

                while self.do_traverse_schema(func, node[key]):
                    pass

                self.ancestors.pop()

        return res
