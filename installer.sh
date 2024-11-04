#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo -e "[\033[0;35m\e[1mVOID\e[0m\033[0m][$(date +"%H:%M:%S")]: Ejecuta el script como root"
  exit
fi

if [ -f /etc/os-release ]; then
  . /etc/os-release
  DISTRO=$ID
else
  echo "No se pudo detectar la distribución."
  exit 1
fi

echo -e "\033[0;35m
            _    __
 _  _____  (_)__/ /
| |/ / _ \/ / _  / 
|___/\___/_/\_,_/  
                   
[*] Github: github.com/v019-exe
[*] Script hecha por v019.exe
[*] OS: $DISTRO
\033[0m"

install_python() {
    if command -v apt &> /dev/null; then
        sudo apt update -qq > /dev/null
        sudo apt install python3 -y -qq > /dev/null
    elif command -v yum &> /dev/null; then
        sudo yum install python3 -y -q > /dev/null
    elif command -v dnf &> /dev/null; then
        sudo dnf install python3 -y -q > /dev/null
    elif command -v zypper &> /dev/null; then
        sudo zypper install python3 -y -q > /dev/null
    else
        echo -e "${RED}No se pudo detectar el gestor de paquetes. Por favor, instala Python manualmente.${RESET}"
        exit 1
    fi
}

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python no está instalado. Procediendo a instalarlo...${RESET}"
    install_python
else
    echo -e "${GREEN}Python ya está instalado.${RESET}"
fi

if ! command -v pip &> /dev/null; then
    if command -v apt &> /dev/null; then
        sudo apt install python3-pip -y -qq > /dev/null
    elif command -v yum &> /dev/null; then
        sudo yum install python3-pip -y -q > /dev/null
    elif command -v dnf &> /dev/null; then
        sudo dnf install python3 -y -q > /dev/null
    elif command -v zypper &> /dev/null; then
        sudo zypper install python3-pip -y -q > /dev/null
    else
        echo -e "${RED}No se pudo detectar el gestor de paquetes. Por favor, instala pip manualmente.${RESET}"
        exit 1
    fi
else
    echo -e "${GREEN}pip ya está instalado.${RESET}"
fi

echo -e "[VOID INSTALLER][$(date +"%H:%M:%S")]: Descargando el script docusort"
curl -s -o docusort.py ""

if [ $? -ne 0 ]; then
    echo -e "[VOID INSTALLER][$(date +"%H:%M:%S")]: Error al descargar el script"
    exit 1
fi

if [ ! -f docusort.py ]; then
    echo -e "[VOID INSTALLER][$(date +"%H:%M:%S")]: El archivo docusort.py no se ha descargado correctamente"
fi

chmod +x docusort.py
mv docusort.py /usr/local/bin/docusort.py


echo -e "[VOID INSTALLER][$(date +"%H:%M:%S")]: Creando wrapper..."
cat << EOF | sudo tee /usr/local/bin/docusort-wrapper > dev/null
#!/bin/bash
python3 /usr/local/bin/docusort.py "\$@"
EOF

sudo chmod +x /usr/local/bin/docusort-wrapper
echo "alias docusort='/usr/local/bin/docusort-wrapper'" >> ~/.bashrc
echo -e "[VOID INSTALLER][$(date +"%H:%M:%S")]: Comando creado, docusort"
echo -e "[VOID INSTALLER][$(date +"%H:%M:%S")]: Instalación completada correctamente"
