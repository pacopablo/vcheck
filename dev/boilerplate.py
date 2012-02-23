import clr
clr.AddReference('VMware.Vim')
from System.Collections.Specialized import NameValueCollection
from System import Array
import VMware.Vim
client = VMware.Vim.VimClient()
srv = raw_input('Enter vSphere or ESXi hostname: ')
uname = raw_input('Enter username [administrator]: ') or 'administrator'
password = raw_input('Enter password: ')
client.Connect('https://' + srv + '/sdk')
client.Login(uname, password)
hosts = client.FindEntityViews(VMware.Vim.HostSystem, None, None, None)
