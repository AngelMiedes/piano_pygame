import cx_Freeze
 
executables = [cx_Freeze.Executable("05_piano.py")]
 
build_exe_options = {"packages": ["pygame", "sys", "os", "random"],
                     "include_files":["images", "sounds"]}
 
cx_Freeze.setup(
    name = "Aprende Piano",
    version = "1.0",
    description = "Juego notas musicales",
    options={"build_exe": build_exe_options},
    executables = executables
    )