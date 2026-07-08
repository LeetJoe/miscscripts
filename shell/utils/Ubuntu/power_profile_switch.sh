#!/bin/bash

# 适用于 Ubuntu26, 以 Wayland 为显示服务器的系统，使用 GNOME 桌面环境
PROFILE=$(powerprofilesctl get)

if [ "$PROFILE" == "performance" ]; then
    # === Performance 模式：屏幕常亮，不休眠 ===
    gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
    gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
    
    # 取消屏幕自动变黑
    gsettings set org.gnome.desktop.session idle-delay 0

elif [ "$PROFILE" == "balanced" ]; then
    # === Balance 模式：恢复超时熄屏和自动休眠 ===
    gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 600
    gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'suspend'
    
    gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 300
    gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'suspend'
    
    # 恢复屏幕 5 分钟(300秒)后自动变黑
    gsettings set org.gnome.desktop.session idle-delay 300
fi