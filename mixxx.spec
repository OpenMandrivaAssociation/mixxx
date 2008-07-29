%define base_version	1.6.0
%define pre		beta2
%define minor_version	1
%if %pre
%define release		%mkrel 0.%pre.1
%define version		%base_version
%define distname	%name-%version-%pre
%else
%define release		%mkrel 3
%define version		%base_version.%minor_version
%define distname	%name-%version
%endif

Summary:	Music DJing software
Name:		mixxx
Version:	%{version}
Release:	%{release}
Group:		Sound
License:	GPLv2+
URL:		http://mixxx.sourceforge.net/
Source:		http://downloads.sourceforge.net/mixxx/%{distname}-src.tar.gz
# Remove the djconsole test, as it doesn't seem to work - AdamW 2008/03
Patch0:		mixxx-1.6.0-djconsole.patch
# Fix up the menu entry for MDV standards - AdamW 2008/03
Patch1:		mixxx-1.6.0-desktop.patch
# Allow custom optflags to be specified as a build parameter, letting
# us use the MDV optflags: with thanks to misc for python help :)
# - AdamW 2008/03
Patch2:		mixxx-1.6.0-optflags.patch
BuildRequires:	libsndfile-static-devel
BuildRequires:	qt4-devel 
BuildRequires:	fftw-devel 
BuildRequires:	libogg-devel 
BuildRequires:	libvorbis-devel 
BuildRequires:	jackit-devel
BuildRequires:	audiofile-devel 
BuildRequires:	libid3tag-devel 
BuildRequires:	mad-devel
BuildRequires:	mesaglu-devel 
BuildRequires:	alsa-lib-devel
BuildRequires:	portaudio-devel >= 0.19
BuildRequires:	libdjconsole-devel
BuildRequires:	libusb-devel
BuildRequires:	sed
BuildRequires:	scons
BuildRequires:	qt4-linguist
%py_requires -d
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Mixxx allows DJs to mix music live with a clean, simple interface.
Futhermore, Mixxx has a number of key features to help DJs in the mix:
Beat estimation, parallel visual displays, and support for various DJ
hardware controllers.

Mixxx can be controlled through the GUI using the mouse, or by
connecting MIDI devices to the computer. Commercial and custom build
MIDI controllers can be used. The mapping between functions and MIDI
controller values are done in text files. 

%prep
%if %pre
%setup -q -n %{name}-%{base_version}%{pre}
%else
%setup -q -n %{name}-%{base_version}
%endif
%patch0 -p1 -b .djconsole
%patch1 -p1 -b .desktop
%patch2 -p1 -b .optflags

%build
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{qt4lib}/pkgconfig

sed -i -e "s|QTDIR\/lib|QTDIR\/%{_lib}|g" \
	src/SConscript
sed -i -e "s|lib\/libqt-mt|%{_lib}\/libqt-mt|g" \
	src/build.definition

scons %{_smp_mflags} prefix=%{_prefix} install_root=%{buildroot}%{_prefix} qtdir=%{qt4dir} djconsole=1 optimize="%{optflags}"

%install
rm -rf %{buildroot}
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{qt4lib}/pkgconfig
mkdir -p %{buildroot}%{_prefix}
scons %{_smp_mflags} install prefix=%{_prefix} install_root=%{buildroot}%{_prefix} qtdir=%{qt4dir} djconsole=1 optimize="%{optflags}"
rm -fr %{buildroot}/%{_docdir}

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 src/mixxx.desktop %{buildroot}%{_datadir}/applications

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128,scalable}/apps

install -m644 src/iconsmall.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/mixxx-icon.png
install -m644 src/iconlarge.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/mixxx-icon.png
install -m644 src/iconhuge.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/mixxx-icon.png
install -m644 src/icon.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/mixxx-icon.png
install -m644 src/icon.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/mixxx-icon.png

# not needed
rm -rf %{buildroot}%{_datadir}/pixmaps

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%files
%defattr(-,root,root)
%doc COPYING README LICENSE README.macro HERCULES.txt 
%doc Mixxx-Manual.pdf
%{_bindir}/%{name}
%{_iconsdir}/*/*/apps/mixxx-icon.*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop

