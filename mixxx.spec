Summary:	Music DJing software
Name:		mixxx
Version:	1.7.2
Release:	%mkrel 2
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


%changelog
* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 1.7.2-2mdv2011.0
+ Revision: 593920
- rebuild for py2.7

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - add patch to fix build on x86_64, (multiarch has been fixed in cooker
      this is to make backports build)

* Sun Jan 24 2010 Jérôme Brenier <incubusss@mandriva.org> 1.7.2-1mdv2010.1
+ Revision: 495565
- new version 1.7.2
- fix x86_64 build

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.7.1
    - spec file clean
    - update to new version 1.7.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Emmanuel Andry <eandry@mandriva.org>
    - drop patches
    - use desktop-file-utils

* Mon Jan 19 2009 Götz Waschk <waschk@mandriva.org> 1.6.1-3mdv2009.1
+ Revision: 331127
- rebuild for new libgpod

* Sat Jan 17 2009 Funda Wang <fwang@mandriva.org> 1.6.1-2mdv2009.1
+ Revision: 330740
- rediff djconsole patch
- rebuild

* Thu Oct 23 2008 Helio Chissini de Castro <helio@mandriva.com> 1.6.1-1mdv2009.1
+ Revision: 296764
- New upstream version

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.6.0-0.beta2.1mdv2009.0
+ Revision: 252544
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Mar 07 2008 Adam Williamson <awilliamson@mandriva.org> 1.6.0-0.beta2.1mdv2008.1
+ Revision: 181218
- install .svg icon as well as .pngs
- adapt %%build and %%install to scons-based buildsystem, drop unnecessary substitutions
- update description
- update buildrequires for qt4 and scons-based buildsystem
- add optflags.patch (patches the build script to allow custom optflags, with thanks to misc for the python syntax help)
- add desktop.patch (fix up menu entry for MDV standards)
- add djconsole.patch (the build's test for libdjconsole doesn't seem to work for some reason, so disable the test and just assume it's present)
- drop djconsole-usb.patch (no longer needed, upstream uses pkg-config now)
- drop python-config.patch (no longer relevant)
- new license policy
- add conditionals to gracefully handle pre-release build
- new release 1.6.0 beta 2 (requested by Anne)

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.5.0.1-4mdv2008.1
+ Revision: 170982
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Aug 20 2007 Oden Eriksson <oeriksson@mandriva.com> 1.5.0.1-3mdv2008.0
+ Revision: 67909
- rebuilt against new portaudio libs

* Sun Jun 24 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.0.1-2mdv2008.0
+ Revision: 43661
- fix bug #31551
- add scriplets

* Sat Jun 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.0.1-1mdv2008.0
+ Revision: 40422
- add buildrequires on usb-devel
- fix building on x86_64
- added missing buildrequires
- spec file clean

  + Helio Chissini de Castro <helio@mandriva.com>
    - Added patch to fix djconsole build against libusb
    - New and revamped mixxx for Mandriva
    - Added support for libdjconsole \o/.
    - Added support for scripting back ( bad python config test )
    - Removed ols debian like menu
    - Added proper desktop file and their official icons
    - Restored portaudio build.
      Lets's have some fun !!


* Tue Sep 05 2006 Emmanuel Andry <eandry@mandriva.org> 1.4.2-3mdv2007.0
- xdg menu
- fix buildrequires

* Wed Jun 22 2005 Tibor Pittich <Tibor.Pittich@mandriva.org> 1.4.2-2mdk
- include README.ALSA
- use mkrel

* Fri Jan 14 2005 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.4.2-1mdk
- 1.4.2
- update configure parameters

* Thu Oct 14 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.4.1-1mdk
- 1.4.1

* Tue Oct 12 2004 Austin Acton <austin@mandrake.org> 1.4-1mdk
- 1.4

* Tue Sep 28 2004 Franck Villaume <fvill@freesurf.fr> 1.3.2-3mdk
- more BuildRequires

* Mon Sep 27 2004 Franck Villaume <fvill@freesurf.fr> 1.3.2-2mdk
- BuildRequires

* Tue Jul 27 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.3.2-1mdk
- 1.3.2
- added patch to allow buid with alsa support, enabled both jack and alsa
- cosmetics, added documentation

* Sun Jul 11 2004 Michael Scherer <misc@mandrake.org> 1.2.1-3mdk 
- rebuid for new gcc (patch #0)

* Mon Mar 22 2004 Austin Acton <austin@mandrake.org> 1.2.1-2mdk
- fix installation

* Mon Feb 16 2004 Austin Acton <austin@mandrake.org> 1.2.1-1mdk
- 1.2.1

* Tue Dec 30 2003 Austin Acton <austin@linux.ca> 1.2-1mdk
- 1.2
- link to local libs

* Mon Oct 06 2003 Austin Acton <aacton@yorku.ca> 1.0-1mdk
- 1.0
- delib buildrequires

