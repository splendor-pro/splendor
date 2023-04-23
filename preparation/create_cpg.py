import os
import sys
import paramiko
client = paramiko.SSHClient()

#
def create_cpg(target_dir):
    try:
        # create ast
        os.system("cd "+target_dir+"&&phpjoern")

        # create cpg
        os.system("cd "+target_dir+"&&java -jar joern.jar nodes.csv rels.csv")

        # upload the cpg
        cpg_upload(target_dir)

        # start neo4j
        start_neo4j()
        # return
        return True
    except Exception as e:
        print(e)
        return False


#
ssh_ip = "x.x.x.x"
user_name = "root"
password = "root"

def cpg_upload(target_dir):
        #
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(ssh_ip, username=user_name, password=password)
    sftp = ssh.open_sftp()
    nodes = target_dir+"/nodes.csv"
    rels = target_dir+"/rels.csv"
    cpgs = target_dir+"/cpg_edges.csv"
    sftp.put(localpath=nodes, remotepath="/tmp/nodes.csv")
    sftp.put(localpath=rels, remotepath="/tmp/rels.csv")
    sftp.put(localpath=cpgs, remotepath="/tmp/cpg_edges.csv")
    ssh.close()    

#
def start_neo4j(move=True):
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_ip, username=user_name, password=password)
    client.exec_command('neo4j stop')
    client.close()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_ip, username=user_name, password=password)
    if move == True:
        # load the cpg into the neo4j
        client.exec_command('mv /tmp/nodes.csv /tmp/rels.csv /tmp/cpg_edges.csv /root/neo4j/batch_importer_21/')
        stdin, stdout, stderr = client.exec_command('cd /root/neo4j/batch_importer_21/&&sh cpg2neo4j.sh')
        for line in stdout:
            print("... " + line.strip('\n'))
    stdin, stdout, stderr = client.exec_command('neo4j start-no-wait')
    for line in stdout:
        print("... " + line.strip('\n'))
    #
    client.close()   

if __name__ == '__main__':
    create_cpg(sys.argv[1])