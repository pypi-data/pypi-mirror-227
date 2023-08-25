# ec2-ssm-connect

An interactive command-line tool to list Amazon EC2 instances and establish secure connections using AWS Systems Manager (SSM) Session Manager.


## 🚀 Installation

Before using this tool, ensure you have the AWS CLI installed. This tool depends on it. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

``` bash
pip install ec2-ssm-connect
```

## 🛠 Usage
** The application reads the AWS CLI credentials from the environment variables. **
After installation, you can use the command:

``` bash
ec2-ssm-connect
```

To filter EC2 instances by name:

``` bash
ec2-ssm-connect --filter [INSTANCE_NAME]
```

Example:

``` bash
$ ec2-ssm-connect
1. ID: i-0bb72e6f61ef2s612   Name: acme-aws-int-keycloak-ec2
2. ID: i-0819d17cdf4ees213   Name: acme-aws-int-auth-proxy-ec2
3. ID: i-082949bfd9b12s7cf   Name: acme-aws-int-auth-app-ec2
4. ID: i-0caaf2ffbb132se5b   Name: acme-aws-int-auth-web-ec2
5. ID: i-0dd580f86932as157   Name: jenkins-int-instance
6. ID: i-001bfa8b72680s6d9   Name: vault-int-ecs-instance
7. ID: i-0295e01f6bc12se68   Name: server01-int-ecs-instance
Enter the number of the EC2 instance you want to connect to: [HERE YOU ENTER THE NUMBER OF THE INSTANCE YOU WANT TO CONNECT TO, IN THIS CASE 1 TO 7]

$ ec2-ssm-connect -f jenkins
1. ID: i-0dd580f86932as157   Name: jenkins-int-instance
Enter the number of the EC2 instance you want to connect to: [HERE YOU ENTER THE NUMBER OF THE INSTANCE YOU WANT TO CONNECT TO, IN THIS CASE ONLY 1 IS POSSIBLE]
```




## 📦 Dependencies

- **boto3**: For AWS SDK functionalities.
- **AWS CLI**: Required for establishing connections with EC2 instances.

## ✍️ Author

- **Ingo Marlos Batista de Sousa**

## 📜 License

This project is licensed under the MIT License.





