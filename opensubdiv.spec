%define major		3
%define libname		%mklibname opensubdiv %{major}
%define develname	%mklibname -d opensubdiv
%define staticname	%mklibname -s -d opensubdiv

%define	ver    3.3.3
%define fver   3_3_3
%define _disable_lto 1

%define use_cuda 0
%{?_with_use_cuda: %global use_cuda 1}
%{?_without_use_cuda: %global use_cuda 0}

Name:		opensubdiv
Version:	%{ver}
Release:	%mkrel 6
Summary:	High performance subdivision surface libraries
Group:		Graphics/3D
License:	Apache License
#Url:		http://graphics.pixar.com/opensubdiv/
Url:		https://github.com/PixarAnimationStudios/OpenSubdiv
Source0:	https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v%{fver}/%{name}-%{version}.tar.gz
Patch0:		opensubdiv-3.3.3-fix-major-soname.patch
BuildRequires:	cmake
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
#BuildRequires:	ptex >= 2.0
# for doc building
BuildRequires:	doxygen >= 1.8.4
BuildRequires:	python-docutils

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
Requires:	%{_lib}tbb2 >= 4.0
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
%setup -q -n OpenSubdiv-%{fver}
%patch0 -p1 -b .major

%build
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


%changelog
* Fri Apr 26 2019 ghibo <ghibo> 3.3.3-6.mga7
+ Revision: 1395556
- Add flags for building with cuda

* Fri Apr 26 2019 ghibo <ghibo> 3.3.3-5.mga7
+ Revision: 1395451
- Add xinerama to BR
- Add xcursor to BR
- Add xrandr to BR
- Rebuild against GLFW 3.3.

* Wed Apr 24 2019 ghibo <ghibo> 3.3.3-4.mga7
+ Revision: 1395119
- Split doc package

* Wed Apr 24 2019 ghibo <ghibo> 3.3.3-3.mga7
+ Revision: 1395108
- Add ICE to BR.
- Add rst2html to BR for docs.

* Tue Apr 23 2019 ghibo <ghibo> 3.3.3-2.mga7
+ Revision: 1395047
- Add missed libgomp-devel in BuildRequires
- Fix typo in description.
- Use PATH type for cmake arguments.

* Tue Apr 23 2019 ghibo <ghibo> 3.3.3-1.mga7
+ Revision: 1395008
- fix soname adding Patch1 (credits to David Geiger)
- fix libpath for 64bit (David Geiger)
- removed CMAKE_BUILD_TYPE=Release (David Geiger)
- removed %%clean section (David Geiger)
- remove trailing dot in Summary (kekePower)
- add docs
- Added a fix for aarch64
- Add xi to BuildRequires
- imported package opensubdiv


* Tue Apr 23 2019 ghibo <ghibo> 3.3.3-1.mga7
- Initial release.
