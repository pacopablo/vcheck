import clr
clr.AddReference('VMware.Vim')
from System.Collections.Specialized import NameValueCollection
from System import Array
import VMware.Vim
from vcheck.igetpass import getpass
#client = VMware.Vim.VimClient()
#srv = raw_input('Enter vSphere or ESXi hostname: ')
#uname = raw_input('Enter username [administrator]: ') or 'administrator'
#password = getpass('Enter password: ')
#lient.Connect('https://' + srv + '/sdk')
#client.Login(uname, password)
#hosts = client.FindEntityViews(VMware.Vim.HostSystem, None, None, None)
