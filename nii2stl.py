import vtk
import SimpleITK as sitk

def nii2stl(nifti_file_path: str):
    """
    nifti2stl
    Args:
        nifti_file_path:

    Returns:
        None:
    """
    # Determine the file type
    file_type = None
    if '.nii.gz' in nifti_file_path:
        file_type = '.nii.gz'
    elif '.nii' in nifti_file_path:
        file_type = '.nii'
    else:
        raise TypeError('Wrong file format!')
    image_info = sitk.ReadImage(nifti_file_path)
    dims = image_info.GetSize()
    images = sitk.GetArrayFromImage(image_info)
    old_origin = image_info.GetOrigin()
    direction = image_info.GetDirection()
    spacing = image_info.GetSpacing()
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(nifti_file_path)
    reader.Update()
    # Modify information
    change = vtk.vtkImageChangeInformation()
    change.SetOutputOrigin(old_origin)
    change.SetInputData(reader.GetOutput())
    change.Update()
    image_data = change.GetOutput()
    origin = image_data.GetOrigin()
    matrix = vtk.vtkMatrix4x4()
    if origin != old_origin:
        matrix.SetElement(0, 0, direction[0])
        matrix.SetElement(0, 1, direction[1])
        matrix.SetElement(0, 2, direction[2])
        matrix.SetElement(0, 3, old_origin[0])
        matrix.SetElement(1, 0, direction[3])
        matrix.SetElement(1, 1, direction[4])
        matrix.SetElement(1, 2, direction[5])
        matrix.SetElement(1, 3, old_origin[1])
        matrix.SetElement(2, 0, direction[6])
        matrix.SetElement(2, 1, direction[7])
        matrix.SetElement(2, 2, direction[8])
        matrix.SetElement(2, 3, old_origin[2])
    else:
        matrix.SetElement(0, 0, direction[0])
        matrix.SetElement(0, 1, direction[1])
        matrix.SetElement(0, 2, direction[2])
        matrix.SetElement(0, 3, 0)
        matrix.SetElement(1, 0, direction[3])
        matrix.SetElement(1, 1, direction[4])
        matrix.SetElement(1, 2, direction[5])
        matrix.SetElement(1, 3, 0)
        matrix.SetElement(2, 0, direction[6])
        matrix.SetElement(2, 1, direction[7])
        matrix.SetElement(2, 2, direction[8])
        matrix.SetElement(2, 3, 0)
    marching_cubes = vtk.vtkImageMarchingCubes()
    marching_cubes.SetInputData(image_data)
    marching_cubes.SetValue(0, 0.6)
    marching_cubes.Update()
    transform = vtk.vtkTransform()
    transform.SetMatrix(matrix)
    transform.PostMultiply()

    trans_filter = vtk.vtkTransformPolyDataFilter()
    trans_filter.SetInputData(marching_cubes.GetOutput())
    trans_filter.SetTransform(transform)
    trans_filter.Update()

    clean = vtk.vtkCleanPolyData()
    clean.SetInputData(trans_filter.GetOutput())
    clean.Update()

    surface = clean.GetOutput()
    save_path = nifti_file_path.replace(file_type, '.stl')
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(save_path)
    writer.SetFileTypeToBinary()
    writer.SetInputData(surface)
    writer.Write()

def stl2vtk(stl_file_path: str) -> str:
    """
    Convert stl files to vtk files
    Args:
        stl_file_path:

    Returns:

    """
    # Convert stl files to vtk files
    stl_reader = vtk.vtkSTLReader()
    stl_reader.SetFileName(stl_file_path)
    stl_reader.Update()
    # Store as vtk file
    vtk_file_path = stl_file_path.replace('.stl', '_tmp.vtk')
    vtk_writer = vtk.vtkPolyDataWriter()
    vtk_writer.SetFileName(vtk_file_path)
    vtk_writer.SetInputData(stl_reader.GetOutput())
    vtk_writer.SetFileVersion(42)
    # vtk_writer.SetFileTypeToBinary()
    vtk_writer.Write()

    return vtk_file_path

def stl2image(stl_file_path: str, nifti_file_path: str, nifti_save_path: str = None):
    '''
    Convert annotated stl models to voxel
    Args:
        stl_file_path (str):stl model file path
        nifti_file_path (str):The raw nifti data corresponding to the stl model, used to extract the file header information
        nifti_save_path (str):The path to store the data after conversion, the default is the model file name

    '''

    # If the input is directly nifti, the above code can be commented out
    read = vtk.vtkNIFTIImageReader()
    read.SetFileName(nifti_file_path)
    read.Update()
    image_info = nib.load(nifti_file_path)
    # Get Origin
    affine = image_info.affine
    origin = list(affine[:, 3][:3])
    for i in range(3):
        if affine[i, i] < 0:
            origin[i] = -1 * origin[i]
    # Get spacing
    spacing = image_info.header.get_zooms()
    im_header = image_info.header
    dims = image_info.get_data().shape
    # Read model files
    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_file_path)
    reader.Update()
    surface = reader.GetOutput()
    # Convert
    whiteImage = vtk.vtkImageData()
    whiteImage.SetSpacing(spacing)
    whiteImage.SetDimensions(dims)
    whiteImage.SetExtent(0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1)
    whiteImage.SetOrigin(origin)
    whiteImage.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
    whiteImage.GetPointData().SetScalars(
        numpy_to_vtk(np.array([1] * dims[0] * dims[1] * dims[2])))
    # fill the image with foreground voxel
    pol2stenc = vtk.vtkPolyDataToImageStencil()
    pol2stenc.SetInputData(surface)
    pol2stenc.SetOutputOrigin(origin)
    pol2stenc.SetOutputSpacing(spacing)
    pol2stenc.SetOutputWholeExtent(whiteImage.GetExtent())
    pol2stenc.Update()
    # cut the corresponding white image and set the background:
    imgstenc = vtk.vtkImageStencil()
    imgstenc.SetInputData(whiteImage)
    imgstenc.SetStencilData(pol2stenc.GetOutput())
    imgstenc.ReverseStencilOff()
    imgstenc.SetBackgroundValue(0)
    imgstenc.Update()
    # dilate one pixel
    dilate = vtk.vtkImageContinuousDilate3D()
    dilate.SetKernelSize(
        2, 2,
        2)  # If KernelSize of an axis is 1, no processing is done on that axis.
    dilate.SetInputData(imgstenc.GetOutput())
    dilate.Update()
    # save image data
    if not nifti_save_path:
        nifti_save_path = stl_file_path[:-3] + 'nii.gz'
    writer = vtk.vtkNIFTIImageWriter()
    writer.SetFileName(nifti_save_path)
    writer.SetInputData(dilate.GetOutput())
    writer.SetNIFTIHeader(read.GetNIFTIHeader())
    writer.Write()

    image_info = nib.load(nifti_save_path)
    nib.save(nib.Nifti1Image(image_info.get_data(), affine, im_header),
             nifti_save_path)

nii2stl(nifti_file_path = '')