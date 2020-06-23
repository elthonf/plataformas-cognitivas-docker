#$PROJECT_ID=curso-gcp-ml-tensorflow
#unset DEVSHELL_PROJECT_ID

# OBTENDO O PROJETO
if [ ! -z "$DEVSHELL_PROJECT_ID" ] && [ -z "$PROJECT_ID" ]
then
  PROJECT_ID=$DEVSHELL_PROJECT_ID
fi

if [ -z "$PROJECT_ID" ]
then
  read -p "Enter the project ID: "  PROJECT_ID
fi
#$PROJECT_ID=curso-gcp-ml-tensorflow

echo "Usando PROJECT_ID: $PROJECT_ID"


# OBTENDO O NOME DA MV
if [ $# -gt 0 ]; then # Se passar a data, usa o primeiro arrgumento
    VMNAME=$1
else                  #Nao passou a data
    VMNAME=vm-fiap-plataformas
fi


echo "Cria a máquina $VMNAME no projeto $PROJECT_ID"

gcloud compute --project=$PROJECT_ID instances create $VMNAME \
  --zone=us-east1-b \
  --machine-type=n1-standard-1 --subnet=default \
  --tags=http-server,https-server,fiap-plataformas \
  --image=ubuntu-1804-bionic-v20200529 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=$VMNAME \
  --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring


FIRENAME=firewall-fiap-plataformas-02
echo "Cria a regra de firewall $FIRENAME no projeto $PROJECT_ID"

gcloud compute --project=$PROJECT_ID firewall-rules create $FIRENAME \
   --description=Libera\ portas\ necess\árias\ para\ pr\áticas\ de\ plataformas\ cognitivas \
   --direction=INGRESS --priority=1000 --network=default --action=ALLOW \
   --rules=tcp:8080,tcp:8081,tcp:5000,tcp:1234,tcp:1235,tcp:1236,tcp:1237 \
   --source-ranges=0.0.0.0/0 \
   --target-tags=fiap-plataformas

