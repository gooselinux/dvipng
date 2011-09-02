Name:           dvipng
Version:        1.11
Release:        3.2%{?dist}
Summary:        Converts DVI files to PNG/GIF format

Group:          Applications/Publishing 
License:        GPLv2+ and OFSFDL
URL:            http://savannah.nongnu.org/projects/dvipng/
Source0:        http://download.savannah.gnu.org/releases/dvipng/%{name}-%{version}.tar.gz
Patch0:         dvipng-CVE-2010-0829-multiple-array-indexing-errors.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  kpathsea-devel gd-devel zlib-devel libpng-devel texinfo-tex
BuildRequires:  t1lib-devel freetype-devel

Requires(pre):  /sbin/install-info 
Requires(post): /sbin/install-info

%description
This program makes PNG and/or GIF graphics from DVI files as obtained
from TeX and its relatives.

It is intended to produce anti-aliased screen-resolution images as
fast as is possible. The target audience is people who need to generate
and regenerate many images again and again. 

%prep
%setup -q
%patch0 -p1 -b .CVE-2010-0829

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

rm -rf $RPM_BUILD_ROOT/%{_infodir}/dir

for i in ChangeLog ChangeLog.0 ; do
    iconv -f ISO-8859-1 -t UTF8 $i > $i.utf8 && touch -r $i $i.utf8 && mv $i.utf8 $i
done

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/install-info %{_infodir}/dvipng.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ "$1" = "0" ] ; then 
   /sbin/install-info --delete %{_infodir}/dvipng.info %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog ChangeLog.0 README RELEASE
%{_bindir}/dvigif
%{_bindir}/dvipng
%{_infodir}/dvipng.info*
%{_mandir}/man1/dvigif.1*
%{_mandir}/man1/dvipng.1*

%changelog
* Tue Apr 27 2010 Jindrich Novy <jnovy@redhat.com> - 1.11-3.2
- fix multiple array indexing overflows CVE-2010-0829 (#585191)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.11-3.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.11-1
- Update to version 1.11

* Sun Feb  3 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.9-50
- Remove kpathsea Requires
- Add OFSFDL license tag
- Make INSTALL use install -p
- Preserve time stamp of ChangeLog and ChangeLog.0 files
- Use globbing in filelist
- Remove .gz from the end of filenames in install-info commands
- Bump release to 50 to fix up upgrade path from current dvipng package from texlive

* Sun Feb  3 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.9-2
- Install dvigif info file
- Add Provides for dvigif

* Sun Feb  3 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.9-1
- Initial package
