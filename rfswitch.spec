#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	0.1
Summary:	Wireless Radio Software Switch
Name:		rfswitch
Version:	1.1
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
URL:		http://rfswitch.sourceforge.net/
Source0:	http://dl.sourceforge.net/rfswitch/%{name}-%{version}.tar.gz
# Source0-md5:	1f2233397bb95721c0f5b6d6f7868513
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project enables users to change the status of their wireless
cards' radio on laptops which do not use a hardware based wireless
radio switch.

%package -n kernel%{_alt_kernel}-misc-rfswitch
Summary:	Linux driver for rfswitch
Summary(pl.UTF-8):	Sterownik dla Linuksa do rfswitch
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-rfswitch
This is driver for rfswitch for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-misc-rfswitch -l pl.UTF-8
Sterownik dla Linuksa do rfswitch.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q
cat > rfswitch.modprobe <<EOF
# kwizart rfswitch wireless modprobe.
# Choose To uncomment Packard Bell or Averatec
# See the README for others options.
#options av5100 radio=0
#options pbe5 radio=0
EOF

%build
%if %{with kernel}
%build_kernel_modules -m rfswitch
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
cp -a rfswitch.modprobe $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/rfswitch
%endif

%if %{with kernel}
%install_kernel_modules -m rfswitch -d kernel/misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-rfswitch
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-rfswitch
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc FILES ISSUES LICENSE README
/etc/modprobe.d/rfswitch
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-rfswitch
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/misc/*.ko*
%endif
