%global libcurl_version 7.52.0

%undefine __cmake_in_source_build

%if 0%{?rhel}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif

%global dnf_conflict 2.8.8

Name:           librepo
Version:        1.14.2
Release:        4%{?dist}
Summary:        Repodata downloading library

License:        LGPLv2+
URL:            https://github.com/rpm-software-management/librepo
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0001:      0001-Use-nanosec-precision-for-timestamp-of-checksum-cach.patch
Patch0002:      0002-Fix-alloc-free-mismatches-from-covscan.patch
Patch0003:      0003-More-covscan-fixes.patch
Patch0004:      0004-Use-g_strdup_vprintf-instead-of-manually-calculating.patch
Patch0005:      0005-Use-g_list_free_full-to-free-LRMetadataTarget-err.patch
Patch0006:      0006-Detailed-error-message-when-using-non-existing-TMPDI.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check-devel
BuildRequires:  doxygen
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  gpgme-devel
BuildRequires:  libattr-devel
BuildRequires:  libcurl-devel >= %{libcurl_version}
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(openssl)
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= 0.9.11
%endif
Requires:       libcurl%{?_isa} >= %{libcurl_version}

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for librepo.

%package -n python3-%{name}
Summary:        Python 3 bindings for the librepo library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-gpg
BuildRequires:  python3-pyxattr
BuildRequires:  python3-requests
BuildRequires:  python3-sphinx
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Obsoletes Fedora 27 package
Obsoletes:      platform-python-%{name} < %{version}-%{release}
Conflicts:      python3-dnf < %{dnf_conflict}

%description -n python3-%{name}
Python 3 bindings for the librepo library.

%prep
%autosetup -p1

%build
%cmake %{!?with_zchunk:-DWITH_ZCHUNK=OFF}
%cmake_build

%check
%ctest

%install
%cmake_install

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%{python3_sitearch}/%{name}/

%changelog
* Mon Sep 12 2022 Lukas Hrazky <lhrazky@redhat.com> - 1.14.2-4
- Fix termination of va_list in lr_metadatatarget_append_error()
- Detailed error message when using non-existing TMPDIR

* Mon Jul 25 2022 Lukas Hrazky <lhrazky@redhat.com> - 1.14.2-3
- Fix covscan issues

* Tue Jul 12 2022 Lukas Hrazky <lhrazky@redhat.com> - 1.14.2-2
- Use nanosec precision for timestamp of checksum cache

* Tue Nov 09 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 1.14.2-1
- Update to 1.14.2
- Reduce time to load metadata
- Fix resource leaks and memory leaks
- Remove build dependency on python3-flask

* Fri Jun 25 2021 Marek Blaha <mblaha@redhat.com> - 1.14.0-2
- Recover from fsync fail on read-only filesystem (RhBug:1956361)

* Fri Apr 30 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 1.14.0-1
- Update to 1.14.0
- Fix the key string parsing in url_substitution
- When zchunk enabled and not using HTTP/S protocol, download the whole file (RhBug:1886706)
- Add an option LRO_SSLVERIFYSTATUS to check TLS certificate revocation status (using OCSP stapling) (RhBug:1814383)
- Fix: lr_perform() - Avoid 100% CPU usage
- Add support for working with certificates used with proxy
- Reposync does not re-download unchanged packages (RhBug:1931904)
- Fix memory leaks

* Tue Dec 15 2020 Marek Blaha <mblaha@redhat.com> - 1.12.0-3
- Add support for pkcs11 certificate and key for repository authorization (RhBug:1859495)

* Mon Aug 17 2020 Ales Matej <amatej@redhat.com> - 1.12.0-2
- Validate paths read from repomd.xml (RhBug:1866505)

* Wed Jun 03 2020 Nicola Sella <nsella@redhat.com> - 1.12.0-1
- Update to 1.12.0
- Decode package URL when using for local filename (RhBug:1817130)
- Fix memory leak in lr_download_metadata() and lr_yum_download_remote()
- Download sources work when at least one of specified is working (RhBug:1775184)
- Enable building on OSX

* Fri Apr 03 2020 Ales Matej <amatej@redhat.com> - 1.11.3-1
 - Update to 1.11.3
 - Prefer mirrorlist/metalink over baseurl (RhBug:1775184)
 - Fix calling Python API without holding GIL (RhBug:1788918) 
 - Do not unref LrErr_Exception on exit (RhBug:1778854) 

* Fri Dec 06 2019 Lukas Hrazky <lhrazky@redhat.com> - 1.11.0-2
 - Create a directory for gpg sockets in /run/user/ (RhBug:1769831,1771012)

* Tue Nov 12 2019 Ales Matej <amatej@redhat.com> - 1.11.0-1
 - Update to 1.11.0
 - Retry mirrorlist/metalink downloads several times (RhBug:1741931)
 - Improve variable substitutions in URLs and add ${variable} support 

* Tue Oct 22 2019 Ales Matej <amatej@redhat.com> - 1.10.6-1
- Update to 1.10.6
- Imporove handling of xattr to re-download damadged files (RhBug:1690894)
- Rephrase repository GPG check error message (RhBug:1741442)
- Add sleep before next try when all mirrors were tried (RhBug:1741931)
- Raise logging level of error messages (RhBug:1737709)
- Handle webservers that don't support ranges when downloading zck
- Define LRO_SUPPORTS_CACHEDIR only with zchunk (RhBug:1726141)
- Allow to use mirrors multiple times for a target (RhBug:1678588)
- Allow to try baseurl multiple times (RhBug:1678588)

* Fri Sep 06 2019 Marek Blaha <mblaha@redhat.com> - 1.10.3-3
- Backport patch: Fix: Verification of checksum from file attr

* Wed Jul 31 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.10.3-2
- Backport patch: Define LRO_SUPPORTS_CACHEDIR only with zchunk (RhBug:1726141,1719830)

* Tue Jun 11 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.10.3-1
- Update to 1.10.3
- Exit gpg-agent after repokey import (RhBug:1650266)

* Mon May 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.10.1-1
- Update to 1.10.1
- Reduce download delays
- Add an option to preserve timestamps of the downloaded files (RhBug:1688537)
- Append the '?' part of repo URL after the path
- Fix memory leaks

* Tue Sep 25 2018 Jaroslav Mracek <jmracek@redhat.com> - 1.9.2-1
- Update to 1.9.2
- Bug 1626495 - major performance regression with libcurl-7.61.1

* Mon Aug 13 2018 Daniel Mach <dmach@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jaroslav Mracek <jmracek@redhat.com> - 1.9.0-3
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.0-2
- Fix ldconfig_scriptlets once more

* Tue Jun 26 2018 Jaroslav Mracek <jmracek@redhat.com> - 1.9.0-1
- Update to 1.9.0

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-9
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-8
- Bootstrap for Python 3.7

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-7
- Add if conditionals around pyxattr

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.8.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-5
- Switch to %%ldconfig_scriptlets

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-4
- Use better Obsoletes for platform-python

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-3
- Fix typo in Obsoletes

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-2
- Remove platform-python subpackage

* Fri Sep 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Fri Sep 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.0-2
- Disable platform python on old releases

* Wed Aug 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Fri Aug 18 2017 Tomas Orsava <torsava@redhat.com> - 1.7.20-9
- Added Patch 0 to fix a tearDown failure in the test suite

* Thu Aug 10 2017 Petr Viktorin <pviktori@redhat.com> - 1.7.20-8
- Add subpackage for platform-python (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.7.20-4
- Enable tests

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.7.20-3
- Rebuild for Python 3.6
- Disable tests for now

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.20-2
- Rebuild for gpgme 1.18

* Thu Aug 25 2016 Tomas Mlcoch <tmlcoch@redhat.com> - 1.7.20-1
- Tests: Disable test_download_packages_with_resume_02 test
- Update build utils to match new fedora spec schema

* Wed Aug 24 2016 Tomas Mlcoch <tmlcoch@redhat.com> - 1.7.19-1
- Add yumrecord substitution mechanism (mluscon)
- Fix a memory leak in signature verification (cwalters)

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.7.18-4
- Add %%{?system_python_abi}
- Trim ton of changelog

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.18-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.7.18-2
- Adopt to new packaging guidelines
- Cleanups in spec file

* Fri Mar  4 2016 Tomas Mlcoch <tmlcoch@redhat.com> - 1.7.18-1
- Add new option LRO_FTPUSEEPSV
- Update AUTHORS
- downloader prepare_next_transfer(): simplify long line
- downloader prepare_next_transfer(): add missing error check
- downloader prepare_next_transfer(): cleanup error path
- downloader prepare_next_transfer() - fix memory leak on error path (Alan Jenkins)
- handle: Don't use proxy cache for downloads of metalink/mirrorlist
- handle: Don't set CURLOPT_HTTPHEADER into curl handle immediately when specified
- downloader: Implement logic for no_cache param in LrDownloadTarget (RhBug: 1297762)
- Add no_cache param to LrDownloadTarget and lr_downloadtarget_new()
- New test: always try to download from the fastest mirror (Alexander Todorov)
- Doc: Fixed minor doc typo (Philippe Ombredanne)
- Doc: Other updates
- Doc: Update default values in doc to reflect reality
