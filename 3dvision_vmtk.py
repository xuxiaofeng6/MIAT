import vtk

def vis_stl(stl_file_path: str):
    # 加载STL文件
    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_file_path)
    reader.Update()

    # 创建渲染窗口和渲染器
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # 创建一个表示几何图形的演员对象
    actor = vtk.vtkActor()
    actor.SetMapper(vtk.vtkPolyDataMapper())
    actor.GetMapper().SetInputConnection(reader.GetOutputPort())

    # 将演员对象添加到渲染器中
    renderer.AddActor(actor)

    # 设置相机的位置和方向
    camera = renderer.GetActiveCamera()
    camera.SetPosition(0, 0, 10)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 1, 0)

    # 设置背景颜色
    renderer.SetBackground(0.2, 0.2, 0.2)

    # 打开渲染窗口
    render_window.Render()

    # 进入交互模式
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Start()

def vis_vtk(vtk_file_path: str):
    # 读取vtk文件
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(vtk_file_path)
    reader.Update()

    # 创建一个Mapper
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # 创建一个Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # 创建一个Renderer并添加Actor
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    # 创建一个RenderWindow并设置Renderer
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # 创建一个Interactor并设置RenderWindow
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # 启动Interactor
    interactor.Initialize()
    interactor.Start()