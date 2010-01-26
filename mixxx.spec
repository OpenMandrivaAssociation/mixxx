Summary:	Music DJing software
Name:		mixxx
Version:	1.7.2
Release:	%mkrel 1
Group:		Sound
License:	GPLv2+
URL:		http://mixxx.sourceforge.net/
Source:		http://downloads.sourceforge.net/mixxx/%{name}-%{version}-src.tar.gz
Patch2:		mixxx-1.7.0-ffmpeg-headers.patch
Patch3:		mixxx-1.7.2-fix-multiarch-sndfile.patch
BuildRequires:	libsndfile-devel
BuildRequires:	qt4-devel
BuildRequires:	fftw-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	jackit-devel
BuildRequires:	audiofile-devel
BuildRequires:	libid3tag-devel
BuildRequires:	mad-devel
BuildRequires:	mesaglu-devel
BuildRequires:	sndfile-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	portaudio-devel >= 0.19
BuildRequires:	libdjconsole-devel
BuildRequires:	ladspa-devel
BuildRequires:	libusb-devel
BuildRequires:	libgpod-devel
BuildRequires:	libshout-devel
#BuildRequires:	portmidi-devel
BuildRequires:	libffmpeg-devel
BuildRequires:	sed
BuildRequires:	scons
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
%patch2 -p1

# fix multiarch sndfile includes to backport to 2010.0
# multiarch is fixed in cooker
%if %mdkversion < 201010
%ifarch x86_64
%patch3 -p0
%endif
%endif

%build
sed -i -e "s|QTDIR\/lib|QTDIR\/%{_lib}|g" src/SConscript
sed -i -e 's|-Wl,-rpath,\$QTDIR/%{_lib}||g' src/SConscript

#sed -i -e "s|lib\/libqt-mt|%{_lib}\/libqt-mt|g" \
#	src/build.definition

%scons \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix} \
    qtdir=%{qt4dir} \
    djconsole=1 \
    optimize=0 \
    script=1 \
    shoutcast=1 \
    ladspa=1 \
    ipod=1 \
    hifieq=1 \
    ffmpeg=0 \
    vinylcontrol=1 \
    midiscript=1 \
    rawmidi=1 \
    tonal=1 \
    portmidi=0 \
    m4a=0 \
    tuned=0

%install
rm -rf %{buildroot}
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{qt4lib}/pkgconfig
mkdir -p %{buildroot}%{_prefix}
%scons_install \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix}

rm -fr %{buildroot}/%{_docdir}

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 src/mixxx.desktop %{buildroot}%{_datadir}/applications

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128,scalable}/apps

install -m644 res/images/iconsmall.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/mixxx-icon.png
install -m644 res/images/iconlarge.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/mixxx-icon.png
install -m644 res/images/iconhuge.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/mixxx-icon.png
install -m644 res/images/icon.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/mixxx-icon.png
install -m644 res/images/icon.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/mixxx-icon.svg

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
%doc README LICENSE README.macro
%doc Mixxx-Manual.pdf
%{_bindir}/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
