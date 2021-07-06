from __future__ import annotations

import typing
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


@dataclass
class ElementParser:
    tag: typing.ClassVar[str] = ""
    children: typing.ClassVar[typing.List[typing.Type[ElementParser]]] = []

    parent: typing.Optional[ElementParser] = None
    data: typing.List[typing.Tuple[str, typing.Any]] = field(default_factory=list)

    def parse(self, e: ET.Element) -> typing.Any:

        parent: typing.Optional[ElementParser] = self
        while parent is not None:
            parser = next((p for p in parent.children if p.tag == e.tag), None)
            if parser:
                return parser(parent=parent)

            parent = parent.parent

        # parser = next((p for p in self.children if p.tag == e.tag), None)
        # if parser:
        #     return parser(parent=self)

    def end(self, e: ET.Element) -> typing.Any:
        return None


@dataclass
class DocumentParser(ElementParser):
    def __init__(self, root: typing.Type[ElementParser]) -> None:
        DocumentParser.children = [root]
        super().__init__()


def parse(content: typing.IO[bytes], parser: typing.Type[ElementParser]) -> typing.Any:
    elements = ET.iterparse(content, events=("start", "end"))
    document_parser = DocumentParser(root=parser)
    parsers: typing.List[typing.Tuple[str, typing.Optional[ElementParser]]] = [
        ("", document_parser)
    ]
    for event, element in elements:
        current_element_parser = parsers[-1][1]
        if event == "start":
            if current_element_parser is not None:
                next_element_parser = current_element_parser.parse(element)
                if next_element_parser:
                    parsers.append((next_element_parser.tag, next_element_parser))
                    continue

            # parsers.append((element.tag, None))
            parsers.append((element.tag, ElementParser(parent=current_element_parser)))
        else:
            if current_element_parser is not None:
                data = current_element_parser.end(element)
                if data and current_element_parser.parent:
                    current_element_parser.parent.data.append((element.tag, data))

            parsers.pop()
            # element.clear()

    return document_parser.data[0][1]
