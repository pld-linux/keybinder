#
# Conditional build:
%bcond_without	lua		# don't build lua bindings
%bcond_without	python		# don't build python bindings
#
Summary:	keybinder library
Summary(pl.UTF-8):	Biblioteka keybinder
Name:		keybinder
Version:	0.3.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://kaizer.se/publicfiles/keybinder/%{name}-%{version}.tar.gz
# Source0-md5:	2a0aed62ba14d1bf5c79707e20cb4059
URL:		http://kaizer.se/wiki/keybinder/
BuildRequires:	gtk+2-devel
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	xorg-lib-libX11-devel
%if %{with lua}
BuildRequires:	lua51
BuildRequires:	lua51-devel >= 5.1
%endif
%if %{with python}
BuildRequires:	python-devel >= 2.5
BuildRequires:	python-distribute
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
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

%description devel
Header files for keybinder library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki keybinder.

%package doc
Summary:	HTML documentation for keybinder library
Summary(pl.UTF-8):	Dokumentacja w HTML biblioteki keybinder
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description doc
HTML documentation for keybinder library.

%description devel -l pl.UTF-8
Dokumentacja w HTML biblioteki keybinder.

%package -n python-keybinder
Summary:	Python bindings for keybinder library
Summary(pl.UTF-8):	Wiązania pythona biblioteki keybinder
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs
Requires:	python-modules

%description -n python-keybinder
Python bindings for keybinder library.

%description -n python-keybinder -l pl.UTF-8
Wiązania pythona biblioteki keybinder.

%package -n lua-keybinder
Summary:	Lua bindings for keybinder library
Summary(pl.UTF-8):	Wiązania lua biblioteki keybinder
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n lua-keybinder
Lua bindings for keybinder library.

%description -n lua-keybinder -l pl.UTF-8
Wiązania lua biblioteki keybinder.

%prep
%setup -q

%build
%configure \
%if %{with lua}
	--with-lua-includes=%{_includedir}/lua51 \
	--with-lua-suffix=51
%endif


%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT%{_docdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

mv $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/keybinder/ $RPM_BUILD_ROOT%{_docdir}/

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libkeybinder.so.0
%attr(755,root,root) %{_libdir}/libkeybinder.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkeybinder.so
%{_libdir}/libkeybinder.la
%{_includedir}/keybinder.h
%{_pkgconfigdir}/keybinder.pc
%{_examplesdir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/keybinder
%{_docdir}/keybinder/*[css,html,png,devhelp2]

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
