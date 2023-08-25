# ec2-ssm-connect

An interactive command-line tool to list Amazon EC2 instances and establish secure connections using AWS Systems Manager (SSM) Session Manager.

## 🚀 Installation

Before using this tool, ensure you have the AWS CLI installed. This tool depends on it.

pip install ec2-ssm-connect


## 🛠 Usage

After installation, you can use the command:

```
ec2-ssm-connect
```

To filter EC2 instances by name:

ec2-ssm-connect --filter [INSTANCE_NAME]


## 📦 Dependencies

- **boto3**: For AWS SDK functionalities.
- **AWS CLI**: Required for establishing connections with EC2 instances.

## ✍️ Author

- **Ingo Marlos Batista de Sousa**

## 📜 License

This project is licensed under the MIT License.

