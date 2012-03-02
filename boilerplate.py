# This is meant to be run inside the interactive python window in Visual Studio
# To make sure imports work properly, highlight the code, right-click and select
# "Send to Interactive", or press Ctrl-E, Ctrl E
import clr
clr.AddReference('VMware.Vim')
from System.Collections.Specialized import NameValueCollection
from System import Array
import VMware.Vim
from ipgetpass import getpass
client = VMware.Vim.VimClient()
srv = raw_input('Enter vSphere or ESXi hostname: ')
uname = raw_input('Enter username [administrator]: ') or 'administrator'
# getpass does not work in the REPL, so the password you enter below will appear in
# plain text
password = raw_input('Enter password: ')
client.Connect('https://' + srv + '/sdk')
client.Login(uname, password)
hosts = client.FindEntityViews(VMware.Vim.HostSystem, None, None, None)

client.Connect('https://10.140.0.106/sdk')
client.Login(uname, password)

hosts = client.FindEntityViews(VMware.Vim.HostSystem, None, None, None)
ns = client.GetView(hosts[0].ConfigManager.NetworkSystem, None)

ns.RemoveVirtualSwitch('vSwitch')
bonded_nics = Array[str](['vmnic0', 'vmnic1'])
#linkdiscovery = VMware.Vim.LinkDiscoveryProtocolConfig()
#linkdiscovery.Operation = 'listen'
#linkdiscovery.Protocol = 'cdp'
#beacon = VMware.Vim.HostVirtualSwitchBeaconConfig()
#beacon.Interval = 1
vSwitch_bridge = VMware.Vim.HostVirtualSwitchBondBridge()
vSwitch_bridge.NicDevice = bonded_nics
#vSwitch_bridge.LinkDiscoveryProtocolConfig = linkdiscovery
#vSwitch_bridge.Beacon = beacon
nicorder = VMware.Vim.HostNicOrderPolicy()
nicorder.ActiveNic = Array[str](['vmnic0', 'vmnic1'])
nicorder.StandbyNic = Array[str]([])
failure = VMware.Vim.HostNicFailureCriteria()
failure.CheckBeacon = False
failure.CheckDuplex = False
failure.CheckErrorPercent = False
failure.CheckSpeed = 'minimum'
failure.FullDuplex = False
failure.Percentage = 0
failure.Speed = 10
nicteaming = VMware.Vim.HostNicTeamingPolicy()
nicteaming.FailureCriteria = failure
nicteaming.NicOrder = nicorder
nicteaming.NotifySwitches = True
nicteaming.Policy = 'loadbalance_ip'
nicteaming.ReversePolicy = True
nicteaming.RollingOrder = False
security = VMware.Vim.HostNetworkSecurityPolicy()
security.ForgedTransmits = True
security.MacChanges = True
security.AllowPromiscuous = False
shaping = VMware.Vim.HostNetworkTrafficShapingPolicy()
shaping.Enabled = False
vSwitch_policy = VMware.Vim.HostNetworkPolicy()
vSwitch_policy.NicTeaming = nicteaming
vSwitch_policy.Security = security
vSwitch_policy.ShapingPolicy = shaping
vSwitch = VMware.Vim.HostVirtualSwitchSpec()
vSwitch.NumPorts = 128
vSwitch.Mtu = 9000
vSwitch.Bridge = vSwitch_bridge
vSwitch.Policy = vSwitch_policy

try:
    ns.AddVirtualSwitch('vSwitch', vSwitch)
except VMware.Vim.VimException, e:
    print "Error buddy.  Check e"
    
ns.UpdateViewData()
ns.NetworkConfig.Vswitch[1]
ns.NetworkConfig.Vswitch[1].Spec.Bridge.LinkDiscoveryProtocolConfig

