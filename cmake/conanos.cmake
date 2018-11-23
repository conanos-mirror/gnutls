

#
# Use Conan.io
#
if(USE_CONAN_IO)
    include(conanbuildinfo.cmake)
    conan_basic_setup()
    conan_define_targets()
endif()

if(MSVC)   
  if(CMAKE_GENERATOR MATCHES Win64)
    set(__arch__ x86_64)
  else()
    set(__arch__ x86)
  endif()
  
  add_definitions(-D_CRT_SECURE_NO_WARNINGS)
  add_definitions(/wd4018)
  add_definitions(/wd4273)
  add_definitions(/wd4090)
  add_definitions(/wd4013)
  add_definitions(/wd4244)
  add_definitions(/wd4311)
  add_definitions(/wd4267)
  add_definitions(/wd5999)
  add_definitions(/wd4146)
  add_definitions(/wd4819)
  add_definitions(/wd4101)
  add_definitions(/wd4334)
  
endif()




function(assign_source_group)
    foreach(_source IN ITEMS ${ARGN})
        if (IS_ABSOLUTE "${_source}")
            file(RELATIVE_PATH _source_rel "${CMAKE_CURRENT_SOURCE_DIR}" "${_source}")
        else()
            set(_source_rel "${_source}")
        endif()
        get_filename_component(_source_path "${_source_rel}" PATH)
        string(REPLACE "/" "\\" _source_path_msvc "${_source_path}")
        source_group("${_source_path_msvc}" FILES "${_source}")
    endforeach()
endfunction(assign_source_group)

