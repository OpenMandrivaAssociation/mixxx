Name: mixxx
Version: 1.7.0
Release: %mkrel 1
Group: Sound
License: GPLv2+
Summary: Music DJing software
URL: http://mixxx.sourceforge.net/
Source: http://downloads.sourceforge.net/mixxx/%{name}-%{version}-src.tar.gz
# Remove the djconsole test, as it doesn't seem to work - AdamW 2008/03
#Patch0:	 mixxx-1.6.1-djconsole.patch
# Fix up the menu entry for MDV standards - AdamW 2008/03
#Patch1: mixxx-1.6.0-desktop.patch
BuildRequires: libsndfile-static-devel
BuildRequires: qt4-devel
BuildRequires: fftw-devel
BuildRequires: libogg-devel
BuildRequires: libvorbis-devel
BuildRequires: jackit-devel
BuildRequires: audiofile-devel
BuildRequires: libid3tag-devel
BuildRequires: mad-devel
BuildRequires: mesaglu-devel
BuildRequires: sndfile-devel
BuildRequires: alsa-lib-devel
BuildRequires: portaudio-devel >= 0.19
BuildRequires: libdjconsole-devel
BuildRequires: ladspa-devel
BuildRequires: libusb-devel
BuildRequires: libgpod-devel
BuildRequires: libshout-devel
BuildRequires: sed
BuildRequires: scons
BuildRequires: desktop-file-utils
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
%setup -q 
#%patch0 -p1 -b .djconsole
#%patch1 -p1 -b .desktop

%build
sed -i -e "s|QTDIR\/lib|QTDIR\/%{_lib}|g" \
	src/SConscript
#sed -i -e "s|lib\/libqt-mt|%{_lib}\/libqt-mt|g" \
#	src/build.definition

scons \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix} \
    qtdir=%{qt4dir} \
    djconsole=1 \
    optimize=1 \
    script=1 \
    shoutcast=1 \
    ladspa=1 \
    ipod=1

%install
rm -rf %{buildroot}
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{qt4lib}/pkgconfig
mkdir -p %{buildroot}%{_prefix}

scons \
    install \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix} \
    qtdir=%{qt4dir} \
    djconsole=1 \
    optimize=1 \
    script=1 \
    shoutcast=1 \
    ladspa=1 \
    ipod=1

rm -fr %{buildroot}/%{_docdir}

#mkdir -p %{buildroot}%{_datadir}/applications
#install -m644 src/mixxx.desktop %{buildroot}%{_datadir}/applications

#mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128,scalable}/apps

#install -m644 src/iconsmall.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/mixxx-icon.png
#install -m644 src/iconlarge.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/mixxx-icon.png
#install -m644 src/iconhuge.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/mixxx-icon.png
#install -m644 src/icon.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/mixxx-icon.png
#install -m644 src/icon.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/mixxx-icon.png

#remove png extension
sed -i -e 's/^Icon=%{name}-icon.png$/Icon=%{name}-icon/g' %{buildroot}%{_datadir}/applications/*

desktop-file-install \
  --copy-name-to-generic-name \
  --add-category="Qt;AudioVideo;Audio;" \
  --remove-category="Application" \
  --remove-key="Encoding" \
  --remove-key="Version" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# not needed
#rm -rf %{buildroot}%{_datadir}/pixmaps

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
#%{_iconsdir}/*/*/apps/mixxx-icon.*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/%{name}.desktop

