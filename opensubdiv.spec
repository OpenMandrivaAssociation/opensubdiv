%define major		3
%define libname		%mklibname opensubdiv %{major}
%define develname	%mklibname -d opensubdiv
%define staticname	%mklibname -s -d opensubdiv

%define oname	OpenSubdiv
%define _disable_lto 1
%define _disable_ld_no_undefined 1

%define use_cuda 0
%{?_with_use_cuda: %global use_cuda 1}
%{?_without_use_cuda: %global use_cuda 0}
%define underscore %(echo %{version} | sed -e "s/\\\./_/g")

Name:		opensubdiv
Version:	3.4.4
Release:	1
Summary:	High performance subdivision surface libraries
Group:		Graphics/3D
License:	Apache License
#Url:		http://graphics.pixar.com/opensubdiv/
Url:		https://github.com/PixarAnimationStudios/OpenSubdiv
Source0:	https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v%{underscore}/%{oname}-%{version}.tar.gz
Patch0:		opensubdiv-3.3.3-fix-major-soname.patch
Patch1:		OpenSubdiv-3.4.3-find-OpenCL.patch
Patch2:		opensubdiv-3.4.4-tbb.patch
BuildRequires:	cmake
BuildRequires:	make
BuildRequires:	libgomp-devel
%if %{use_cuda}
BuildRequires:	nvidia-cuda-toolkit >= 4.0
BuildRequires:	nvidia-cuda-toolkit-devel >= 4.0
%endif
BuildRequires:	pkgconfig(OpenCL) >= 1.1
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glfw3) >= 3.0.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(tbb) >= 4.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:  pkgconfig(xxf86vm)
#BuildRequires:	ptex >= 2.0
# for doc building
BuildRequires:	doxygen >= 1.8.4
# FIXME documentation/*.py needs to be ported to 3.x
BuildRequires:	python2
BuildRequires:	python2dist(docutils)

%description 
OpenSubdiv is a set of open source libraries that implement high
performance subdivision surface (subdiv) evaluation on massively
parallel CPU and GPU architectures. This code path is optimized for
drawing deforming surfaces with static topology at interactive
frame rates.

OpenSubdiv is an API ready to be integrated into 3rd party digital
content creation tools. It is not an application, nor a tool that can
be used directly to create digital assets.

%package doc
Summary:	High performance subdivision surface libraries
Group:		Documentation
BuildArch:	noarch

%description doc
OpenSubdiv is a set of open source libraries that implement high
performance subdivision surface (subdiv) evaluation on massively
parallel CPU and GPU architectures. This code path is optimized for
drawing deforming surfaces with static topology at interactive
frame rates.

This package includes the documentation of OpenSubdiv.

%package -n %{libname}
Summary:	High performance subdivision surface libraries
Group:		System/Libraries
Requires:	%{_lib}glfw3 >= 3.0

%description -n %{libname}
OpenSubdiv is a set of open source libraries that implement high
performance subdivision surface (subdiv) evaluation on massively
parallel CPU and GPU architectures. This code path is optimized for
drawing deforming surfaces with static topology at interactive
frame rates.

OpenSubdiv is an API ready to be integrated into 3rd party digital
content creation tools. It is not an application, nor a tool that can
be used directly to create digital assets.

This package contains the shared library of OpenSubdiv.

%package -n %{develname}
Summary:	Development files for the OpenSubdiv library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	opensubdiv-devel = %{version}-%{release}

%description -n %{develname}
Development files for the OpenSubdiv library. Install this package if you
want to compile applications using the OpenSubDiv library.

%package -n %{staticname}
Summary:	Static libraries for linking to OpenSubdiv
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static = %{version}-%{release}
Provides:	opensubdiv-static-devel = %{version}-%{release}

%description -n %{staticname}
Static libraries for OpenSubdiv.


%prep
%autosetup -p1 -n OpenSubdiv-%{underscore}

%build
# Fix for aarch64. With Clang 10: "/usr/include/tbb/tbb_machine.h:338:6: error: Unsupported machine word size.
# #error Unsupported machine word size."
# Quick solution - use GCC.

%ifarch aarch64
export CC=gcc
export CXX=g++
%endif

export CFLAGS="%{optflags} -fopenmp"
export CXXFLAGS="%{optflags} -fopenmp"

%cmake	\
	-DBUILD_STATIC_LIBS:BOOL=ON \
	-DCMAKE_LIBDIR_BASE:PATH=%{_libdir} \
	-DGLEW_LOCATION:PATH=%{_prefix} \
	-DGLFW_LOCATION:PATH=%{_prefix} \
	-DNO_CLEW:BOOL=ON \
%if %{use_cuda}
	-DNO_CUDA:BOOL=OFF \
	-DOSD_CUDA_NVCC_FLAGS:STRING="--gpu-architecture=compute_30" \
%else
	-DNO_CUDA:BOOL=ON \
%endif
	-DNO_GLFW:BOOL=OFF \
	-DNO_EXAMPLES:BOOL=ON \
	-DNO_METAL:BOOL=ON \
	-DNO_OMP:BOOL=OFF \
	-DNO_OPENCL:BOOL=OFF \
	-DNO_PTEX:BOOL=ON \
	-DNO_REGRESSION:BOOL=ON \
	-DNO_TUTORIALS:BOOL:=ON

if [ "$?" != "0" ]; then
	cat CMakeFiles/CMakeOutput.log
	exit 1
fi

%make_build
cd ..

%install
%make_install -C build
rm -f %{buildroot}%{_bindir}/stringify

%files doc
%{_datadir}/doc/%{name}

%files -n %{libname}
%doc LICENSE.txt NOTICE.txt README.md
%{_libdir}/*.so.%{major}{,.*}

%files -n %{develname}
%{_libdir}/lib*.so
%{_includedir}/*

%files -n %{staticname}
%{_libdir}/*.a
