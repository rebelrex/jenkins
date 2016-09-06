pkill ceph
pkill ceph-osd
umount /dev/vdb1
umount /dev/vdb2
umount /dev/vdb3
mkfs.xfs -f /dev/vdb1
mkfs.xfs -f /dev/vdb2
mkfs.xfs -f /dev/vdb3
rm -rf /tmp/ceph.mon.keyring /tmp/monmap
rm -rf /data
rm -rf /etc/ceph/ceph.mds.a.keyring /etc/ceph/ceph.client.admin.keyring /etc/ceph/rbdmap