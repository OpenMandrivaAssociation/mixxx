%undefine	_debugsource_packages
%global		optflags %{optflags} -DPROTOBUF_USE_DLLS=1 -Wno-nan-infinity-disabled

Summary:	Music DJing software
Name:		mixxx
Version:		2.5.6
Release:		2
Group:		Sound/Players
License:	GPLv2+
Url:		https://www.mixxx.org/
Source0:	https://github.com/mixxxdj/mixxx/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:		cmake >= 3.21
BuildRequires:		icoutils
BuildRequires:		imagemagick
BuildRequires:		ninja
#BuildRequires:	scons
BuildRequires:		sed
BuildRequires:		ffmpeg-devel
BuildRequires:		ladspa-devel
BuildRequires:		vamp-plugin-sdk-devel
BuildRequires:		cmake(Qt6Keychain)
BuildRequires:		cmake(Qt6LinguistTools)
BuildRequires:		cmake(Microsoft.GSL)
BuildRequires:		cmake(Qt6QuickShapesPrivate)
BuildRequires:		cmake(VulkanHeaders)
BuildRequires:		pkgconfig(alsa)
BuildRequires:		pkgconfig(audiofile)
BuildRequires:		pkgconfig(benchmark)
BuildRequires:		pkgconfig(cups)
BuildRequires:		pkgconfig(fftw3)
BuildRequires:		pkgconfig(flac)
BuildRequires:		pkgconfig(gl)
BuildRequires:		pkgconfig(gtest)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(hidapi-libusb)
BuildRequires:		pkgconfig(id3tag)
BuildRequires:		pkgconfig(lame)
BuildRequires:		pkgconfig(libchromaprint)
BuildRequires:		pkgconfig(libcrypto)
BuildRequires:		pkgconfig(libebur128)
BuildRequires:		pkgconfig(libgpod-1.0)
BuildRequires:		pkgconfig(libkeyfinder)
BuildRequires:		pkgconfig(libmodplug)
BuildRequires:		pkgconfig(libusb-1.0)
BuildRequires:		pkgconfig(lilv-0)
BuildRequires:		pkgconfig(mad)
BuildRequires:		pkgconfig(mp4v2)
BuildRequires:		pkgconfig(ogg)
BuildRequires:		pkgconfig(opusfile)
BuildRequires:		pkgconfig(portaudio-2.0)
BuildRequires:		pkgconfig(portmidi)
BuildRequires:		pkgconfig(protobuf)
BuildRequires:		pkgconfig(Qt6Concurrent)
BuildRequires:		pkgconfig(Qt6Core)
BuildRequires:		pkgconfig(Qt6Core5Compat)
BuildRequires:		pkgconfig(Qt6DBus)
BuildRequires:		pkgconfig(Qt6Gui)
BuildRequires:		pkgconfig(Qt6Help)
BuildRequires:		pkgconfig(Qt6LabsQmlModels)
BuildRequires:		pkgconfig(Qt6Network)
BuildRequires:		pkgconfig(Qt6OpenGL)
BuildRequires:		pkgconfig(Qt6PrintSupport)
BuildRequires:		pkgconfig(Qt6Quick)
BuildRequires:		pkgconfig(Qt6QuickControls2)
BuildRequires:		pkgconfig(Qt6QuickControls2Basic)
BuildRequires:		pkgconfig(Qt6QuickControls2BasicStyleImpl)
BuildRequires:		pkgconfig(Qt6QuickControls2Fusion)
BuildRequires:		pkgconfig(Qt6QuickControls2FusionStyleImpl)
BuildRequires:		pkgconfig(Qt6QuickControls2Impl)
BuildRequires:		pkgconfig(Qt6QuickLayouts)
BuildRequires:		pkgconfig(Qt6QuickWidgets)
BuildRequires:		pkgconfig(Qt6Qml)
BuildRequires:		pkgconfig(Qt6Sql)
BuildRequires:		pkgconfig(Qt6Svg)
BuildRequires:		pkgconfig(Qt6SvgWidgets)
BuildRequires:		pkgconfig(Qt6ShaderTools)
BuildRequires:		pkgconfig(Qt6Test)
BuildRequires:		pkgconfig(Qt6Widgets)
BuildRequires:		pkgconfig(Qt6Xml)
BuildRequires:		pkgconfig(rubberband)
BuildRequires:		pkgconfig(shout)
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(soundtouch)
BuildRequires:		pkgconfig(sqlite3)
BuildRequires:		pkgconfig(taglib)
BuildRequires:		pkgconfig(udev)
BuildRequires:		pkgconfig(upower-glib)
BuildRequires:		pkgconfig(vamp-hostsdk)
BuildRequires:		pkgconfig(vamp-sdk)
BuildRequires:		pkgconfig(vorbis)
BuildRequires:		pkgconfig(vulkan)
BuildRequires:		pkgconfig(wavpack)
BuildRequires:		pkgconfig(x11)
BuildRequires:		pkgconfig(xext)
BuildRequires:		pkgconfig(xkbcommon-x11)
BuildRequires:		pkgconfig(zlib)
Requires:	qt6-qtbase-sql-sqlite

%description
Mixxx allows DJs to mix music live with a clean, simple interface. Futhermore,
it has a number of key features to help DJs in the mix: beat estimation,
parallel visual displays, and support for various DJ hardware controllers.
It can be controlled through the GUI using the mouse, or by connecting MIDI
devices to the computer. Commercial and custom build MIDI controllers can be
used. The mapping between functions and MIDI controller values are done
in text files.

%files
%doc README* LICENSE
%{_bindir}/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/%{name}/
%{_datadir}/applications/org.mixxx.Mixxx.desktop
%{_datadir}/metainfo/org.mixxx.Mixxx.metainfo.xml
%{_prefix}/lib/udev/rules.d/*

#-----------------------------------------------------------------------------

%prep
%autosetup -n %{name}-%{version} -p1


%build
#setup_compile_flags
#sed -i -e 's,CMAKE_CXX_STANDARD 17,CMAKE_CXX_STANDARD 20,g' CMakeLists.txt
%cmake -G Ninja -DENGINEPRIME=OFF
%ninja_build


%install
%ninja_install -C build
rm -fr %{buildroot}%{_docdir}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
install -m644 res/images/templates/ic_template_mixxx.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

# Not needed
rm -rf %{buildroot}%{_datadir}/pixmaps
