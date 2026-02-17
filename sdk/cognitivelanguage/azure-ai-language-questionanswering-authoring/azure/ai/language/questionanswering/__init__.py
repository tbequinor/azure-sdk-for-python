__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

# The authoring distribution shares the `azure.ai.language.questionanswering` namespace
# with the runtime distribution. When both are installed, users expect runtime symbols
# (like `QuestionAnsweringClient`) to remain importable from this package.
try:
    from ._client import QuestionAnsweringClient  # type: ignore
    from ._version import VERSION  # type: ignore

    __version__ = VERSION
    __all__ = ["QuestionAnsweringClient"]
except ImportError:
    __all__ = []
