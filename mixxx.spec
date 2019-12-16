Summary:	Music DJing software
Name:		mixxx
Version:	2.2.3
Release:	1
Group:		Sound/Players
License:	GPLv2+
URL:		https://www.mixxx.org/
Source0:	https://github.com/mixxxdj/mixxx/archive/release-%{version}/%{name}-release-%{version}.tar.gz
Patch0:     mixxx-2.2.2-scons-python3.patch
BuildRequires:	icoutils
BuildRequires:	imagemagick
BuildRequires:	scons
BuildRequires:	sed
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	scons
BuildRequires:	qt5-linguist-tools
BuildRequires:	portmidi-devel
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:	pkgconfig(Qt5ScriptTools)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(libchromaprint)
BuildRequires:	pkgconfig(libebur128)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libgpod-1.0)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:	pkgconfig(lilv-0)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(shout)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(opusfile)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(protobuf)
#BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(wavpack)

Requires:	qt5-database-plugin-sqlite

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
%autosetup -n %{name}-release-%{version} -p1

%build
%setup_compile_flags

sed -i -e "s|QTDIR\/lib|QTDIR\/%{_lib}|g" src/SConscript
sed -i -e 's|-Wl,-rpath,\$QTDIR/%{_lib}||g' src/SConscript

%global machine %{_arch}

%ifarch %ix86
%global machine i586
%endif
%ifarch x86_64
%global machine amd64
%endif
%ifarch armv5tl
%global machine armel
%endif
%ifarch armv7hl
%global machine armhf
%endif

#FIXME : LIBDIR needed by Mixxx as of 2.0.0 version
export LIBDIR=%{_libdir}

%scons \
    prefix=%{_prefix} \
    install_root=%{buildroot}%{_prefix} \
    qt5=1 \
    qtdir=%{_libdir}/qt5 \
    build=release \
    optimize=portable \
    shoutcast=1 \
    ladspa=0 \
    ipod=0 \
    ffmpeg=1 \
    vinylcontrol=1 \
    portmidi=1 \
    m4a=0 \
    tuned=0 \
    vamp=1 \
    qtkeychain=1 \
    wavpack=1 \
    modplug=1 \
    machine=%{machine}

%install
#FIXME : LIBDIR needed by Mixxx as of 2.0.0 version
export LIBDIR=%{_libdir}

%scons install DESTDIR=%{buildroot} \
    prefix=%{_prefix} \
    qtdir=%{_libdir}/qt5 \
    install_root=%{buildroot}%{_prefix} \
    qt5=1 \
    machine=%{machine}

rm -fr %{buildroot}%{_docdir}

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 res/linux/%{name}.desktop %{buildroot}%{_datadir}/applications
sed -i -e "s|mixxx-icon|mixxx|g" %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
install -m644 res/images/templates/ic_template_mixxx.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

# Install udev rule
mkdir -p %{buildroot}%{_udevrulesdir}
install -p -m 0644 res/linux/mixxx.usb.rules %{buildroot}%{_udevrulesdir}/90-mixxx.usb.rules

# not needed
rm -rf %{buildroot}%{_datadir}/pixmaps

%files
%doc CHANGELOG README* LICENSE
%doc Mixxx-Manual.pdf
%{_bindir}/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_libdir}/%{name}/
%{_udevrulesdir}/90-%{name}.usb.rules
