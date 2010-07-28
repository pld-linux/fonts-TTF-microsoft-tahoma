#
# Conditional build:
%bcond_with	license_agreement	# generates package (requires Windows license)
#
%define		base_name		fonts-TTF-microsoft-tahoma
%define		_rel			5
Summary:	Microsoft Tahoma TrueType font
Summary(pl.UTF-8):	Font TrueType Tahoma firmy Microsoft
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	20020525
Release:	%{_rel}%{?with_license_agreement:wla}
# part of IE update - requires Windows license to use
License:	Windows EULA
Group:		Fonts
%if %{with license_agreement}
Source0:	http://download.microsoft.com/download/ie6sp1/finrel/6_sp1/W98NT42KMeXP/EN-US/IELPKTH.CAB
# NoSource0-md5: 358584cddb75ac90472c25f01b308ebe
NoSource:	0
BuildRequires:	cabextract
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
%else
Source1:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source1-md5:  329c25f457fea66ec502b7ef70cb9ede
Requires:	cabextract
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft Tahoma TrueType font.

%description -l pl.UTF-8
Font TrueType Tahoma firmy Microsoft.

%prep
%if %{with license_agreement}
%setup -q -c -T
%{_bindir}/cabextract -L %{SOURCE0}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if !%{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@USE_DISTFILES@,no,g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
' %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf $RPM_BUILD_ROOT%{ttffontsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with license_agreement}
%post
fontpostinst TTF

%postun
fontpostinst TTF

%else
%post
echo "
License issues made us not to include inherent files into this package
by default (You need Windows license). If you want to create full
working package please build it with the following command:

%{_bindir}/%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%{ttffontsdir}/*
%else
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%endif
