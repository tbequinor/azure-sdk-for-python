# The MIT License (MIT)
# Copyright (c) Microsoft Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Configuration types for Azure Cosmos DB availability strategies."""

from typing import Optional, Any, Union

# Default values for cross-region hedging strategy
DEFAULT_THRESHOLD_MS = 500
DEFAULT_THRESHOLD_STEPS_MS = 100


class _ExplicitlyDisabled:
    """Sentinel class to indicate availability strategy is explicitly disabled.

    This is used to distinguish between "not set" (None/_Unset) and "explicitly disabled" (False).
    When explicitly disabled, client-level defaults should NOT be used.
    """
    _instance: Optional["_ExplicitlyDisabled"] = None

    def __new__(cls) -> "_ExplicitlyDisabled":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Singleton instance for explicit disable
EXPLICITLY_DISABLED: _ExplicitlyDisabled = _ExplicitlyDisabled()


class CrossRegionHedgingStrategy:
    """Configuration for cross-region request hedging strategy.

    :param config: Dictionary containing configuration values, defaults to None
    :type config: Optional[Dict[str, Any]]
    :raises ValueError: If configuration values are invalid
    
    The config dictionary can contain:
    - threshold_ms: Time in ms before routing to alternate region (default: 500)
    - threshold_steps_ms: Time interval between routing attempts (default: 100)
    """
    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        if config is None:
            self.threshold_ms = DEFAULT_THRESHOLD_MS
            self.threshold_steps_ms = DEFAULT_THRESHOLD_STEPS_MS
        else:
            self.threshold_ms = config.get("threshold_ms", DEFAULT_THRESHOLD_MS)
            self.threshold_steps_ms = config.get("threshold_steps_ms", DEFAULT_THRESHOLD_STEPS_MS)

        if self.threshold_ms <= 0:
            raise ValueError("threshold_ms must be positive")
        if self.threshold_steps_ms <= 0:
            raise ValueError("threshold_steps_ms must be positive")


def _validate_hedging_strategy(
        config: Optional[Union[bool, dict[str, Any]]]
) -> Optional[Union[CrossRegionHedgingStrategy, _ExplicitlyDisabled]]:
    """Validate and create a CrossRegionHedgingStrategy.
    
    :param config: Configuration for availability strategy. Can be:
        - None: Returns None (no strategy, uses client default if available)
        - True: Returns strategy with default values (threshold_ms=500, threshold_steps_ms=100)
        - False: Returns EXPLICITLY_DISABLED sentinel (overrides client defaults, no hedging)
        - dict: Returns strategy with values from dict, using defaults for missing keys
    :type config: Optional[Union[bool, Dict[str, Any]]]
    :returns: Validated configuration object, EXPLICITLY_DISABLED sentinel, or None
    :rtype: Optional[Union[CrossRegionHedgingStrategy, _ExplicitlyDisabled]]
    """
    if config is None:
        return None

    if isinstance(config, bool):
        if config:
            # True -> use default values
            return CrossRegionHedgingStrategy()
        else:
            # False -> explicitly disabled, returns sentinel to override client defaults
            return EXPLICITLY_DISABLED

    # dict -> use values from dict
    return CrossRegionHedgingStrategy(config)
