%bcond_with ocf

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#################################################################################
# common
#################################################################################
Name:		ceph
Version:	0.80.5
Release:	1%{?dist}
Summary:	User space components of the Ceph file system
License:	GPL-2.0
Group:		System Environment/Base
URL:		http://ceph.com/
Source0:	http://ceph.com/download/%{name}-%{version}.tar.gz
Requires:	librbd1 = %{version}-%{release}
Requires:	librados2 = %{version}-%{release}
Requires:	libcephfs1 = %{version}-%{release}
Requires:	ceph-common = %{version}-%{release}
Requires:	python
Requires:	python-argparse
Requires:	python-ceph
Requires:	python-requests
Requires:	xfsprogs
Requires:	cryptsetup
Requires:	parted
Requires:	util-linux
Requires:	hdparm
Requires(post):	binutils
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:	make
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	boost-devel
BuildRequires:	libedit-devel
BuildRequires:	perl
BuildRequires:	gdbm
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-nose
BuildRequires:	python-argparse
BuildRequires:	libaio-devel
BuildRequires:	libcurl-devel
BuildRequires:	libxml2-devel
BuildRequires:	libuuid-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	leveldb-devel > 1.2
BuildRequires:	xfsprogs-devel
BuildRequires:	yasm
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora}
BuildRequires:	snappy-devel
%endif

#################################################################################
# specific
#################################################################################
%if ! 0%{?rhel}
BuildRequires:	sharutils
%endif

%if 0%{defined suse_version}
%if 0%{?suse_version} > 1210
Requires:	gptfdisk
BuildRequires:	gperftools-devel
%else
Requires:	scsirastools
BuildRequires:	google-perftools-devel
%endif
Recommends:	logrotate
BuildRequires:	%insserv_prereq
BuildRequires:	mozilla-nss-devel
BuildRequires:	keyutils-devel
BuildRequires:	libatomic-ops-devel
BuildRequires:	fdupes
%else
Requires:	gdisk
BuildRequires:	nss-devel
BuildRequires:	keyutils-libs-devel
BuildRequires:	libatomic_ops-devel
Requires:	gdisk
Requires(post):	chkconfig
Requires(preun):chkconfig
Requires(preun):initscripts
BuildRequires:	gperftools-devel
%endif

%description
Ceph is a massively scalable, open-source, distributed
storage system that runs on commodity hardware and delivers object,
block and file system storage.


#################################################################################
# packages
#################################################################################
%package -n ceph-common
Summary:	Ceph Common
Group:		System Environment/Base
Requires:	librbd1 = %{version}-%{release}
Requires:	librados2 = %{version}-%{release}
Requires:	python-ceph = %{version}-%{release}
Requires:	python-requests
Requires:	redhat-lsb-core
%description -n ceph-common
common utilities to mount and interact with a ceph storage cluster

%package fuse
Summary:	Ceph fuse-based client
Group:		System Environment/Base
Requires:	%{name}
BuildRequires:	fuse-devel
%description fuse
FUSE based client for Ceph distributed network file system

%package -n rbd-fuse
Summary:	Ceph fuse-based client
Group:		System Environment/Base
Requires:	%{name}
Requires:	librados2 = %{version}-%{release}
Requires:	librbd1 = %{version}-%{release}
BuildRequires:	fuse-devel
%description -n rbd-fuse
FUSE based client to map Ceph rbd images to files

%package devel
Summary:	Ceph headers
Group:		Development/Libraries
License:	LGPL-2.0
Requires:	%{name} = %{version}-%{release}
Requires:	librados2 = %{version}-%{release}
Requires:	librbd1 = %{version}-%{release}
Requires:	libcephfs1 = %{version}-%{release}
Requires:	libcephfs_jni1 = %{version}-%{release}
%description devel
This package contains libraries and headers needed to develop programs
that use Ceph.

%package radosgw
Summary:	Rados REST gateway
Group:		Development/Libraries
Requires:	ceph-common = %{version}-%{release}
Requires:	librados2 = %{version}-%{release}
%if 0%{defined suse_version}
BuildRequires:	libexpat-devel
BuildRequires:	FastCGI-devel
Requires:	apache2-mod_fcgid
%else
BuildRequires:	expat-devel
BuildRequires:	fcgi-devel
%endif
%description radosgw
radosgw is an S3 HTTP REST gateway for the RADOS object store. It is
implemented as a FastCGI module using libfcgi, and can be used in
conjunction with any FastCGI capable web server.

%if %{with ocf}
%package resource-agents
Summary:	OCF-compliant resource agents for Ceph daemons
Group:		System Environment/Base
License:	LGPL-2.0
Requires:	%{name} = %{version}
Requires:	resource-agents
%description resource-agents
Resource agents for monitoring and managing Ceph daemons
under Open Cluster Framework (OCF) compliant resource
managers such as Pacemaker.
%endif

%package -n librados2
Summary:	RADOS distributed object store client library
Group:		System Environment/Libraries
License:	LGPL-2.0
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora}
Obsoletes:	ceph-libs
%endif
%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librbd1
Summary:	RADOS block device client library
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	librados2 = %{version}-%{release}
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora}
Obsoletes:	ceph-libs
%endif
%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n libcephfs1
Summary:	Ceph distributed file system client library
Group:		System Environment/Libraries
License:	LGPL-2.0
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora}
Obsoletes:	ceph-libs
%endif
%description -n libcephfs1
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n python-ceph
Summary:	Python libraries for the Ceph distributed filesystem
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	librados2 = %{version}-%{release}
Requires:	librbd1 = %{version}-%{release}
Requires:	python-flask
%if 0%{defined suse_version}
%py_requires
%endif
%description -n python-ceph
This package contains Python libraries for interacting with Cephs RADOS
object storage.

%package -n rest-bench
Summary:	RESTful benchmark
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	ceph-common = %{version}-%{release}
%description -n rest-bench
RESTful bencher that can be used to benchmark radosgw performance.

%package -n ceph-test
Summary:	Ceph benchmarks and test tools
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	librados2 = %{version}-%{release}
Requires:	librbd1 = %{version}-%{release}
Requires:	libcephfs1 = %{version}-%{release}
%description -n ceph-test
This package contains Ceph benchmarks and test tools.

%package -n libcephfs_jni1
Summary:	Java Native Interface library for CephFS Java bindings.
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	java
Requires:	libcephfs1 = %{version}-%{release}
BuildRequires:	java-devel
%description -n libcephfs_jni1
This package contains the Java Native Interface library for CephFS Java
bindings.

%package -n cephfs-java
Summary:	Java libraries for the Ceph File System.
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	java
Requires:	libcephfs_jni1 = %{version}-%{release}
BuildRequires:	java-devel
Requires:	junit4
BuildRequires:	junit4
%description -n cephfs-java
This package contains the Java libraries for the Ceph File System.

%if 0%{?opensuse} || 0%{?suse_version}
%debug_package
%endif

#################################################################################
# common
#################################################################################
%prep
%setup -q

%build
# Find jni.h
for i in /usr/{lib64,lib}/jvm/java/include{,/linux}; do
    [ -d $i ] && java_inc="$java_inc -I$i"
done

./autogen.sh
MY_CONF_OPT=""

MY_CONF_OPT="$MY_CONF_OPT --with-radosgw"

export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/i386/i486/'`

%{configure}	CPPFLAGS="$java_inc" \
		--prefix=/usr \
		--localstatedir=/var \
		--sysconfdir=/etc \
		--docdir=%{_docdir}/ceph \
		--with-nss \
		--without-cryptopp \
		--with-rest-bench \
		--with-debug \
		--enable-cephfs-java \
		$MY_CONF_OPT \
		%{?_with_ocf} \
		CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"

# fix bug in specific version of libedit-devel
%if 0%{defined suse_version}
sed -i -e "s/-lcurses/-lncurses/g" Makefile
sed -i -e "s/-lcurses/-lncurses/g" src/Makefile
sed -i -e "s/-lcurses/-lncurses/g" man/Makefile
sed -i -e "s/-lcurses/-lncurses/g" src/ocf/Makefile
sed -i -e "s/-lcurses/-lncurses/g" src/java/Makefile
%endif

make -j$(getconf _NPROCESSORS_ONLN)

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
install -D src/init-ceph $RPM_BUILD_ROOT%{_initrddir}/ceph
install -D src/init-radosgw.sysv $RPM_BUILD_ROOT%{_initrddir}/ceph-radosgw
install -D src/init-rbdmap $RPM_BUILD_ROOT%{_initrddir}/rbdmap
install -D src/rbdmap $RPM_BUILD_ROOT%{_sysconfdir}/ceph/rbdmap
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -sf ../../etc/init.d/ceph %{buildroot}/%{_sbindir}/rcceph
ln -sf ../../etc/init.d/ceph-radosgw %{buildroot}/%{_sbindir}/rcceph-radosgw
install -m 0644 -D src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph
install -m 0644 -D src/rgw/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/radosgw
chmod 0644 $RPM_BUILD_ROOT%{_docdir}/ceph/sample.ceph.conf
chmod 0644 $RPM_BUILD_ROOT%{_docdir}/ceph/sample.fetch_config

# udev rules
%if 0%{?rhel} >= 7
install -m 0644 -D udev/50-rbd.rules $RPM_BUILD_ROOT/usr/lib/udev/rules.d/50-rbd.rules
install -m 0644 -D udev/60-ceph-partuuid-workaround.rules $RPM_BUILD_ROOT/usr/lib/udev/rules.d/60-ceph-partuuid-workaround.rules
%else
install -m 0644 -D udev/50-rbd.rules $RPM_BUILD_ROOT/lib/udev/rules.d/50-rbd.rules
install -m 0644 -D udev/60-ceph-partuuid-workaround.rules $RPM_BUILD_ROOT/lib/udev/rules.d/60-ceph-partuuid-workaround.rules
%endif

%if (0%{?rhel} || 0%{?rhel} < 7)
install -m 0644 -D udev/95-ceph-osd-alt.rules $RPM_BUILD_ROOT/lib/udev/rules.d/95-ceph-osd.rules
%else
install -m 0644 -D udev/95-ceph-osd.rules $RPM_BUILD_ROOT/lib/udev/rules.d/95-ceph-osd.rules
%endif

%if 0%{?rhel} >= 7
mv $RPM_BUILD_ROOT/lib/udev/rules.d/95-ceph-osd.rules $RPM_BUILD_ROOT/usr/lib/udev/rules.d/95-ceph-osd.rules
mv $RPM_BUILD_ROOT/sbin/mkcephfs $RPM_BUILD_ROOT/usr/sbin/mkcephfs
mv $RPM_BUILD_ROOT/sbin/mount.ceph $RPM_BUILD_ROOT/usr/sbin/mount.ceph
mv $RPM_BUILD_ROOT/sbin/mount.fuse.ceph $RPM_BUILD_ROOT/usr/sbin/mount.fuse.ceph
%endif

#set up placeholder directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ceph
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/ceph
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ceph
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/tmp
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/mon
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/osd
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/mds
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/bootstrap-osd
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/bootstrap-mds
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/radosgw

%if %{defined suse_version}
# Fedora seems to have some problems with this macro, use it only on SUSE
%fdupes -s $RPM_BUILD_ROOT/%{python_sitelib}
%fdupes %buildroot
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add ceph
mkdir -p %{_localstatedir}/run/ceph/

%preun
%if %{defined suse_version}
%stop_on_removal ceph
%endif
if [ $1 = 0 ] ; then
    /sbin/service ceph stop >/dev/null 2>&1
    /sbin/chkconfig --del ceph
fi

%postun
/sbin/ldconfig
%if %{defined suse_version}
%insserv_cleanup
%endif


#################################################################################
# files
#################################################################################
%files
%defattr(-,root,root,-)
%docdir %{_docdir}
%dir %{_docdir}/ceph
%{_docdir}/ceph/sample.ceph.conf
%{_docdir}/ceph/sample.fetch_config
%{_bindir}/cephfs
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-rest-api
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-run
%{_bindir}/ceph-mon
%{_bindir}/ceph-mds
%{_bindir}/ceph-osd
%{_bindir}/ceph-rbdnamer
%{_bindir}/librados-config
%{_bindir}/ceph-client-debug
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-coverage
%{_bindir}/ceph_mon_store_converter
%{_initrddir}/ceph
%{_sbindir}/ceph-disk
%{_sbindir}/ceph-disk-activate
%{_sbindir}/ceph-disk-prepare
%{_sbindir}/ceph-disk-udev
%{_sbindir}/ceph-create-keys
%{_sbindir}/rcceph
%if 0%{?rhel} >= 7
%{_sbindir}/mkcephfs
%else
/sbin/mkcephfs
%endif
%if 0%{?rhel} >= 7
%{_sbindir}/mount.ceph
%else
/sbin/mount.ceph
%endif
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph_common.sh
%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/libcls_rbd.so*
%{_libdir}/rados-classes/libcls_hello.so*
%{_libdir}/rados-classes/libcls_rgw.so*
%{_libdir}/rados-classes/libcls_lock.so*
%{_libdir}/rados-classes/libcls_kvs.so*
%{_libdir}/rados-classes/libcls_refcount.so*
%{_libdir}/rados-classes/libcls_log.so*
%{_libdir}/rados-classes/libcls_replica_log.so*
%{_libdir}/rados-classes/libcls_statelog.so*
%{_libdir}/rados-classes/libcls_user.so*
%{_libdir}/rados-classes/libcls_version.so*
%dir %{_libdir}/ceph/erasure-code
%{_libdir}/ceph/erasure-code/libec_example.so*
%{_libdir}/ceph/erasure-code/libec_fail_to_initialize.so*
%{_libdir}/ceph/erasure-code/libec_fail_to_register.so*
%{_libdir}/ceph/erasure-code/libec_hangs.so*
%{_libdir}/ceph/erasure-code/libec_jerasure*.so*
%{_libdir}/ceph/erasure-code/libec_test_jerasure*.so*
%{_libdir}/ceph/erasure-code/libec_missing_entry_point.so*
%if 0%{?rhel} >= 7
/usr/lib/udev/rules.d/60-ceph-partuuid-workaround.rules
/usr/lib/udev/rules.d/95-ceph-osd.rules
%else
/lib/udev/rules.d/60-ceph-partuuid-workaround.rules
/lib/udev/rules.d/95-ceph-osd.rules
%endif
%config %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/logrotate.d/radosgw
%{_mandir}/man8/ceph-mon.8*
%{_mandir}/man8/ceph-mds.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/mkcephfs.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/ceph-rest-api.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/cephfs.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-debugpack.8*
%{_mandir}/man8/ceph-clsinfo.8.gz
%{_mandir}/man8/librados-config.8.gz
#set up placeholder directories
%dir %{_localstatedir}/lib/ceph/
%dir %{_localstatedir}/lib/ceph/tmp
%dir %{_localstatedir}/lib/ceph/mon
%dir %{_localstatedir}/lib/ceph/osd
%dir %{_localstatedir}/lib/ceph/mds
%dir %{_localstatedir}/lib/ceph/bootstrap-osd
%dir %{_localstatedir}/lib/ceph/bootstrap-mds
%ghost %dir %{_localstatedir}/run/ceph/

#################################################################################
%files -n ceph-common
%defattr(-,root,root,-)
%{_bindir}/ceph
%{_bindir}/ceph-authtool
%{_bindir}/ceph-conf
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-syn
%{_bindir}/ceph-crush-location
%{_bindir}/rados
%{_bindir}/rbd
%{_bindir}/ceph-post-file
%{_bindir}/ceph-brag
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/rbd.8*
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_datadir}/ceph/id_dsa_drop.ceph.com
%{_datadir}/ceph/id_dsa_drop.ceph.com.pub
%dir %{_sysconfdir}/ceph/
%dir %{_localstatedir}/log/ceph/
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/rbd
%config(noreplace) %{_sysconfdir}/ceph/rbdmap
%{_initrddir}/rbdmap

%postun -n ceph-common
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf /var/log/ceph
    rm -rf /etc/ceph
fi

#################################################################################
%files fuse
%defattr(-,root,root,-)
%{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*
%if 0%{?rhel} >= 7
%{_sbindir}/mount.fuse.ceph
%else
/sbin/mount.fuse.ceph
%endif

#################################################################################
%files -n rbd-fuse
%defattr(-,root,root,-)
%{_bindir}/rbd-fuse
%{_mandir}/man8/rbd-fuse.8*

#################################################################################
%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/buffer.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/rados_types.hpp
%{_includedir}/rados/memory.h
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/libcephfs.so
%{_libdir}/librbd.so
%{_libdir}/librados.so
%{_libdir}/libcephfs_jni.so

#################################################################################
%files radosgw
%defattr(-,root,root,-)
%{_initrddir}/ceph-radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*
%{_sbindir}/rcceph-radosgw
%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%dir %{_localstatedir}/log/radosgw/

%post radosgw
/sbin/ldconfig
%if %{defined suse_version}
%fillup_and_insserv -f -y ceph-radosgw
%endif

%preun radosgw
%if %{defined suse_version}
%stop_on_removal ceph-radosgw
%endif

%postun radosgw
/sbin/ldconfig
%if %{defined suse_version}
%restart_on_update ceph-radosgw
%insserv_cleanup
%endif
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf /var/log/radosgw
fi


#################################################################################
%if %{with ocf}
%files resource-agents
%defattr(0755,root,root,-)
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
%dir /usr/lib/ocf/resource.d/ceph
/usr/lib/ocf/resource.d/%{name}/*
%endif

#################################################################################
%files -n librados2
%defattr(-,root,root,-)
%{_libdir}/librados.so.*

%post -n librados2
/sbin/ldconfig

%postun -n librados2
/sbin/ldconfig

#################################################################################
%files -n librbd1
%defattr(-,root,root,-)
%{_libdir}/librbd.so.*
%if 0%{?rhel} >= 7
/usr/lib/udev/rules.d/50-rbd.rules
%else
/lib/udev/rules.d/50-rbd.rules
%endif

%post -n librbd1
/sbin/ldconfig
mkdir -p /usr/lib64/qemu/
ln -sf %{_libdir}/librbd.so.1 /usr/lib64/qemu/librbd.so.1

%postun -n librbd1
/sbin/ldconfig

#################################################################################
%files -n libcephfs1
%defattr(-,root,root,-)
%{_libdir}/libcephfs.so.*

%post -n libcephfs1
/sbin/ldconfig

%postun -n libcephfs1
/sbin/ldconfig

#################################################################################
%files -n python-ceph
%defattr(-,root,root,-)
%{python_sitelib}/rados.py*
%{python_sitelib}/rbd.py*
%{python_sitelib}/cephfs.py*
%{python_sitelib}/ceph_argparse.py*
%{python_sitelib}/ceph_rest_api.py*

#################################################################################
%files -n rest-bench
%defattr(-,root,root,-)
%{_bindir}/rest-bench

#################################################################################
%files -n ceph-test
%defattr(-,root,root,-)
%{_bindir}/ceph_bench_log
%{_bindir}/ceph_dupstore
%{_bindir}/ceph_kvstorebench
%{_bindir}/ceph_multi_stress_watch
%{_bindir}/ceph_erasure_code
%{_bindir}/ceph_erasure_code_benchmark
%{_bindir}/ceph_omapbench
%{_bindir}/ceph_psim
%{_bindir}/ceph_radosacl
%{_bindir}/ceph_rgw_jsonparser
%{_bindir}/ceph_rgw_multiparser
%{_bindir}/ceph_scratchtool
%{_bindir}/ceph_scratchtoolpp
%{_bindir}/ceph_smalliobench
%{_bindir}/ceph_smalliobenchdumb
%{_bindir}/ceph_smalliobenchfs
%{_bindir}/ceph_smalliobenchrbd
%{_bindir}/ceph_filestore_dump
%{_bindir}/ceph_filestore_tool
%{_bindir}/ceph_streamtest
%{_bindir}/ceph_test_*
%{_bindir}/ceph_tpbench
%{_bindir}/ceph_xattr_bench
%{_bindir}/ceph-monstore-tool
%{_bindir}/ceph-osdomap-tool
%{_bindir}/ceph-kvstore-tool

%files -n libcephfs_jni1
%defattr(-,root,root,-)
%{_libdir}/libcephfs_jni.so.*

%files -n cephfs-java
%defattr(-,root,root,-)
%{_javadir}/libcephfs.jar
%{_javadir}/libcephfs-test.jar

%changelog
