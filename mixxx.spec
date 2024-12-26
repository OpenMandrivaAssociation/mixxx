%undefine _debugsource_packages
%global optflags %{optflags} -DPROTOBUF_USE_DLLS=1 -Wno-nan-infinity-disabled

Summary:	Music DJing software
Name:		mixxx
Version:	2.5.0
Release:	1
Group:		Sound/Players
License:	GPLv2+
URL:		https://www.mixxx.org/
Source0:	https://github.com/mixxxdj/mixxx/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake ninja
BuildRequires:	icoutils
BuildRequires:	imagemagick
BuildRequires:	sed
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:  lame-devel
BuildRequires:	scons
BuildRequires:	portmidi-devel
BuildRequires:  pkgconfig(gtest)
BuildRequires:	cmake(Qt6Keychain)
BuildRequires:  cmake(Microsoft.GSL)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(flac)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	pkgconfig(Qt6Concurrent)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:  pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Sql)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6SvgWidgets)
BuildRequires:  pkgconfig(Qt6ShaderTools)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Xml)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:  pkgconfig(benchmark)
BuildRequires:  pkgconfig(libkeyfinder)
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
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  cmake(VulkanHeaders)
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
sed -i -e 's,CMAKE_CXX_STANDARD 17,CMAKE_CXX_STANDARD 20,g' CMakeLists.txt
%cmake -G Ninja -DENGINEPRIME=OFF

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
%{_prefix}/lib/udev/rules.d/*
