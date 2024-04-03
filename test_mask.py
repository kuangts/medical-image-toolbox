from vtkmodules.vtkIOImage import vtkNIFTIImageReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkImageMapper,
    vtkActor,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkInteractorStyle
)
# from vtkmodules.vtkRenderingImage import vtkImageResliceMapper
from vtkmodules.vtkImagingCore import vtkImageResliceToColors
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage

#_______________________#
# crash without following lines
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
#_______________________#

def main():

    reader = vtkNIFTIImageReader()
    reader.SetFileName(r'C:\\data\\pre-post-paired-40-send-1122\\n0002\\20100921-pre.nii.gz')
    reader.Update()
    img = reader.GetOutput()

    mapper = vtkImageSliceMapper()
    mapper.SetOrientationToY()
    mapper.SetSliceNumber(100)
    mapper.SetInputConnection(reader.GetOutputPort())

    image_slice = vtkImageSlice()
    image_slice.SetMapper(mapper)

    renderer = vtkRenderer()
    renderer.AddViewProp(image_slice)
    renderer.SetBackground(.67, .93, .93)

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(960, 960)
    render_window.SetWindowName('')

    style = vtkInteractorStyleImage()
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.SetInteractorStyle(style)

    render_window.Render()
    renderer.ResetCamera()
    interactor.Initialize()
    interactor.Start()


if __name__ == '__main__':
    main()