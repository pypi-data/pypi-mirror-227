import inspect
from typing import Any, Optional, Sequence, Tuple

from langsmith.run_helpers import trace, _get_inputs
import logging

logger = logging.getLogger(__name__)


class ModuleWrapper:
    __slots__ = ["_lc_module", "_lc_full_path", "__weakref__", "_run_type"]

    def __init__(self, module: Any, module_path: Optional[Sequence[str]] = None):
        object.__setattr__(self, "_lc_module", module)
        full_module = module_path or []
        full_module.append(module.__name__)
        object.__setattr__(self, "_lc_full_path", full_module)
        object.__setattr__(self, "_run_type", "chain")

    def __getattr__(self, name: str) -> Any:
        attr = getattr(object.__getattribute__(self, "_lc_module"), name)
        if inspect.isclass(attr) or inspect.isfunction(attr) or inspect.ismethod(attr):
            return self.__class__(attr, object.__getattribute__(self, "_lc_full_path"))
        return attr

    def __setattr__(self, name, value):
        setattr(self._lc_module, name, value)

    def __delattr__(self, name):
        delattr(self._lc_module, name)

    def _langsmith_convert_input(self, input: Any) -> Tuple[dict, Optional[dict]]:
        return _get_inputs(input), None

    def _langsmith_convert_output(self, output: Any) -> dict:
        return {"output": output}

    def __call__(self, *args, **kwargs):
        function_object = object.__getattribute__(self, "_lc_module")
        if inspect.isclass(function_object):
            return self.__class__(
                function_object(*args, **kwargs),
            )
        run_name = ".".join(object.__getattribute__(self, "_lc_full_path"))
        run_type = object.__getattribute__(
            self,
            "_run_type",
        )
        try:
            mapped_inputs, extra = self._langsmith_convert_input(
                inspect.signature(function_object, args, kwargs)
            )
        except Exception as e:
            logger.debug(f"Failed to convert inputs for {run_name}: {e}")
            mapped_inputs, extra = {}, None
        with trace(
            run_type=run_type, name=run_name, inputs=mapped_inputs, extra=extra
        ) as run_tree:
            function_response = function_object(*args, **kwargs)
            run_tree.end(outputs=self._langsmith_convert_output(function_response))
        return function_response

    def __repr__(self) -> str:
        return repr(object.__getattribute__(self, "_lc_module"))
