%define name	mixxx	
%define version	1.4.2
%define release	%mkrel 3

%define	section	Multimedia/Sound
%define	title	Mixxx
%define Summary	Digital DJ and mixing software

Name: 	 	%{name}
Summary:	%{Summary}
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png
Patch:          mixx-1.2.1-gcc34.diff
URL:		http://mixxx.sourceforge.net/
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	qt3-devel fftw-devel libogg-devel libvorbis-devel jackit-devel
BuildRequires:	audiofile-devel libid3tag-devel mad-devel
BuildRequires:	mesaglu-devel alsa-lib-devel
BuildRequires:	libsndfile-static-devel

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
%setup -q
%patch -p0
%build
cd src
./configure --enable-jack --enable-alsa
%{_libdir}/qt3/bin/qmake mixxx.pro
%make

%install
rm -rf $RPM_BUILD_ROOT
cd src
INSTALL_ROOT=$RPM_BUILD_ROOT %makeinstall_std
rm -fr $RPM_BUILD_ROOT/%_docdir

#menu
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
command="%_bindir/%name" \
needs="X11" \
icon="%name.png" \
section="%section" \
title="%title" \
longtitle="%Summary" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;AudioVideo;Mixer;
Encoding=UTF-8
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE1 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE2 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%doc COPYING README README.ALSA LICENSE
%doc Mixxx-Manual.pdf
%{_bindir}/%name
%{_datadir}/%name
%{_menudir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

