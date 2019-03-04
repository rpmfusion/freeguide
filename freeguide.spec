Name:           freeguide
Version:        0.11.1
Release:        6%{?dist}
Summary:        A TV Guide

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://www.artificialworlds.net/freeguide/Main/HomePage
Source0:        http://downloads.sourceforge.net/freeguide-tv/freeguide-%{version}.tar.gz
Source1:        freeguide.desktop
# completely disable the automatic check for updates
Patch0:         0001-disable-check-for-updates.patch
BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  javapackages-tools
BuildRequires:  ant
BuildRequires:  desktop-file-utils

Requires:       java >= 1:1.6.0
Requires:       javapackages-tools
Requires:       xmltv xmltv-gui

%description
FreeGuide is a TV guide program. It uses parser programs to extract TV
information from web pages and stores them for viewing without the need to
connect to the Internet. The viewer allows the user to view television listings
and create customized TV guides by selecting programs and by building up a
favorites list.

It works with listings for many countries.  Check the web site
freeguide-tv.sf.net for details.


%prep
%setup -q
%patch0 -p1

find . -name '*.jar' -exec rm -f '{}' \;

rm -rf xmltv

%build
ant jar


%install
ant -Dinstall_bin_dir=%{buildroot}/%{_bindir} \
    -Dinstall_share_dir=%{buildroot}/%{_datadir} \
    -Dinstall_doc_dir=%{buildroot}/%{_defaultdocdir}/%{name} \
    -Dinstall_real_dir=%{_datadir}/freeguide \
    -Dinstall_real_doc_dir=%{_defaultdocdir}/%{name} \
    install

install -d -m 0755 %{buildroot}%{_javadir}/%{name}
for jar in $(find %{buildroot}%{_datadir}/%{name} -type f -name '*.jar'); do
    mv ${jar} %{buildroot}%{_javadir}/%{name}
    ln -s %{_javadir}/%{name}/$(basename ${jar}) ${jar}
done

#rm -rf %{buildroot}%{_defaultdocdir}/%{name}

desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

%files
%defattr(0644,root,root,0755)
%doc doc-bin/*
%license doc/COPYING
%attr(0755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_javadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/*


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jul 24 2016 Sérgio Basto <sergio@serjux.com> - 0.11.1-1
- Update freeguide to 0.11.1
- Drop ant-nodeps dependency as it's long been provided by ant based on:
  https://lists.fedoraproject.org/pipermail/scm-commits/Week-of-Mon-20130429/1007603.html
- Depend on javapackages-tools instead of jpackage-utils to conform to new Java
  guidelines
- Modernize spec, add license tag

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.11-3
- Mass rebuilt for Fedora 19 Features

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 23 2010 Iain Arnell <iarnell@gmail.com> 0.11-1
- update to latest upstream version
- remove no-jalopy-retroweaver patch
- rebase disable-check-for-updates patch
- Americanize spelling in description

* Fri Dec 11 2009 Iain Arnell <iarnell@gmail.com> 0.10.12-1
- update to latest upstream version

* Sun Sep 13 2009 Iain Arnell <iarnell@gmail.com> 0.10.10-1
- initial packaging

