%global project ovn-kubernetes
%global commit         ddb1c2ab55a295468c235993d871f70351312aa9
%global shortcommit    %(c=%{commit}; echo ${c:0:7})
%global repo %{project}
%global debug_package %{nil}

# some distros (e.g: RHEL-7) don't define _rundir macro yet
# Fedora 15 onwards uses /run as _rundir
%if 0%{!?_rundir:1}
%define _rundir /run
%endif

# define the python package prefix based on distribution version so that we can
# simultaneously support RHEL-based and later Fedora versions in this spec file.
%if 0%{?fedora} >= 25
%define _py2 python2
%endif

%if 0%{?rhel} || 0%{?fedora} < 25
%define _py2 python
%endif

Name: openvswitch-%{project}
Summary: Open Virtual Networking Kubernetes Wedge
URL: http://www.github.com/openvswitch/ovn-kubernetes
Version: 0.1.0
Release: 1%{?dist}

License: ASL 2.0
Source0: https://github.com/openvswitch/%{repo}/archive/%{commit}/%{repo}-git%{shortcommit}.tar.gz
ExclusiveArch: x86_64

BuildRequires: %{_py2}-devel
%if 0%{?fedora} > 22 || %{with build_python3}
BuildRequires: python3-devel
%endif
BuildRequires: golang >= 1.8.1

%description
This allows kubernetes to use Open Virtual Networking (OVN)

%prep
%setup -q -n %{repo}-%{commit}

%build
cd go-controller && make
strip _output/go/bin/ovnkube
strip _output/go/bin/ovn-kube-util
strip _output/go/bin/ovn-k8s-overlay
strip _output/go/bin/ovn-k8s-cni-overlay

%install
install -d -m 0750 %{buildroot}%{_bindir}
install -d -m 0750 %{buildroot}%{_libexecdir}
install -p -m 755 go-controller/_output/go/bin/ovnkube %{buildroot}%{_bindir}
install -p -m 755 go-controller/_output/go/bin/ovn-kube-util %{buildroot}%{_bindir}
install -p -m 755 go-controller/_output/go/bin/ovn-k8s-overlay %{buildroot}%{_bindir}
install -p -m 755 go-controller/_output/go/bin/ovn-k8s-cni-overlay %{buildroot}%{_libexecdir}
install -d -m 0750 %{buildroot}/etc/openvswitch
install -p -m 644 go-controller/etc/ovn_k8s.conf %{buildroot}/etc/openvswitch
install -d -m 0750 %{buildroot}%{_mandir}/man1
install -p -m 644 docs/ovnkube.1 %{buildroot}%{_mandir}/man1
install -p -m 644 docs/ovn-kube-util.1 %{buildroot}%{_mandir}/man1
install -p -m 644 docs/ovn-k8s-overlay.1 %{buildroot}%{_mandir}/man1

%files
%defattr(-,root,root)
%license COPYING
%doc CONTRIBUTING.md README.md
%doc docs/config.md  docs/debugging.md  docs/INSTALL.K8S.md  docs/INSTALL.SSL.md  docs/INSTALL.UBUNTU.md
%{_mandir}/man1/ovnkube.1.*
%{_mandir}/man1/ovn-kube-util.1.*
%{_mandir}/man1/ovn-k8s-overlay.1.*
%{_bindir}/ovnkube
%{_bindir}/ovn-kube-util
%{_bindir}/ovn-k8s-overlay
%{_libexecdir}/ovn-k8s-cni-overlay
%config(noreplace) %{_sysconfdir}/openvswitch/ovn_k8s.conf

%changelog
* Fri Jan 12 2018 Phil Cameron <pcameron@redhat.com> - 0.1.0-1
- Initial package for Fedora

