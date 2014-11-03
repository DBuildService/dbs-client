Name:           dbs-client
Version:        0.1
Release:        1%{?dist}

Summary:        Client tool / library for DBuildService
Group:          Development Tools
License:        BSD
URL:            https://github.com/orgs/DBuildService/dbs-client
Source0:        http://github.srcurl.net/DBuildService/%{name}/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
Client tool / library for DBuildService


%prep
%setup -q


%build
# build python package
%{__python} setup.py build


%install
# install python package
%{__python} setup.py install --skip-build --root %{buildroot}


%files
%doc README.md LICENSE
%{_bindir}/dbs-client
%{python_sitelib}/dbs_client
%{python_sitelib}/dbs_client-%{version}-py2.*.egg-info


%changelog
* Mon Nov 03 2014 Jakub Dorňák <jdornak@redhat.com> 0.1-1
- new package built with tito

* Sun Nov  2 2014 Jakub Dorňák <jdornak@redhat.com> - 0.1-1
- Initial package

