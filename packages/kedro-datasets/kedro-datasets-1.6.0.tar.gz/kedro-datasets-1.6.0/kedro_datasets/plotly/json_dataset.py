"""``JSONDataSet`` loads/saves a plotly figure from/to a JSON file using an underlying
filesystem (e.g.: local, S3, GCS).
"""
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Dict, Union

import fsspec
import plotly.io as pio
from kedro.io.core import Version, get_filepath_str, get_protocol_and_path
from plotly import graph_objects as go

from .._io import AbstractVersionedDataset as AbstractVersionedDataSet


class JSONDataSet(
    AbstractVersionedDataSet[go.Figure, Union[go.Figure, go.FigureWidget]]
):
    """``JSONDataSet`` loads/saves a plotly figure from/to a JSON file using an
    underlying filesystem (e.g.: local, S3, GCS).

    Example usage for the
    `YAML API <https://kedro.readthedocs.io/en/stable/data/\
    data_catalog.html#use-the-data-catalog-with-the-yaml-api>`_:

    .. code-block:: yaml

        scatter_plot:
          type: plotly.JSONDataSet
          filepath: data/08_reporting/scatter_plot.json
          save_args:
            engine: auto

    Example usage for the
    `Python API <https://kedro.readthedocs.io/en/stable/data/\
    data_catalog.html#use-the-data-catalog-with-the-code-api>`_:
    ::

        >>> from kedro_datasets.plotly import JSONDataSet
        >>> import plotly.express as px
        >>>
        >>> fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
        >>> data_set = JSONDataSet(filepath="test.json")
        >>> data_set.save(fig)
        >>> reloaded = data_set.load()
        >>> assert fig == reloaded
    """

    DEFAULT_LOAD_ARGS: Dict[str, Any] = {}
    DEFAULT_SAVE_ARGS: Dict[str, Any] = {}

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        filepath: str,
        load_args: Dict[str, Any] = None,
        save_args: Dict[str, Any] = None,
        version: Version = None,
        credentials: Dict[str, Any] = None,
        fs_args: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """Creates a new instance of ``JSONDataSet`` pointing to a concrete JSON file
        on a specific filesystem.

        Args:
            filepath: Filepath in POSIX format to a JSON file prefixed with a protocol like `s3://`.
                If prefix is not provided `file` protocol (local filesystem) will be used.
                The prefix should be any protocol supported by ``fsspec``.
                Note: `http(s)` doesn't support versioning.
            load_args: Plotly options for loading JSON files.
                Here you can find all available arguments:
                https://plotly.com/python-api-reference/generated/plotly.io.from_json.html#plotly.io.from_json
                All defaults are preserved.
            save_args: Plotly options for saving JSON files.
                Here you can find all available arguments:
                https://plotly.com/python-api-reference/generated/plotly.io.write_json.html
                All defaults are preserved.
            version: If specified, should be an instance of
                ``kedro.io.core.Version``. If its ``load`` attribute is
                None, the latest version will be loaded. If its ``save``
                attribute is None, save version will be autogenerated.
            credentials: Credentials required to get access to the underlying filesystem.
                E.g. for ``GCSFileSystem`` it should look like `{'token': None}`.
            fs_args: Extra arguments to pass into underlying filesystem class constructor
                (e.g. `{"project": "my-project"}` for ``GCSFileSystem``), as well as
                to pass to the filesystem's `open` method through nested keys
                `open_args_load` and `open_args_save`.
                Here you can find all available arguments for `open`:
                https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.spec.AbstractFileSystem.open
                All defaults are preserved, except `mode`, which is set to `w` when
                saving.
            metadata: Any arbitrary metadata.
                This is ignored by Kedro, but may be consumed by users or external plugins.
        """
        _fs_args = deepcopy(fs_args) or {}
        _fs_open_args_load = _fs_args.pop("open_args_load", {})
        _fs_open_args_save = _fs_args.pop("open_args_save", {})
        _credentials = deepcopy(credentials) or {}

        protocol, path = get_protocol_and_path(filepath, version)
        if protocol == "file":
            _fs_args.setdefault("auto_mkdir", True)

        self._protocol = protocol
        self._fs = fsspec.filesystem(self._protocol, **_credentials, **_fs_args)

        self.metadata = metadata

        super().__init__(
            filepath=PurePosixPath(path),
            version=version,
            exists_function=self._fs.exists,
            glob_function=self._fs.glob,
        )

        # Handle default load and save arguments
        self._load_args = deepcopy(self.DEFAULT_LOAD_ARGS)
        if load_args is not None:
            self._load_args.update(load_args)
        self._save_args = deepcopy(self.DEFAULT_SAVE_ARGS)
        if save_args is not None:
            self._save_args.update(save_args)

        _fs_open_args_save.setdefault("mode", "w")
        self._fs_open_args_load = _fs_open_args_load
        self._fs_open_args_save = _fs_open_args_save

    def _describe(self) -> Dict[str, Any]:
        return {
            "filepath": self._filepath,
            "protocol": self._protocol,
            "load_args": self._load_args,
            "save_args": self._save_args,
            "version": self._version,
        }

    def _load(self) -> Union[go.Figure, go.FigureWidget]:
        load_path = get_filepath_str(self._get_load_path(), self._protocol)

        with self._fs.open(load_path, **self._fs_open_args_load) as fs_file:
            # read_json doesn't work correctly with file handler, so we have to read
            # the file, decode it manually and pass to the low-level from_json instead.
            return pio.from_json(str(fs_file.read(), "utf-8"), **self._load_args)

    def _save(self, data: go.Figure) -> None:
        save_path = get_filepath_str(self._get_save_path(), self._protocol)

        with self._fs.open(save_path, **self._fs_open_args_save) as fs_file:
            data.write_json(fs_file, **self._save_args)

        self._invalidate_cache()

    def _exists(self) -> bool:
        load_path = get_filepath_str(self._get_load_path(), self._protocol)

        return self._fs.exists(load_path)

    def _release(self) -> None:
        super()._release()
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        filepath = get_filepath_str(self._filepath, self._protocol)
        self._fs.invalidate_cache(filepath)
