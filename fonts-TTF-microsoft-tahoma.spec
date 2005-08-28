#
# Conditional build:
%bcond_with	license_agreement	# generates package (may require Windows license?)
#
Summary:	Microsoft Tahoma True Type font
Summary(pl):	Font True Type Tahoma firmy Microsoft
%define		base_name		fonts-TTF-microsoft-tahoma
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	20020525
Release:	2%{?with_license_agreement:wla}
# part of IE update - may require Windows license to use
License:	?
Group:		Fonts
%if %{with license_agreement}
# also at http://dl.sourceforge.net/corefonts/
Source0:	http://download.microsoft.com/download/ie6sp1/finrel/6_sp1/W98NT42KMeXP/EN-US/IELPKTH.CAB
# NoSource0-md5: 358584cddb75ac90472c25f01b308ebe
BuildRequires:	cabextract
Requires:	%{_fontsdir}/TTF
Requires(post,postun):	fontpostinst
%else
Source0:	license-installer.sh
Requires:	cabextract
Requires:	rpm-build-tools
Requires:	wget
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft Tahoma True Type font.
%if %{without license_agreement}
License issues made us not to include inherent files into this package
by default (it probably requires Windows license). If you want to
create full working package please build it with one of the following
command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%description -l pl
Font True Type Tahoma firmy Microsoft.
%if %{without license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików (prawdopodobnie wymaga licencji na Windows). Je¶li chcesz stworzyæ
w pe³ni funkcjonalny pakiet, zbuduj go za pomoc± polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%prep
%if %{with license_agreement}
%setup -q -c -T
/usr/bin/cabextract -L %{SOURCE0}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

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
%pre
echo "
License issues made us not to include inherent files into this package
by default (it probably requires Windows license). If you want to
create full working package please build it with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
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
