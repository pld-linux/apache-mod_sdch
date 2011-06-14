%define		svnrev	9
%define		rel		0.1
%define		mod_name	sdch
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache implementation of shared dictionary comrpession over HTTP
Name:		apache-mod_%{mod_name}
Version:	0
Release:	%{svnrev}.%{rel}
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
# revno=
# svn co http://mod-sdch.googlecode.com/svn/trunk${revno:+@$revno} mod-sdch
# tar -cjf mod-sdch-$(svnversion mod-sdch).tar.bz2 --exclude-vcs mod-sdch
# ../dropin mod-sdch-$(svnversion mod-sdch).tar.bz2
Source0:	mod-sdch-9.tar.bz2
# Source0-md5:	-
#Source1:	apache.conf
URL:		http://code.google.com/p/mod-sdch/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
Shared Dictionary Compression over HTTP is a proposed modification to
RFC 2616.

This Apache module will initially attempt to prototype a reference
implementation.

%prep
%setup -qn mod-%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -p mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

# module configuration
# - should contain LoadModule line
# - and directives must be between IfModule (so user could disable the module easily)
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

# or, if no directives needed, put just LoadModule line
echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}.so
