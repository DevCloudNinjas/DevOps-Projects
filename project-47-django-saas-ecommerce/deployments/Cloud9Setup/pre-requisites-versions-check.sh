#!/bin/bash
SUMMARY="Make sure all the pre-requisites checks PASS"$'\n'
check_version() {
  retval=0  
  MIN_VERSION=$1
  CURRENT_VERSION=$2
  IFS='.' read -r -a minarr <<< "$MIN_VERSION"
  IFS='.' read -r -a currarr <<< "$CURRENT_VERSION"
  
  for ((i=0; i<${#minarr[@]}; i++));
  do
    #echo "${currarr[$i]}, ${minarr[$i]}"
    if [[ ${currarr[$i]} -gt ${minarr[$i]} ]]; then
        break
    elif [[ ${currarr[$i]} -lt ${minarr[$i]} ]]; then
        retval=1
        break
    else
        continue
    fi        
  done

  return $retval  
}

echo "Checking python version"
python3 --version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d'n' -f 2 | xargs)
PYTHON_MIN_VERSION=3.8.0
check_version $PYTHON_MIN_VERSION $PYTHON_VERSION
if [[ $? -eq 1 ]]; then
    echo "ACTION REQUIRED: Need to have python version greater than or equal to $PYTHON_MIN_VERSION"
    SUMMARY+="* ACTION REQUIRED: Need to have python version greater than or equal to $PYTHON_MIN_VERSION"$'\n'
else 
    SUMMARY+="* PASS : Python version $PYTHON_VERSION installed. The minimum required version $PYTHON_MIN_VERSION"$'\n'
fi
echo ""

echo "Checking aws cli version"
aws --version
if [[ $? -ne 0 ]]; then
     echo "ACTION REQUIRED: aws cli is missing, please install !!" 
     SUMMARY+="* ACTION REQUIRED: aws cli is missing, please install !!"$'\n'
else 
    AWS_VERSION=$(aws --version | cut -d'P' -f 1 | xargs)
    SUMMARY+="* PASS : $AWS_VERSION version installed"$'\n'
    jq --version
    if [[ $? -ne 0 ]]; then
        echo yes | sudo yum install jq
    fi    
    CLOUD9_INSTANCE=$(aws ec2 describe-instances --filters Name=instance-type,Values=t3.large | jq -r '.Reservations[0].Instances[0].InstanceId')
    if [ -z $CLOUD9_INSTANCE ]; then
        echo "ACTION REQUIRED: Looks like Cloud9 instance with t3.large instance type is missing. Please create one!!"
        SUMMARY+="* ACTION REQUIRED: Looks like Cloud9 instance with t3.large instance type is missing. Please create one!!"$'\n'
    else
        SUMMARY+="* PASS : Has required t3.large instance type"$'\n' 
        CLOUD9_INSTANCE_VOLUME_ID=$(aws ec2 describe-instances --filters Name=instance-type,Values=t3.large | jq -r '.Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId')
        VOLUME_SIZE=$(aws ec2 describe-volumes --volume-ids $CLOUD9_INSTANCE_VOLUME_ID | jq -r '.Volumes[0].Size')
        if [[ $VOLUME_SIZE -lt 50 ]]; then
            echo "ACTION REQUIRED: The volume size of cloud9 is less than 50GiB. Please update volume size to atleast 50GiB"
            SUMMARY+="* ACTION REQUIRED: The volume size of cloud9 is less than 50GiB. Please update volume size to atleast 50GiB"$'\n'
        else
            SUMMARY+="* PASS : Has minimum required 50GiB volume size"$'\n'
        fi
    fi
fi
echo ""

echo "Checking sam cli version"
sam --version
SAM_VERSION=$(sam --version | cut -d'n' -f 2 | xargs)
SAM_MIN_VERSION=1.20.0
check_version $SAM_MIN_VERSION $SAM_VERSION
if [[ $? -eq 1 ]]; then
    echo "ACTION REQUIRED: Need to have SAM version greater than or equal to $SAM_MIN_VERSION"
    SUMMARY+="* ACTION REQUIRED: Need to have SAM version greater than or equal to $SAM_MIN_VERSION"$'\n'
else
    SUMMARY+="* PASS : Sam cli version $SAM_VERSION installed. The minimum required version $SAM_MIN_VERSION"$'\n'
fi
echo ""

echo "Checking git-remote-codecommit version"
python3 -m pip show git-remote-codecommit
if [[ $? -ne 0 ]]; then
    echo "ACTION REQUIRED: git-remote-codecommit is missing, please install"
    SUMMARY+="* ACTION REQUIRED: git-remote-codecommit is missing, please install !!"$'\n'
else
    SUMMARY+="* PASS : Has git-remote-codecommit installed"$'\n'
fi
echo ""

echo "Checking node version"
node --version
NODE_VERSION=$(node --version | cut -d'v' -f 2)
NODE_MIN_VERSION=16.0.0
check_version $NODE_MIN_VERSION $NODE_VERSION 
if [[ $? -eq 1 ]]; then
    echo "ACTION REQUIRED: Need to have Node version greater than or equal to $NODE_MIN_VERSION"
    SUMMARY+="* ACTION REQUIRED: Need to have Node version greater than or equal to $NODE_MIN_VERSION"$'\n'
else
    SUMMARY+="* PASS : Node version $NODE_VERSION installed. The minimum required version $NODE_MIN_VERSION"$'\n'
fi
echo ""


echo "Checking cdk version"
cdk --version
CDK_VERSION=$(cdk --version | cut -d'(' -f 1| xargs)
CDK_MIN_VERSION=2.40.0
check_version $CDK_MIN_VERSION $CDK_VERSION
if [[ $? -eq 1 ]]; then
    echo "ACTION REQUIRED: Need to have CDK version greater than or equal to $CDK_MIN_VERSION"
    SUMMARY+="* ACTION REQUIRED: Need to have CDK version greater than or equal to $CDK_MIN_VERSION"$'\n'
else 
    SUMMARY+="* PASS : CDK version $CDK_VERSION installed. The minimum required version $CDK_MIN_VERSION"$'\n'
fi
echo ""

echo "***************SUMMARY****************"
echo "$SUMMARY"
echo "***************END OF SUMMARY*********"
