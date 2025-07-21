#!/system/bin/sh
# system-cert.sh

# 创建临时目录用于备份证书
mkdir -m 700 /data/local/tmp/htk-ca-copy

# 备份现有的系统CA证书
cp /system/etc/security/cacerts/* /data/local/tmp/htk-ca-copy/

# 在证书目录上挂载临时文件系统
mount -t tmpfs tmpfs /system/etc/security/cacerts

# 将备份的证书恢复到系统目录
mv /data/local/tmp/htk-ca-copy/* /system/etc/security/cacerts/

# 复制新的证书文件
cp /data/local/tmp/9a5ba575.0 /system/etc/security/cacerts/

# 设置证书文件的所有者
chown root:root /system/etc/security/cacerts/*

# 设置证书文件权限
chmod 644 /system/etc/security/cacerts/*

# 设置SELinux上下文
chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*

# 清理临时目录
rm -r /data/local/tmp/htk-ca-copy

echo "System cert successfully injected"