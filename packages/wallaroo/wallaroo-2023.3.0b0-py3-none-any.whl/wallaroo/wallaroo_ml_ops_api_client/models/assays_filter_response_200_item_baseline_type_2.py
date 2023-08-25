from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.assays_filter_response_200_item_baseline_type_2_fixed import \
      AssaysFilterResponse200ItemBaselineType2Fixed





T = TypeVar("T", bound="AssaysFilterResponse200ItemBaselineType2")


@attr.s(auto_attribs=True)
class AssaysFilterResponse200ItemBaselineType2:
    """ 
        Attributes:
            fixed (AssaysFilterResponse200ItemBaselineType2Fixed):
     """

    fixed: 'AssaysFilterResponse200ItemBaselineType2Fixed'
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        fixed = self.fixed.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "Fixed": fixed,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assays_filter_response_200_item_baseline_type_2_fixed import \
            AssaysFilterResponse200ItemBaselineType2Fixed
        d = src_dict.copy()
        fixed = AssaysFilterResponse200ItemBaselineType2Fixed.from_dict(d.pop("Fixed"))




        assays_filter_response_200_item_baseline_type_2 = cls(
            fixed=fixed,
        )

        assays_filter_response_200_item_baseline_type_2.additional_properties = d
        return assays_filter_response_200_item_baseline_type_2

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
