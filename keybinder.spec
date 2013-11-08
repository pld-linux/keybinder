#
# Conditional build:
%bcond_without	lua		# don't build Lua bindings
%bcond_without	python		# don't build Python bindings
%bcond_without	static_libs	# static library build
#
Summary:	keybinder library
Summary(pl.UTF-8):	Biblioteka keybinder
Name:		keybinder
Version:	0.3.0
Release:	4
License:	GPL v2
Group:		Libraries
Source0:	http://kaizer.se/publicfiles/keybinder/%{name}-%{version}.tar.gz
# Source0-md5:	2a0aed62ba14d1bf5c79707e20cb4059
URL:		http://kaizer.se/wiki/keybinder/
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	gtk+2-devel >= 2:2.20
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
%if %{with lua}
BuildRequires:	lua51 >= 5.1
BuildRequires:	lua51-devel >= 5.1
%endif
%if %{with python}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-distribute
BuildRequires:	python-pygobject-devel >= 2.15.3
BuildRequires:	python-pygtk-devel >= 2:2.12
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
keybinder is a library for registering global keyboard shortcuts.
Keybinder works with GTK-based applications using the X Window System.

%description -l pl.UTF-8
keybinder jest biblioteką umożliwiającą rejestrowanie globalnych
skrótów klawiszowych. Działa z aplikacjami opartymi na GTK.

%package devel
Summary:	Header files for keybinder library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki keybinder
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.20

%description devel
Header files for keybinder library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki keybinder.

%package static
Summary:	Static keybinder library
Summary(pl.UTF-8):	Statyczna biblioteka keybinder
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static keybinder library.

%description static -l pl.UTF-8
Statyczna biblioteka keybinder.

%package doc
Summary:	HTML documentation for keybinder library
Summary(pl.UTF-8):	Dokumentacja w HTML biblioteki keybinder
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
HTML documentation for keybinder library.

%description devel -l pl.UTF-8
Dokumentacja w HTML biblioteki keybinder.

%package -n python-keybinder
Summary:	Python bindings for keybinder library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki keybinder
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs
Requires:	python-modules
Requires:	python-pygobject >= 2.15.3
Requires:	python-pygtk-gtk >= 2:2.12

%description -n python-keybinder
Python bindings for keybinder library.

%description -n python-keybinder -l pl.UTF-8
Wiązania Pythona do biblioteki keybinder.

%package -n lua-keybinder
Summary:	Lua bindings for keybinder library
Summary(pl.UTF-8):	Wiązania języka Lua do biblioteki keybinder
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n lua-keybinder
Lua bindings for keybinder library.

%description -n lua-keybinder -l pl.UTF-8
Wiązania języka Lua do biblioteki keybinder.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir} \
%if %{with lua}
	--with-lua-includes=%{_includedir}/lua51 \
	--with-lua-suffix=51
%endif


%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/keybinder/*.la
%{?with_static_libs:%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/keybinder/*.a}
%endif

%if %{with lua}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lua/*/*.la
%{?with_static_libs:%{__rm} $RPM_BUILD_ROOT%{_libdir}/lua/*/*.a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %ghost %{_libdir}/libkeybinder.so.0
%attr(755,root,root) %{_libdir}/libkeybinder.so.*.*.*
%{_libdir}/girepository-1.0/Keybinder-0.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkeybinder.so
%{_libdir}/libkeybinder.la
%{_datadir}/gir-1.0/Keybinder-0.0.gir
%{_includedir}/keybinder.h
%{_pkgconfigdir}/keybinder.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libkeybinder.a
%endif

%files doc
%defattr(644,root,root,755)
%{_gtkdocdir}/keybinder

%if %{with python}
%files -n python-keybinder
%defattr(644,root,root,755)
%dir %{py_sitedir}/keybinder
%{py_sitedir}/keybinder/*.py[co]
%attr(755,root,root) %{py_sitedir}/keybinder/_keybinder.so
%endif

%if %{with lua}
%files -n lua-keybinder
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lua/5.1/keybinder.so
%endif
