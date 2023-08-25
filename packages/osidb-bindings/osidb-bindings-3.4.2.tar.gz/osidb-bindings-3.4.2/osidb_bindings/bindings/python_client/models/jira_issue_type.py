from typing import Any, Dict, List, Type, TypeVar

import attr

from ..types import UNSET, OSIDBModel

T = TypeVar("T", bound="JiraIssueType")


@attr.s(auto_attribs=True)
class JiraIssueType(OSIDBModel):
    """Jira issue type, can be a Task, Story or Epic."""

    id: int
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        jira_issue_type = cls(
            id=id,
            name=name,
        )

        jira_issue_type.additional_properties = d
        return jira_issue_type

    @staticmethod
    def get_fields():
        return {
            "id": int,
            "name": str,
        }

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
