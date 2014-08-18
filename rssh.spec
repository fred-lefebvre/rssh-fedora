Name:           rssh
Version:        2.3.4
Release:        5%{?dist}
Summary:        Restricted shell for use with OpenSSH, allowing only scp and/or sftp
Group:          Applications/Internet
License:        BSD 
URL:            http://www.pizzashack.org/rssh/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz.sig
Patch0:         rssh-2.3.4-makefile.patch
Patch1:         rssh-2.3.4-rsync-protocol.patch
Patch2:         rssh-2.3.4-command-line-error.patch

BuildRequires:  openssh-server, openssh-clients
BuildRequires:  cvs rsync rdist
Requires:       openssh-server
Requires(pre):  shadow-utils

%description
rssh is a restricted shell for use with OpenSSH, allowing only scp
and/or sftp. For example, if you have a server which you only want
to allow users to copy files off of via scp, without providing shell
access, you can use rssh to do that. It is a alternative to scponly. 


%prep
%setup -q
%patch0 -p1 -b .makefile
%patch1 -p1 -b .rsync3
%patch2 -p1 -b .cmdline-error

chmod 644 conf_convert.sh
chmod 644 mkchroot.sh


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}
# since rssh 2.3.4, default config is installed as rssh.conf.default,
# rename it for packaging in rpm
mv %{buildroot}/%{_sysconfdir}/rssh.conf{.default,}

%clean
rm -rf %{buildroot}

%pre
getent group rsshusers >/dev/null || groupadd -r rsshusers
exit 0


%files
%doc AUTHORS ChangeLog CHROOT COPYING NEWS README SECURITY TODO
%doc conf_convert.sh mkchroot.sh
%doc %{_mandir}/man1/rssh.1*
%doc %{_mandir}/man5/rssh.conf.5*
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(750, root, rsshusers) %{_bindir}/rssh
%attr(4750, root, rsshusers) %{_libexecdir}/rssh_chroot_helper


%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Tomas Hoger <thoger@fedoraproject.org> - 2.3.4-1
- Update to upstream version 2.3.4, which fixes CVE-2012-3478 and CVE-2012-2252
- Updated rsync-protocol.patch to fix CVE-2012-2251, and to apply on top of the
  CVE-2012-3478 and CVE-2012-2252 fixes.
- Updated makefile.patch to preserve RPM CFLAGS.
- Added command-line-error.patch (from Debian), correcting error message
  generated when insecure command line option is used (CVE-2012-3478 fix
  regression).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb  6 2012 Daniel Drake <dsd@laptop.org> - 2.3.3-3
- Add patch for rsync3 compat (#485946)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 19 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.3-1
- Upstream security fix release.  Resolves rhbz#705904

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 30 2008 Ian Weller <ianweller@gmail.com> - 2.3.2-5
- Remove pre and post scripts
  - https://bugzilla.redhat.com/show_bug.cgi?id=456182#c17

* Wed Aug 11 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.2-4
- Fix review issues and apply patch

* Wed Aug 07 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.2-3
- Fix postun to remove rssh shell

* Wed Jul 30 2008 Rahul Sundaram <sundaram@fedoraproject.org>  - 2.3.2-2
- Fix BR and defattr. Added a group and shell

* Tue Jul 22 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.2-1
- initial spec

