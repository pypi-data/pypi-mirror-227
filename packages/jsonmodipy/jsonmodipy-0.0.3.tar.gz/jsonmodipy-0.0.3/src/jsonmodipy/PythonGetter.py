"""Convert Python file content to modular Python code storage structures, and
from those code structures to Json."""
import ast
from typing import List, Union

import astunparse  # type: ignore[import]
from comparison import (  # type: ignore[import]
    equal_without_multi_spaces,
    get_without_empty_lines,
    remove_empty_lines,
)
from file_parsing import (  # type: ignore[import]
    delete_file_if_exists,
    format_python_file,
    load_file_content,
    set_file_content,
    write_dict_to_json,
)
from HC import HC  # type: ignore[import]
from helper import pretty_print  # type: ignore[import]
from PythonSetter import PythonSetter  # type: ignore[import]
from PythonStructures import (  # type: ignore[import]
    ArgStorage,
    ClassStorage,
    CodeStorage,
    Docstring,
    DocumentationStorage,
    JsonContent,
    MethodsStorage,
    TypeStorage,
)
from typeguard import typechecked


# pylint: disable=R0902
class PythonGetter:
    """A class to convert Python file content to modular Python code storage
    structures, and from those code structures to Json."""

    @typechecked
    def __init__(self, python_content: str, file_dir: str, raw_filename: str):
        self.python_content: str = python_content
        self.file_dir: str = file_dir
        self.raw_filename: str = raw_filename
        self.tree: ast.Module = ast.parse(
            self.python_content, type_comments=True
        )
        self.json_content: JsonContent = self.code_to_structure(tree=self.tree)

        # Write python code to dummy file.
        self.hardcoded: HC = HC()
        self.original_py_filepath: str = f"{file_dir}{raw_filename}.py"
        # TODO: assert file does not yet exist.
        self.dummy_filepath: str = (
            f"{file_dir}{self.hardcoded.reconstruct_id}{raw_filename}.py"
        )
        self.json_dummy_filepath: str = (
            f"{file_dir}{self.hardcoded.reconstruct_id}{raw_filename}.json"
        )

        write_dict_to_json(
            data=self.json_content.to_dict(), filepath=self.json_dummy_filepath
        )

        self.verify_code_retrievability(
            dummy_filepath=self.dummy_filepath,
            original_py_filepath=self.original_py_filepath,
            json_content=self.json_content,
            file_dir=self.file_dir,
            raw_filename=self.raw_filename,
        )

    @typechecked
    def code_to_structure(self, tree: ast.Module) -> JsonContent:
        """Extracts class names and docstrings from Python content.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing class names
            and docstrings.
        """
        json_content: JsonContent = ast_to_json_content(tree=tree)
        return json_content

    # pylint: disable=R0913
    @typechecked
    def verify_code_retrievability(
        self,
        dummy_filepath: str,
        original_py_filepath: str,
        json_content: JsonContent,
        file_dir: str,
        raw_filename: str,
    ) -> None:
        """Verifies that the json file can be convert back into the original
        Python file before proceeding."""
        python_setter: PythonSetter = PythonSetter(
            file_dir=file_dir, raw_filename=raw_filename
        )

        # Convert JSON filecontent back to JsonContent object.
        new_json_content: JsonContent = (
            python_setter.convert_from_json_to_structure(
                json_dict=json_content.to_dict()
            )
        )
        # Convert the JsonContent structure back to Python code.
        python_code: str = python_setter.structure_to_python(
            json_content=new_json_content
        )

        delete_file_if_exists(file_path=dummy_filepath)
        set_file_content(
            file_path=dummy_filepath,
            content=remove_empty_lines(text=python_code),
        )

        # Apply black formatting to original Python file and dummy file.
        format_python_file(file_path=original_py_filepath)
        format_python_file(file_path=dummy_filepath)

        original_content: str = load_file_content(
            file_path=original_py_filepath
        )
        reconstructed_content: str = load_file_content(
            file_path=dummy_filepath
        )
        collapsed_original: str = get_without_empty_lines(
            text=original_content
        )
        collapsed_reconstructed: str = get_without_empty_lines(
            text=reconstructed_content
        )
        if not equal_without_multi_spaces(
            original=collapsed_original, reconstructed=collapsed_reconstructed
        ):
            print("Original:")
            print(collapsed_original)
            print("Reconstructed:")
            print(collapsed_reconstructed)
            print("Original filepath:")
            print(original_py_filepath)
            raise ValueError(
                "Error, without newlines the reconstructed python file is not"
                + " identical to the original Python file."
            )


@typechecked
def convert_arg(node: ast.arg) -> ArgStorage:
    """Converts a class into a Python storage structure for a class or method
    argument."""
    if node.annotation is None:
        return ArgStorage(name=node.arg)
    raise ValueError(
        "Error, the node.annotation.id parameter does not exist."
        "So it is not yet known what to do in this case."
    )


@typechecked
def convert_function(
    node: ast.FunctionDef, hc: HC, indentation: int
) -> MethodsStorage:
    """Converts a class into a Python storage structure for a method."""
    arguments: List[ArgStorage] = [convert_arg(arg) for arg in node.args.args]
    children: List[
        Union[
            ClassStorage,
            CodeStorage,
            DocumentationStorage,
            MethodsStorage,
        ]
    ] = []
    for stmt in node.body:
        if isinstance(stmt, ast.FunctionDef):
            children.append(
                convert_function(
                    node=stmt,
                    hc=hc,
                    indentation=indentation + hc.indent_spaces,
                )
            )
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str):
            children.append(
                DocumentationStorage(
                    documentation_content=stmt.value.s, indentation=indentation
                )
            )
        else:
            source_code: str = astunparse.unparse(stmt)
            children.append(
                CodeStorage(
                    code_content=source_code,
                    indentation=indentation,
                )
            )

    if node.returns is None:
        returnType = TypeStorage(name="")
    return MethodsStorage(
        arguments=arguments,
        children=children,
        documentation=ast.get_docstring(node) or "",
        name=node.name,
        returnType=returnType,
    )


@typechecked
def convert_class(
    node: ast.ClassDef, hc: HC, indentation: int
) -> ClassStorage:
    """Converts a class into a Python storage structure for a class."""
    arguments: List[ArgStorage] = [
        convert_arg(arg) for arg in node.body if isinstance(arg, ast.arg)
    ]
    children: List[
        Union[ClassStorage, CodeStorage, DocumentationStorage, MethodsStorage]
    ] = []
    for stmt in node.body:
        if isinstance(stmt, ast.FunctionDef):
            children.append(
                convert_function(
                    node=stmt,
                    hc=hc,
                    indentation=indentation + hc.indent_spaces,
                )
            )
        elif isinstance(stmt, ast.ClassDef):
            children.append(
                convert_class(
                    node=stmt,
                    hc=hc,
                    indentation=indentation + hc.indent_spaces,
                )
            )
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str):
            children.append(
                CodeStorage(
                    code_content=stmt.value.s,
                    indentation=indentation + hc.indent_spaces,
                )
            )
        else:
            print(f"stmt={stmt}")
            raise ValueError(
                f"Error, this code type is not yet supported:{stmt}"
            )
    return ClassStorage(
        documentation=ast.get_docstring(node) or "",
        name=node.name,
        arguments=arguments,
        children=children,
        returnType=TypeStorage(name=type(None)),
    )


@typechecked
def ast_to_json_content(tree: ast.Module) -> JsonContent:
    """Converts an abstract syntax tree to a Python storage structure."""
    code_elems: List[
        Union[ClassStorage, CodeStorage, DocumentationStorage, MethodsStorage]
    ] = []
    docstring: str = ""
    hc: HC = HC()

    pretty_print(data=tree.__dict__)

    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            docstring = node.value.s
        elif isinstance(node, ast.FunctionDef):
            code_elems.append(
                convert_function(
                    node=node, hc=hc, indentation=0 + hc.indent_spaces
                )
            )
        elif isinstance(node, ast.ClassDef):
            code_elems.append(
                convert_class(
                    node=node, hc=hc, indentation=0 + hc.indent_spaces
                )
            )
        else:
            print(f"node={node}")
            raise ValueError(
                f"Error, this code type is not yet supported:{node}"
            )

    return JsonContent(
        docstring=Docstring(docstring=docstring), code_elems=code_elems
    )
