import paramiko.auth_strategy
import paramiko.client


def foo():
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname="35.153.228.11", username="ec2-user", password="datacore_pc1"
        )

        local_path = "hola_mundo.py"
        remote_path = "/home/ec2-user/hola_mundo.py"

        # ftp_client = client.open_sftp()
        # ftp_client.put(local_path, remote_path)
        # ftp_client.close()

        stdin, stdout, stderr = client.exec_command("python hola_mundo.py")
        output = stdout.read().decode()
        error = stderr.read().decode()

        print(output)
        print(error)

        client.close()
    except Exception as e:
        print(e.with_traceback())


foo()
