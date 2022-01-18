Summary:	Music DJing software
Name:		mixxx
Version:	2.3.1
Release:	2
Group:		Sound/Players
License:	GPLv2+
URL:		https://www.mixxx.org/
Source0:	https://github.com/mixxxdj/mixxx/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		mixxx-2.3.1-compile.patch
Patch1:		mixxx-2.3.1-ffmpeg-5.0.patch

BuildRequires:  cmake ninja
BuildRequires:	icoutils
BuildRequires:	imagemagick
BuildRequires:	sed
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:  lame-devel
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
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(wavpack)
BuildRequires:  pkgconfig(vamp-hostsdk)
BuildRequires:  pkgconfig(vamp-sdk)
BuildRequires:	pkgconfig(udev)
BuildRequires:  vamp-plugin-sdk-devel

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
%autosetup -n %{name}-%{version} -p1
%setup_compile_flags
%cmake -G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
rm -fr %{buildroot}%{_docdir}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
install -m644 res/images/templates/ic_template_mixxx.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

# not needed
rm -rf %{buildroot}%{_datadir}/pixmaps

%files
%doc README* LICENSE
%{_bindir}/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/%{name}/
%{_datadir}/applications/org.mixxx.Mixxx.desktop
%{_datadir}/metainfo/org.mixxx.Mixxx.metainfo.xml
/lib/udev/rules.d/*
