%define beta            b8
%define section         free
%define orig_name       jdom
%define gcj_support     1

Name:           oldjdom
Version:        1.0
Release:        %mkrel 0.%{beta}.2.8
Epoch:          0
Summary:        Java alternative to DOM and SAX
License:        Apache License-like
URL:            http://www.jdom.org/
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        http://www.jdom.org/dist/source/jdom-b8.tar.bz2
Requires:       xalan-j2 >= 0:2.2.0
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant
BuildRequires:  xalan-j2 >= 0:2.2.0
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
JDOM is, quite simply, a Java representation of an XML document. JDOM
provides a way to represent that document for easy and efficient
reading, manipulation, and writing. It has a straightforward API, is a
lightweight and fast, and is optimized for the Java programmer. It's an
alternative to DOM and SAX, although it integrates well with both DOM
and SAX.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{orig_name}-%{beta}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=$(build-classpath xalan-j2 xml-commons-apis)
perl -p -i -e 's|<property name="build.compiler".*||' build.xml
%ant package javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{orig_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt COMMITTERS.txt LICENSE.txt README.txt TODO.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}




%changelog
* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.0-0.b8.2.8mdv2010.0
+ Revision: 426267
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.0-0.b8.2.7mdv2009.0
+ Revision: 136634
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-0.b8.2.7mdv2008.1
+ Revision: 120999
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-0.b8.2.6mdv2008.0
+ Revision: 87273
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.0-0.b8.2.5mdv2008.0
+ Revision: 82876
- rebuild


* Fri Mar 16 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.0-0.b8.2.4mdv2007.1
+ Revision: 144745
- rebuild for 2007.1
- Import oldjdom

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.0-0.b8.2.2mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sat May 28 2005 David Walluck <walluck@mandriva.org> 0:1.0-0.b8.2.1mdk
- release

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com> 0:1.0-0.b8.2jpp
- Rebuild with Ant 1.6.2

