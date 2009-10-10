Name:           freeguide
Version:        0.10.10
Release:        1%{?dist}
Summary:        A TV Guide

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://www.artificialworlds.net/freeguide/Main/HomePage
Source0:        http://downloads.sourceforge.net/freeguide-tv/freeguide-%{version}.tar.gz
Source1:        freeguide.desktop
# upstream uses jalopy to format sources and retroweaver to allow 1.5 code to
# run on 1.4 jre; we don't need (or have) either, so patch them away
Patch0:         no-jalopy-retroweaver.patch
# completely disable the automatic check for updates
Patch1:         disable-check-for-updates.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  tagsoup
BuildRequires:  desktop-file-utils

Requires(post): jpackage-utils
Requires(post): tagsoup

Requires:       java >= 1:1.6.0
Requires:       jpackage-utils
Requires:       tagsoup
Requires:       xmltv-gui

%description
FreeGuide is a TV guide program. It uses parser programs to extract TV
information from web pages and stores them for viewing without the need to
connect to the Internet. The viewer allows the user to view television listings
and create customised TV guides by selecting programmes and by building up a
favourites list.

It works with listings for many countries.  Check the web site
freeguide-tv.sf.net for details.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

find . -name '*.jar' -exec rm -f '{}' \;
build-jar-repository -s -p lib tagsoup

rm -rf xmltv

%build
ant jars-lin


%install
rm -rf %{buildroot}
ant -Dinstall_bin_dir=%{buildroot}/%{_bindir} \
    -Dinstall_share_dir=%{buildroot}/%{_datadir} \
    -Dinstall_doc_dir=%{buildroot}/%{_defaultdocdir}/%{name}-%{version} \
    -Dinstall_real_dir=%{_datadir}/freeguide \
    -Dinstall_real_doc_dir=%{_defaultdocdir}/%{name}-%{version} \
    install-linux

rm %{buildroot}%{_datadir}/%{name}/lib/tagsoup.jar

install -d -m 0755 %{buildroot}%{_javadir}/%{name}
for jar in $(find %{buildroot}%{_datadir}/%{name} -type f -name '*.jar'); do
    mv ${jar} %{buildroot}%{_javadir}/%{name}
    ln -s %{_javadir}/%{name}/$(basename ${jar}) ${jar}
done

rm -f %{buildroot}%{_datadir}/%{name}/lib/docs.zip

desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

%clean
rm -rf %{buildroot}


%post
build-jar-repository -s -p %{_datadir}/%{name}/lib tagsoup
exit 0


%files
%defattr(0644,root,root,0755)
%doc doc/COPYING doc/html-local/*
%attr(0755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_javadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/*


%changelog
* Sun Sep 13 2009 Iain Arnell <iarnell@gmail.com> 0.10.10-1
- initial packaging

