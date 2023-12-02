import libvirt 
import os


def connectToHypervisor():
    # Se connecter à l'hyperviseur
    conn = libvirt.open("qemu:///system")
        # Vérifier si la connexion est réussie
    if conn is None:
        print('Échec de la connexion à l\'hyperviseur')
        exit(1)
    else: return conn 

#lister les machines virtuelles 
def listVMs():
    conn = connectToHypervisor()
    domains = conn.listAllDomains()
    if len(domains) == 0:
        print('Aucune machine virtuelle trouvée.')
    else:
        print('Liste des machines virtuelles :')
        for domain in domains:
            print('Nom :', domain.name())
            print('ID :', domain.ID())
            print('Etat :', domain.state())
            print('**************************************************')


#demarrer une machine virtuelle spécifique 
def startVM(vm_name):
    conn = connectToHypervisor()
    domain = conn.lookupByName(vm_name)
    if domain is None:
        print('Machine virtuelle non trouvée.')
        return
    else:
        domain.create()
        print(f'Machine virtuelle {vm_name} démarrée avec succès.')
    

#arreter une machine virtuelle 
def stopVM(vm_name):
    conn = connectToHypervisor()

    try:
        domain = conn.lookupByName(vm_name)
        if domain.isActive():  # Vérifier si la VM est active
            domain.destroy()  # Arrêter la VM

        print(f"La machine virtuelle {vm_name} a été arrêtée avec succès.")
    except libvirt.libvirtError as e:
        print(f"Erreur lors de l'arrêt de la machine virtuelle {vm_name}: {e}")
    finally:
        conn.close()  # Fermer la connexion à l'hyperviseur

#informations sur la vm 
def getInfoMv(info):
        print("\n")
        conn = connectToHypervisor()
        dom = conn.lookupByName(info)
        try:
            print('**********  Information de la machine virtuelle:')
            print('Powered : {}'.format('ON' if dom.isActive() else 'OFF'))
            print("Name : " + dom.name())
            print('ID : {}'.format('-' if dom.ID() == -1 else dom.ID()))
            print("UUID : " + str(dom.UUIDString()))
            print("Systeme d'exploitation : " + str(dom.OSType()))
            print("Maximum de memoire allouee: " + str(dom.maxMemory() / 1024))
            if dom.isActive():
                print("Maximum de nombre de VCPUs allouees: " + str(dom.maxVcpus()))
        except libvirt.libvirtError as e:
            print("Erreur lors de la recuperation d'information ")
            sys.exit(1)


#recuperer les infos de l'hyperviseur 
def getInfoHv():
        print("\n")
        try:
            conn = connectToHypervisor()
            infos = conn.getInfo()
            print("Information de l'hyperviseur :")
            print("Nom de l'hote :" + conn.getHostname())
            print("CPU : " + str(infos[0]))
            print("RAM en MB : " + str(infos[1]))
            print("Nombre de coeurs du CPU : " + str(infos[2]))
            print("Nombre de CPU par socket: " + str(infos[5]))
            print("Nombre de CPU coeurs par socket :" + str(infos[6]))
            print("Nombre de thread par coeur : " + str(infos[7]))
        except libvirt.libvirtError as e:
            print("Erreur lors de la recuperation de l'hyperviseur ")
            sys.exit(1)


#voir le status de la vm 
def getVMStatus(name):
    conn = connectToHypervisor()
    try:
        domain = conn.lookupByName(name)
        if domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
            print(f"La machine virtuelle {name} est allumée.")
        elif domain.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            print(f"La machine virtuelle {name} est éteinte.")
        else:
            print(f"La machine virtuelle {name} est dans un état inconnu.")
    except libvirt.libvirtError as e:
        print(f"Erreur : Impossible de trouver la machine virtuelle {name}.")

#lister les vms actives et inactives 
def listActiveVMs():
    conn = connectToHypervisor()
    active_domains = conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
    if len(active_domains) == 0:
        print('Aucune machine virtuelle active trouvée.')
    else:
        print('Liste des machines virtuelles actives :')
        for domain in active_domains:
            print('Nom :', domain.name())
            print('**************************************************')

def listInactiveVMs():
    conn = connectToHypervisor()
    inactive_domains = conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE)
    if len(inactive_domains) == 0:
        print('Aucune machine virtuelle inactive trouvée.')
    else:
        print('Liste des machines virtuelles inactives :')
        for domain in inactive_domains:
            print('Nom :', domain.name())
            print('**************************************************')

#visualiser une machine virtuelle 
def openVMConsole(name):
    conn = connectToHypervisor()
    domain = conn.lookupByName(name)
    if domain.isActive():
        os.system("virt-viewer " + name + " &")
    else:
        print("La machine virtuelle n'est pas active.")            


#recuperer les infos reseau d'une vm 
def getActiveVMNetworkInfo(name):
    conn=connectToHypervisor()
    
    try:
        domain = conn.lookupByName(name)
        if domain.isActive():
            print(f"Informations réseau pour la machine virtuelle '{name}':")
            interfaces = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)
            
            for (name, val) in interfaces.items():
                if val['addrs']:
                    print(f"Interface: {name}")
                    for ipaddr in val['addrs']:
                        print(f"   Adresse IP: {ipaddr['addr']}")
                        print(f"   Adresse MAC: {ipaddr['hwaddr']}")
                        print()
        else:
            print("La machine virtuelle n'est pas active.")
    except libvirt.libvirtError as e:
        print(f"Erreur lors de la récupération des informations réseau : {e}")        



def main():
    print("************************************************************************************************")
    print("***********     Bienvenue dans le gestionnaire de machines virtuelles!     *********************")
    while True:
        print("\nMenu :")
        print("1. Lister toutes les machines virtuelles")
        print("2. Démarrer une machine virtuelle")
        print("3. Arrêter une machine virtuelle")
        print("4. Obtenir des informations sur une machine virtuelle")
        print("5. Obtenir des informations sur l'hyperviseur")
        print("6. Voir le statut d'une machine virtuelle")
        print("7. Lister les machines virtuelles actives")
        print("8. Lister les machines virtuelles inactives")
        print("9. Ouvrir l'écran d'une machine virtuelle active")
        print("10. Obtenir des informations réseau d'une machine virtuelle active")
        print("0. Quitter")

        choice = input("Entrez le numéro correspondant à votre choix : ") 
        if choice == "1":
            listVMs()
        elif choice == "2":
            vm_name = input("Entrez le nom de la machine virtuelle à démarrer : ")
            startVM(vm_name)
        elif choice == "3":
            vm_name = input("Entrez le nom de la machine virtuelle à arrêter : ")
            stopVM(vm_name)
        elif choice == "4":
            vm_name = input("Entrez le nom de la machine virtuelle : ")
            getInfoMv(vm_name)
        elif choice == "5":
            getInfoHv()
        elif choice == "6":
            vm_name = input("Entrez le nom de la machine virtuelle : ")
            getVMStatus(vm_name)
        elif choice == "7":
            listActiveVMs()
        elif choice == "8":
            listInactiveVMs()
        elif choice == "9":
            vm_name = input("Entrez le nom de la machine virtuelle active : ")
            openVMConsole(vm_name)
        elif choice == "10":
            vm_name = input("Entrez le nom de la machine virtuelle active : ")
            getActiveVMNetworkInfo(vm_name)
        elif choice == "0":
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")       