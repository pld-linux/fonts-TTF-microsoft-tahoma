#
# Conditional build:
%bcond_with	license_agreement
# _with_license_agreement       - generates package (may require Windows license?)
#
Summary:	Microsoft Tahoma True Type font
Summary(pl):	Font True Type Tahoma firmy Microsoft
Name:		fonts-TTF-microsoft-tahoma
Version:	20020525
Release:	1
# part of IE update - may require Windows license to use
License:	?
Group:		Fonts
# also at http://dl.sourceforge.net/corefonts/
Source0:	http://download.microsoft.com/download/ie6sp1/finrel/6_sp1/W98NT42KMeXP/EN-US/IELPKTH.CAB
# NoSource0-md5: 358584cddb75ac90472c25f01b308ebe
%if ! %{with license_agreement}
NoSource:	0
%endif
BuildRequires:	cabextract
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft Tahoma True Type font.

%description -l pl
Font True Type Tahoma firmy Microsoft.

%prep
%setup -q -c -T
%if ! %{with license_agreement}
exit 1
%endif
/usr/bin/cabextract -L %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf $RPM_BUILD_ROOT%{ttffontsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst TTF

%postun
fontpostinst TTF

%files
%defattr(644,root,root,755)
%{ttffontsdir}/*
