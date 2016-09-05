#!/bin/sh

rpmdev-setuptree
cp $WORKSPACE/ceph.spec /root/rpmbuild/SPECS
cp $WORKSPACE/ceph-0.80.5.tar.gz /root/rpmbuild/SOURCES
rpmbuild -bb /root/rpmbuild/SPECS/ceph.spec