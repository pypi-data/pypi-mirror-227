"""Helper functions for validating inputs."""
import pathlib
import typing


def validate_dir_or_raise(output_dir, name="Directory"):
    if not isinstance(output_dir, (str, pathlib.Path)):
        raise TypeError(f"{name} must be a string.")
    if not pathlib.Path(output_dir).exists():
        raise FileNotFoundError(f"{name} must exist.")
    if output_dir is None or not pathlib.Path(output_dir).is_dir():
        raise NotADirectoryError(f"{name} must be specified.")


def validate_chip_list_or_raise(chips: list[int], params: dict):
    num_chips = len(params.get("chips", ["single"]))
    if not isinstance(chips, list):
        raise TypeError("Chips must be a list.")
    if len(chips) != len(set(chips)):
        raise ValueError("One or more chip numbers is repeated.")
    for chip in chips:
        if not isinstance(chip, int):
            raise TypeError("Chips must be a list of integers.")
        if not 0 <= chip < num_chips:
            raise ValueError("One or more chip numbers is out of range.")


def validate_channel_sequence_or_raise(params: dict, channels: typing.Iterable[int]):
    max_channels = params["channels"]
    if not isinstance(channels, typing.Iterable):
        raise TypeError("Value must be iterable")
    if not all(isinstance(c, int) for c in channels):
        raise TypeError("All channels must be integers")
    if not all(0 <= c < max_channels for c in channels):
        raise ValueError(f"All channels must be in range 0-{max_channels - 1}")
    if len(channels) != len(set(channels)):
        raise ValueError("One or more channels is repeated.")


def validate_positive_int_or_raise(value: int):
    if not isinstance(value, int):
        raise TypeError(f"value must be an integer.")
    if value <= 0:
        raise ValueError(f"value must be positive.")


def validate_non_negative_int_or_raise(value: int):
    if not isinstance(value, int):
        raise TypeError(f"value must be an integer.")
    if value < 0:
        raise ValueError(f"value must be non-negative.")


def validate_callable_or_raise(fn: typing.Callable):
    # this is incomplete, but works for most callable objects
    if not callable(fn):
        raise TypeError("Value must be callable.")


def validate_readout_settings(readout_settings: dict):
    valid_readout_settings = {
        "trig": ["i", "s", "e"],
        "lb": ["t", "f", "r"],
        "acq": ["p", "r"],
        "ped": ["z", "c", "r"],
        "readoutEn": [True, False],
        "singleEv": [True, False],
    }

    # Validate values
    for key, value in readout_settings.items():
        expected = valid_readout_settings.get(key, None)
        test_val = value[0] if isinstance(value, str) else value
        if expected is None:
            raise KeyError(f"'{key}' is not a valid readout setting.")
        if test_val not in expected:
            raise KeyError(
                f"'{value}' is not a valid value for setting '{key}'. Valid values are {expected}"
            )
