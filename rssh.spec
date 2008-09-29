Name:           rssh
Version:        2.3.2
Release:        4%{?dist}
Summary:        Restricted shell for use with OpenSSH, allowing only scp and/or sftp
Group:          Applications/Internet
License:        BSD 
URL:            http://www.pizzashack.org/rssh/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         rssh-2.3.2-makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

chmod 644 conf_convert.sh
chmod 644 mkchroot.sh


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%pre
getent group rsshusers >/dev/null || groupadd -r rsshusers
exit 0

%post
# Add rssh to the list of allowed shells in /etc/shells
if ! grep %_bindir/rssh %_sysconfdir/shells >/dev/null; then
        echo %_bindir/rssh >>%_sysconfdir/shells
fi

%postun
# Remove rssh from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then
        grep -v %_bindir/rssh %_sysconfdir/shells >%_sysconfdir/rssh.tmp
        mv %_sysconfdir/rssh.tmp %_sysconfdir/shells
fi


%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog CHROOT COPYING NEWS README SECURITY TODO
%doc conf_convert.sh mkchroot.sh
%doc %{_mandir}/man1/rssh.1*
%doc %{_mandir}/man5/rssh.conf.5*
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(750, root, rsshusers) %{_bindir}/rssh
%attr(4750, root, rsshusers) %{_libexecdir}/rssh_chroot_helper


%changelog

* Wed Aug 11 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.2-4
- Fix review issues and apply patch

* Wed Aug 07 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.2-3
- Fix postun to remove rssh shell

* Wed Jul 30 2008 Rahul Sundaram <sundaram@fedoraproject.org>  - 2.3.2-2
- Fix BR and defattr. Added a group and shell

* Tue Jul 22 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 2.3.2-1
- initial spec


