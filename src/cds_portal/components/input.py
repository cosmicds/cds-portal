from solara.alias import rv as v
import solara
from typing import Callable, Dict, List, Optional, TypeVar, Union

from solara.components.input import _use_input_type, use_change


T = TypeVar("T")

@solara.component
def NumericInput(
    str_to_numeric: Callable[[Optional[str]], T],
    label: str,
    value: Union[None, T, solara.Reactive[Optional[T]], solara.Reactive[T]],
    on_value: Union[None, Callable[[Optional[T]], None], Callable[[T], None]] = None,
    on_error_change: Union[None, Callable[[Optional[bool]], None], Callable[[bool], None]] = None,
    disabled: bool = False,
    continuous_update: bool = False,
    clearable: bool = False,
    hide_details: Optional[Union[bool, str]] = None,
    outlined: bool = False,
    classes: List[str] = [],
    style: Optional[Union[str, Dict[str, str]]] = None,
):
    """Integer input.

    ## Arguments

    * `label`: Label to display next to the slider.
    * `value`: The currently entered value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the input is disabled.
    * `continuous_update`: Whether to call the `on_value` callback on every change or only when the input loses focus or the enter key is pressed.
    * `classes`: List of CSS classes to apply to the input.
    * `style`: CSS style to apply to the input.
    """


    style_flat = solara.util._flatten_style(style)
    classes_flat = solara.util._combine_classes(classes)

    internal_value, error, set_value_cast = _use_input_type(
        value,
        str_to_numeric,
        str,
        on_value,
    )

    def on_v_model(value):
        if continuous_update:
            set_value_cast(value)

    if on_error_change:
        on_error_change(bool(error))

    if error:
        label += f" ({error})"
    text_field = v.TextField(
        v_model=internal_value,
        on_v_model=on_v_model,
        label=label,
        disabled=disabled,
        outlined=outlined,
        # we are not using the number type, since we cannot validate invalid input
        # see https://stackoverflow.blog/2022/12/26/why-the-number-input-is-the-worst-input/
        # type="number",
        hide_details=hide_details,
        clearable=clearable,
        error=bool(error),
        class_=classes_flat,
        style_=style_flat,
    )
    # use_change(text_field, set_value_cast, enabled=not continuous_update)
    return text_field


@solara.component
def IntegerInput(
    label: str,
    value: Union[None, int, solara.Reactive[Optional[int]], solara.Reactive[int]],
    on_value: Union[None, Callable[[Optional[int]], None], Callable[[int], None]] = None,
    on_error_change: Union[None, Callable[[Optional[bool]], None], Callable[[bool], None]] = None,
    disabled: bool = False,
    continuous_update: bool = False,
    clearable: bool = False,
    hide_details: Optional[Union[bool, str]] = None,
    optional: bool = False,
    outlined: bool = False,
    classes: List[str] = [],
    style: Optional[Union[str, Dict[str, str]]] = None,
):

    def str_to_int(value: Optional[str]) -> Optional[int]:
        if value:
            try:
                return int(value)
            except ValueError:
                if optional:
                    return None
                raise ValueError("Value must be an integer")
        else:
            if optional:
                return None
            else:
                raise ValueError("Value cannot be empty")

    return NumericInput(
        str_to_int,
        label=label,
        value=value,
        on_value=on_value,
        on_error_change=on_error_change,
        disabled=disabled,
        continuous_update=continuous_update,
        clearable=clearable,
        hide_details=hide_details,
        classes=classes,
        outlined=outlined,
        style=style,
    )
