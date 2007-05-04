%define base_version 1.5.0
%define minor_version 1

Name: mixxx
Version: %{base_version}.%{minor_version}
Release: %mkrel 1
Group: Multimedia/Sound
Summary: Mixxx is DJ software
Source: %{name}-%{version}-src.tar.bz2
Patch0: mixxx-1.5.0.1-python-config.patch
URL: http://mixxx.sourceforge.net/
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	qt3-devel 
BuildRequires: fftw-devel 
BuildRequires: libogg-devel 
BuildRequires: libvorbis-devel 
BuildRequires: jackit-devel
BuildRequires:	audiofile-devel 
BuildRequires: libid3tag-devel 
BuildRequires: mad-devel
BuildRequires:	mesaglu-devel 
BuildRequires: alsa-lib-devel
BuildRequires:	libsndfile-devel
BuildRequires: portaudio-devel >= 0.19
BuildRequires: libdjconsole-devel
%py_requires -d

%description
Mixxx is DJ software emulating an analog mixer with two playback devices. The
mixer includes filters, crossfader and various volume controls. Each player
accepts wave and mp3 files as input, playback speed can be adjusted during
playback, and a wheel for fast searching through a song is provided.

Mixxx can be controlled through the GUI using the mouse, or by connecting MIDI
devices to the computer. Commercial and custom build MIDI controllers can be
used. The mapping between functions and MIDI controller values are done in
text files. 

%prep
%setup -q -n %name-%base_version
%patch0 -p1

%build
cd src

./configure \
	--prefix=%{_prefix} \
	--enable-jack \
	--enable-alsa \
	--enable-djconsole \
	--enable-python

%make

%install
rm -rf %buildroot
cd src
INSTALL_ROOT=%buildroot %makeinstall_std
rm -fr %buildroot/%_docdir

mkdir -p %buildroot%_datadir/applications
install -m644 mixxx.desktop %buildroot%_datadir/applications

for name in 16 32 48 128; do
	mkdir -p %buildroot%_iconsdir/hicolor/${name}x${name}/apps
done
install -m644 iconsmall.png %buildroot%_iconsdir/hicolor/16x16/apps/mixxx-icon.png
install -m644 iconlarge.png %buildroot%_iconsdir/hicolor/32x32/apps/mixxx-icon.png
install -m644 iconhuge.png %buildroot%_iconsdir/hicolor/48x48/apps/mixxx-icon.png
install -m644 icon.png %buildroot%_iconsdir/hicolor/128x128/apps/mixxx-icon.png

# We don't need old icon on pixmaps
rm -rf %buildroot%_datadir/pixmaps

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc COPYING README README.ALSA LICENSE
%doc Mixxx-Manual.pdf
%_bindir/%name
%_iconsdir/*/*/apps/mixxx-icon.png
%dir %_datadir/mixxx
%_datadir/mixxx/*
%_datadir/applications/%name.desktop

