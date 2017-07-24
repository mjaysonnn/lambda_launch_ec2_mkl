import boto3

user_data_script = """#!bin/bash
exec 2> /tmp/rc.local.log
exec 1>&2
set -x
cd /home/ubuntu
apt-get update -y
apt-get install cpio -y
apt-get install g++ -y
apt-get install make -y
wget http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11544/l_mkl_2017.3.196.tgz
tar -zxvf l_mkl_2017.3.196.tgz
cd l_mkl_2017.3.196
echo 'ACCEPT_EULA=accept' >> silent.cfg
./install.sh --silent silent.cfg
cd /home/ubuntu
echo 'source /opt/intel/mkl/bin/mklvars.sh intel64' >> /etc/profile
source /etc/profile
git clone https://github.com/mjaysonnn/MKL.git
chown -R ubuntu MKL
cd /home/ubuntu/MKL
su ubuntu -c export MKLROOT=/opt/intel/compilers_and_libraries_2017.4.196/linux/mkl
make 
./dgesv 3
"""


def lambda_handler(event, context):
    # client = boto3.client('ec2', region_name='us-west-2')
    # print (client)
    ec2 = boto3.client('ec2', region_name='us-west-2')

    response = ec2.run_instances(
        ImageId='ami-835b4efa',
        InstanceType='t2.micro',
        KeyName='macbook-mj',
        MinCount=1,
        MaxCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroups=['mj-security', ],
        UserData=user_data_script)

    print (response)




    # response = ec2.describe_instances()

    # print(response)
