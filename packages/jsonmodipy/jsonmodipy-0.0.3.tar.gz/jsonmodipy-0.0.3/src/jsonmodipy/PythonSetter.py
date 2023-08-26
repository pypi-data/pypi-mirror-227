"""Convert a JSON filecontent back into modular Python code storage structures,
and from those code structures back to a Python filecontent."""

from typing import Dict, List, Union, cast

from file_parsing import load_dict_from_json  # type: ignore[import]
from HC import HC  # type: ignore[import]
from PythonStructures import (  # type: ignore[import]
    ArgStorage,
    ClassStorage,
    ClassStorageType,
    CodeStorage,
    CodeStorageType,
    Docstring,
    DocumentationStorage,
    DocumentationStorageType,
    JsonContent,
    JsonContentType,
    MethodsStorage,
    MethodStorageType,
    TypeStorage,
)
from typeguard import typechecked


class PythonSetter:
    """A class to convert a JSON filecontent back into modular Python code
    storage structures, and from those code structures back to a Python
    filecontent."""

    @typechecked
    def __init__(self, file_dir: str, raw_filename: str):
        self.file_dir: str = file_dir
        self.raw_filename: str = raw_filename

        # Write python code to dummy file.
        self.hardcoded: HC = HC()
        self.json_dummy_filepath: str = (
            f"{file_dir}{self.hardcoded.reconstruct_id}{raw_filename}.json"
        )

        self.json_dict: JsonContentType = load_dict_from_json(
            filename=self.json_dummy_filepath
        )
        self.json_content: JsonContent = self.convert_from_json_to_structure(
            json_dict=self.json_dict
        )
        self.python_code: str = self.structure_to_python(
            json_content=self.json_content
        )

    @typechecked
    def convert_from_json_to_structure(
        self,
        json_dict: JsonContentType,
    ) -> JsonContent:
        """Converts modular JSON back to Python code structures.

        Args:
            json_content (str): JSON content.

        Returns:
            str: Python file content.
        """
        if isinstance(json_dict["code_elems"], List):
            code_elements: List[
                Union[
                    ClassStorageType,
                    CodeStorageType,
                    DocumentationStorageType,
                    MethodStorageType,
                ]
            ] = json_dict["code_elems"]
        else:
            raise TypeError("Error, expected list of code elements.")

        json_content: JsonContent = JsonContent(
            docstring=Docstring(docstring=str(json_dict["docstring"])),
            code_elems=self.children_to_python_structure(
                json_list=code_elements
            ),
        )
        return json_content

    @typechecked
    def children_to_python_structure(
        self,
        json_list: List[
            Union[
                ClassStorageType,
                CodeStorageType,
                DocumentationStorageType,
                MethodStorageType,
            ]
        ],
    ) -> List[
        Union[
            ClassStorage,
            CodeStorage,
            DocumentationStorage,
            MethodsStorage,
        ]
    ]:
        """Recursively convert a list of child elements into Python structure
        objects."""
        # pylint: disable=R0801
        children: List[
            Union[
                ClassStorage,
                CodeStorage,
                DocumentationStorage,
                MethodsStorage,
            ]
        ] = []

        child: Union[
            ClassStorageType,
            CodeStorageType,
            DocumentationStorageType,
            MethodStorageType,
        ]
        for child in json_list:
            if "class" in child:
                children.append(
                    self.json_str_to_class(child=cast(ClassStorageType, child))
                )
            elif "method" in child:
                children.append(
                    self.json_str_to_method(
                        child=cast(MethodStorageType, child)
                    )
                )

            elif "code_content" in child:
                if isinstance(child["code_content"], str) and isinstance(
                    child["indentation"], int
                ):
                    children.append(
                        CodeStorage(
                            code_content=child["code_content"],
                            indentation=child["indentation"],
                        )
                    )
                else:
                    raise TypeError(
                        "Error, expected types str and int for code content "
                        + " and indentation."
                    )
            elif "documentation_content" in child:
                if isinstance(
                    child["documentation_content"], str
                ) and isinstance(child["indentation"], int):
                    children.append(
                        DocumentationStorage(
                            documentation_content=child[
                                "documentation_content"
                            ],
                            indentation=child["indentation"],
                        )
                    )
                else:
                    raise TypeError(
                        "Error, expected types str and int for documentation "
                        + "content and indentation."
                    )
            else:
                raise KeyError(f"Error did not expect key:{child}")
        return children

    @typechecked
    def json_str_to_class(self, child: ClassStorageType) -> ClassStorage:
        """Converts a child dictionary back into a ClassStorage object."""
        class_storage: ClassStorage = ClassStorage(
            documentation=str(child["class"]["documentation"]),
            name=str(child["class"]["name"]),
            arguments=list(
                map(
                    lambda arg: ArgStorage(
                        argType=TypeStorage(name=arg["argtype"]),
                        name=arg["name"],
                    ),
                    child["class"]["arguments"],
                )
            ),
            children=self.children_to_python_structure(
                cast(
                    List[
                        Union[
                            ClassStorageType,
                            CodeStorageType,
                            DocumentationStorageType,
                            MethodStorageType,
                        ]
                    ],
                    child["class"]["children"],
                )
            ),
            returnType=TypeStorage(name=str(child["class"]["returnType"])),
        )
        return class_storage

    @typechecked
    def json_str_to_method(self, child: MethodStorageType) -> MethodsStorage:
        """Converts a child dictionary back into a MethodsStorage object."""
        argList: List[ArgStorage] = list(
            map(
                lambda arg: json_arg_dict_to_argstorage(arg_dict=arg),
                child["method"]["arguments"],
            )
        )
        method_storage = MethodsStorage(
            documentation=str(child["method"]["documentation"]),
            name=str(child["method"]["name"]),
            arguments=argList,
            children=self.children_to_python_structure(
                cast(
                    List[
                        Union[
                            ClassStorageType,
                            CodeStorageType,
                            DocumentationStorageType,
                            MethodStorageType,
                        ]
                    ],
                    child["method"]["children"],
                )
            ),
            returnType=TypeStorage(name=str(child["method"]["returnType"])),
        )
        return method_storage

    @typechecked
    def structure_to_python(self, json_content: JsonContent) -> str:
        """Converts Python code structure back to Python file content.

        Args:
            json_content (str): JSON content.

        Returns:
            Optional[str]: Python file content, or None if conversion fails.
        """
        return str(json_content.to_python_string())


@typechecked
def json_arg_dict_to_argstorage(arg_dict: Dict[str, str]) -> ArgStorage:
    """Converts a class into a Python storage structure for a class or method
    argument."""
    if "argType" in arg_dict.keys():
        return ArgStorage(
            argType=TypeStorage(name=arg_dict["argType"]),
            name=arg_dict["name"],
        )
    return ArgStorage(
        name=arg_dict["name"],
    )
