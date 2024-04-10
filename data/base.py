import dataclasses
from dataclasses import dataclass, fields, field
from typing import NamedTuple, TypeAlias
import SimpleITK as sitk
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonCore import vtkDataArray


ALLOW_PHI = True
CAN_ERASE_PHI_AT_INIT = True


_Vector: TypeAlias = tuple[float, float, float]
_IntVector: TypeAlias = tuple[int, int, int]


@dataclass(kw_only=True, frozen=True)
class Frame:

    origin: _Vector = (0.,0.,0.)
    direction: tuple[_Vector, _Vector, _Vector] = ((1.,0.,0.),(0.,1.,0.),(0.,0.,1.))


@dataclass(kw_only=True, frozen=True)
class ImageFrame(Frame):
    ''' this class encaps the size, spacing, and origin information of medical scans and segmentation masks.
    dimensions are ordered as +x, +y, +z
    on usage of this class:
        numpy arrays are ordered (+z, +y, +x) in this script, same as returned from sitk.GetArrayFromImage
        for legacy reasons, arrays decoded from AnatomicAligner bin file are ordered (-z, -y, +x), so a reversal is needed immediately on axial and coronal axes.
    '''

    size: _IntVector
    spacing: _Vector


    @classmethod
    def from_image(cls, img:sitk.Image|vtkImageData):
        if isinstance(img, sitk.Image):
            return cls(
                        size=img.GetSize(),
                        spacing=img.GetSpacing(),
                        origin=img.GetOrigin(),
                        )
        elif isinstance(img, vtkImageData):
            return cls(
                        size=img.GetDimensions(),
                        spacing=img.GetSpacing(),
                        origin=img.GetOrigin(),
                        )
        else:
            raise ValueError('cannot recognize input type')



@dataclass(kw_only=True)
class Identifier:
    '''this class handles identifiers for all SkullEngine data objects
    id is for program to find a particular object in memory
    metadata describe a particular scan and often contains sensitive data'''

    id:str = '' # for other part of program to find this image
    metadata:dict = field(default_factory=dict) # tags carried over from image file
    has_phi:bool = False

    # def __post_init__(self):
    #     # Loop through the fields
    #     for field in fields(self):
    #         # If there is a default and the value of the field is none we can assign a value
    #         if not isinstance(field.default, dataclasses._MISSING_TYPE) and getattr(self, field.name) is None:
    #             setattr(self, field.name, field.default)


    def erase_phi(self, **kw):
        # for now, delete all metadata
        self.metadata.clear()
        self.has_phi = False


    def confirm_phi(self, *, has_phi):
        self.has_phi = has_phi

        if has_phi:
            if ALLOW_PHI:
                pass

            elif CAN_ERASE_PHI_AT_INIT:
                self.erase_phi()

            else:
                raise ValueError(
                    "This program allows only non-PHI data"
                )


SkullEngineAction = tuple[str, str, list, dict] # class name or self, method name, *args, **kwargs


@dataclass(kw_only=True)
class SkullEngineData:
    
    # @property
    # def identifier(self):
    #     if not hasattr(self, '_identifier'):
    #         self._identifier = Identifier()
    #     return self._identifier
    
    
    # @property
    # def actions(self):
    #     if not hasattr(self, '_actions'):
    #         self._actions = []
    #     return self._actions
    
    
    # @property
    # def extra(self):
    #     if not hasattr(self, '_extra'):
    #         self._extra = {}
    #     return self._extra
    
    
    frame:Frame
    identifier: Identifier
    actions: list = field(default_factory=list)
    extra: dict = field(default_factory=dict) # a user defined dict


