%bcond_with tests

Name:           python-pycparser
Summary:        C parser and AST generator written in Python
Version:        2.20
Release:        0
License:        BSD
URL:            https://github.com/sailfishos/python-pycparser
Source0:        %{name}-%{version}.tar.bz2
Source1:        pycparser-0.91.1-remove-relative-sys-path.py

# This is Fedora-specific; I don't think we should request upstream to
# remove embedded libraries from their distribuution, when we can remove
# them during packaging.
# It also ensures that pycparser uses the same YACC __tabversion__ as ply
# package to prevent "yacc table file version is out of date" problem.
Patch100:       pycparser-unbundle-ply.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-ply

# for unit tests
%if %{with tests}
BuildRequires:  cpp
%endif

%description
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.

%package -n python3-pycparser
Summary:        %{summary}

%description -n python3-pycparser
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

# remove embedded copy of ply
rm -r pycparser/ply

rm -rf examples

%build
%py3_build
pushd build/lib/pycparser
%{python3} _build_tables.py
popd

%install
%py3_install

%check
%if %{with tests}
%{python3} tests/all_tests.py
%endif

%files -n python3-pycparser
%license LICENSE
%{python3_sitelib}/pycparser/
%{python3_sitelib}/pycparser-*.egg-info/
