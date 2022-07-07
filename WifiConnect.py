import os
def connect(goal_ssid,goal_pw):
    # "" important in wpa.conf or it would not work
    goal_ssid = '"' + goal_ssid + '"'   
    goal_pw = '"' + goal_pw + '"'
    
    # Reconfigure goal wifi and key in line 6 and 7 of wpa_supplicant.conf
    cm = "sudo sed -i '7s/.*/   ssid=" + goal_ssid + "/' /etc/wpa_supplicant/wpa_supplicant.conf" # using % does not work with all the "" being important in the wpa.conf
    os.system(cm)
    cm = "sudo sed -i '8s/.*/   psk=" + goal_pw + "/' /etc/wpa_supplicant/wpa_supplicant.conf" # using % does not work with all the "" being important in the wpa.conf
    os.system(cm)

    # Activate new configuration
    cm = "sudo wpa_cli -i wlan0 reconfigure"
    os.system(cm)

# connect("PYUR D654F_2.4", "08111996")
