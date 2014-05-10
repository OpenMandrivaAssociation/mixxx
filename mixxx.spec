Summary:	Music DJing software
Name:		mixxx
Version:	1.11.0
Release:	3
Group:		Sound
License:	GPLv2+
URL:		http://mixxx.sourceforge.net/
Source:		http://downloads.mixxx.org/%{name}-%{version}/%{name}-%{version}-src.tar.gz
BuildRequires:	qt4-devel >= 4.6.0
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(libdjconsole)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libgpod-1.0)
BuildRequires:	pkgconfig(shout)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(wavpack)
BuildRequires:	pkgconfig(libchromaprint)
BuildRequires:	ladspa-devel
BuildRequires:	portmidi-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	scons
BuildRequires:	python
BuildRequires:	imagemagick
Requires:	qt4-database-plugin-sqlite

%description
Mixxx allows DJs to mix music live with a clean, simple interface.
Futhermore, Mixxx has a number of key features to help DJs in the mix: beat
estimation, parallel visual displays, and support for various DJ hardware
controllers.

Mixxx can be controlled through the GUI using the mouse, or by connecting MIDI
devices to the computer. Commercial and custom build MIDI controllers can be
used. The mapping between functions and MIDI controller values are done in
text files. 


%prep
%setup -q

sed -i -e "s|QTDIR\/lib|QTDIR\/%{_lib}|g" src/SConscript
sed -i -e "s|(install_root, 'lib')|(install_root, '%{_lib}')|g" src/SConscript


%build
%scons \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix} \
    qtdir=%{qt4dir} \
    qdebug=0 \
    djconsole=1 \
    optimize=0 \
    shoutcast=1 \
    wavpack=1 \
    promotracks=1 \
    ladspa=0 \
    ipod=0 \
    hifieq=1 \
    ffmpeg=0 \
    vamp=1 \
    vinylcontrol=1 \
    tonal=0 \
    portmidi=1 \
    m4a=0 \
    tuned=0


%install
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{qt4lib}/pkgconfig
mkdir -p %{buildroot}%{_prefix}
%scons_install \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix}


# menu entry
mkdir -p %{buildroot}%{_datadir}/applications
install -m644 src/mixxx.desktop %{buildroot}%{_datadir}/applications

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}/apps
install -m644 res/images/mixxx-icon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/mixxx-icon.png
convert -resize 128x128 res/images/mixxx-icon.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/mixxx-icon.png
convert -resize 32x32 res/images/mixxx-icon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/mixxx-icon.png
convert -resize 16x16 res/images/mixxx-icon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/mixxx-icon.png

# clean
rm -rf %{buildroot}%{_datadir}/pixmaps
rm -fr %{buildroot}/%{_docdir}
chmod +x %{buildroot}%{_datadir}/%{name}/controllers/convertToXMLSchemaV1.php
chmod +x %{buildroot}%{_datadir}/%{name}/controllers/Vestax-VCI-300-scripts.js


%files
%doc README LICENSE README.macro
%doc Mixxx-Manual.pdf
%{_bindir}/%{name}
%{_libdir}/%{name}/plugins/vamp/*.so
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop


