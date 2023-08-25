from __future__ import annotations
import ovito
from ..vis import PythonViewportOverlay
from ..data import DataCollection
from ..pipeline import Pipeline
import abc
import os
from contextlib import contextmanager
import traits.api
from typing import Any, Literal, Tuple, Optional, Generator
import numpy

class ViewportOverlayInterface(traits.api.HasStrictTraits):
    """
    Base: :py:class:`traits.has_traits.HasStrictTraits`

    Abstract base class for :ref:`custom viewport overlays <manual:viewport_layers.python_script>` written in Python.
    Implementations of the interface must at least provide the :py:meth:`render` method.

    .. versionadded:: 3.9.2
    """

    # Import the Canvas helper class defined by the C++ code into the namespace of this class.
    class Canvas(PythonViewportOverlay.ViewportOverlayCanvas):
        """
        This object gets passed to the :py:meth:`ViewportOverlayInterface.render` method by the system and provides various painting functions, which the user-defined
        overlay can invoke to draw graphics on top of a 3d viewport.
        """

        # Define these members only when generating the Sphinx documentation for the OVITO module.
        # Otherwise they are directly taken from the C++ base class implementation.
        if os.environ.get('OVITO_SPHINX_BUILD', False):
            @property
            def is_perspective(self) -> bool:
                """
                Indicates whether the 3d view being rendered uses a perspective projection or parallel projection. This depends on the selected :py:attr:`Viewport.type`.
                """
                return super().is_perspective

            @property
            def field_of_view(self) -> float:
                """
                The field of view of the viewport's camera (:py:attr:`Viewport.fov`). For perspective projections, this value specifies the frustum angle in the vertical direction
                (in radians). For orthogonal projections, this is the visible range in the vertical direction (in simulation units of length).
                """
                return super().field_of_view

            @property
            def size(self) -> tuple[int,int]:
                """
                The width and height in pixels of the image currently being rendered. These dimensions may represent a sub-region of the entire image when rendering a :ref:`multi-viewport layout <manual:viewport_layouts>`.
                The canvas size is measured in *device-independent pixels*, which may be converted to physical *device pixels* by multiplying the values by the :py:attr:`device_pixel_ratio`.
                """
                return super().size

            @property
            def device_pixel_ratio(self) -> float:
                """
                Ratio between (physical) *device pixels* and (logical) *device-independent pixels* of the rendering frame buffer. This ratio is usually 1.0 when rendering an offscreen image,
                but it may be larger when rendering an interactive viewport on a high-resolution display. The device pixel ratio is configured at the operating system level
                and allows `scaling up UI elements on high-dpi displays <https://en.wikipedia.org/wiki/Resolution_independence>`__.

                The physical resolution of the rendering frame buffer is equal to its logical :py:attr:`size` times the :py:attr:`device_pixel_ratio`.
                """
                return super().device_pixel_ratio

            @property
            def view_tm(self) -> numpy.ndarray:
                """
                Affine transformation matrix encoding the location and orientation of the virtual camera in the three-dimensional scene.
                This 3 by 4 matrix transforms points/vectors from world space to camera space.
                """
                return super().view_tm

            @property
            def projection_tm(self) -> numpy.ndarray:
                """
                3d projection matrix, which transforms coordinates from camera space to screen space.
                """
                return super().projection_tm

        @staticmethod
        def _anchor_to_qt_alignment(anchor: str):
            from ovito.qt_compat import QtCore
            if anchor == 'south west': return QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom
            if anchor == 'west': return QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
            if anchor == 'north west': return QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
            if anchor == 'north': return QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
            if anchor == 'north east': return QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop
            if anchor == 'east': return QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
            if anchor == 'south east': return QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom
            if anchor == 'south': return QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom
            if anchor == 'center': return QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
            raise ValueError(f"Invalid anchor value '{anchor}'. Must be one of: 'center', 'south west', 'west', 'north west', 'north', 'north east', 'east', 'south east', 'south'.")

        def draw_image(self,
                    image,
                    pos: tuple[float,float] = (0.0, 0.0),
                    size: tuple[float,float] | None = (1.0, 1.0),
                    anchor: str = "south west"):
            """
            Docs...
            """
            from ovito.qt_compat import shiboken
            from ovito.qt_compat import QtGui
            if not isinstance(image, QtGui.QImage):
                raise TypeError("Invalid image parameter value: expected a QImage.")
            if size is None:
                size = (image.width() * self.device_pixel_ratio, image.height() * self.device_pixel_ratio)
            self._draw_image(shiboken.getCppPointer(image)[0], pos, size, ViewportOverlayInterface.Canvas._anchor_to_qt_alignment(anchor))

        def draw_text(self,
                      text: str,
                      pos: tuple[float,float],
                      font_size: float = 0.05,
                      anchor: str = "south west",
                      color: tuple[float,float,float] = (0.0, 0.0, 0.0),
                      alpha: float = 1.0,
                      outline_color: tuple[float,float,float] = (1.0, 1.0, 1.0),
                      outline_width: float = 0.0,
                      tight_layout: bool = False,
                      rotation: float = 0.0):
            """
            Docs...
            """
            self._draw_text(text, pos, font_size, ViewportOverlayInterface.Canvas._anchor_to_qt_alignment(anchor), color, alpha, outline_color, outline_width, tight_layout, rotation)

        def text_bounds(self,
                        text: str,
                        pos: tuple[float,float] = (0.0, 0.0),
                        font_size: float = 0.05,
                        anchor: str = "south west",
                        outline_width: float = 0.0,
                        tight_layout: bool = False,
                        rotation: float = 0.0) -> tuple[tuple[float,float], tuple[float,float]]:
            """
            Docs...
            """
            return self._text_bounds(text, pos, font_size, ViewportOverlayInterface.Canvas._anchor_to_qt_alignment(anchor), outline_width, tight_layout, rotation)

        @contextmanager
        def qt_painter(self) -> Generator[QtGui.QPainter, None, None]:
            from ovito.qt_compat import QtGui
            image = QtGui.QImage(*self.resolution, self.preferred_qimage_format)
            image.fill(0)
            painter = QtGui.QPainter()
            painter.begin(image)
            yield painter
            painter.end()
            self.draw_image(image, pos=(0.0, 0.0), size=(1.0, 1.0))

        @contextmanager
        def mpl_figure(self,
                       pos: Tuple[float,float] = (0.5, 0.5),
                       size: Tuple[float,float] = (0.5, 0.5),
                       anchor: Literal["center", "north west", "west", "south west", "south", "south east", "east", "north east", "north"] = "center",
                       dpi: float = 100,
                       alpha: float = 0.0,
                       tight_layout: bool = False) -> Generator[matplotlib.figure.Figure, None, None]:
            from ovito.qt_compat import QtGui
            import matplotlib.pyplot as plt
            w = size[0] * self.resolution[0] / dpi
            h = size[1] * self.resolution[1] / dpi
            fig = plt.figure(figsize=(w,h), dpi=dpi, tight_layout=tight_layout)
            fig.patch.set_alpha(alpha) # Make background semi-transparent
            try:
                yield fig
                buffer = fig.canvas.print_to_buffer()
                image = QtGui.QImage(buffer[0], buffer[1][0], buffer[1][1], QtGui.QImage.Format_RGBA8888)
                self.draw_image(image, pos=pos, size=size, anchor=anchor)
            finally:
                plt.close(fig)

    # Abstract method that must be implemented by all sub-classes:
    @abc.abstractmethod
    def render(self, canvas: Canvas, *, data: DataCollection, pipeline: Pipeline | None, interactive: bool, frame: int, **kwargs):
        """
        To be written...
        """
        raise NotImplementedError("Abstract method render() must be implemented by the ViewportOverlayInterface derived class.")

ovito.vis.ViewportOverlayInterface = ViewportOverlayInterface
ovito.vis.PythonViewportOverlay.ViewportOverlayCanvas.draw_image = ViewportOverlayInterface.Canvas.draw_image
ovito.vis.PythonViewportOverlay.ViewportOverlayCanvas.draw_text = ViewportOverlayInterface.Canvas.draw_text
ovito.vis.PythonViewportOverlay.ViewportOverlayCanvas.text_bounds = ViewportOverlayInterface.Canvas.text_bounds
