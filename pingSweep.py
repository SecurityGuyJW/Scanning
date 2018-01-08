# This program takes a text file with a list of domains in them and stores the IP address,
# finally it will ping sweep the list of IPs and will display if they recieve ICMP request

import sh
import re


# When we pull the file using the sh.find() we get a trailing /n at the end of the file, we have to remove that character [,-1]


def format_file(x):
    x = str(x)

    x = list(x)

    x = x[:-1]

    x = ''.join(x)

    return x


# we store the domains in  an array
def store_domains(file_dir):
    domain_list = []

    for i in file_dir:
        domain_list.append(i)

    for i in range(len(domain_list)):
        domain_list[i] = domain_list[i].rstrip()

    return domain_list


# we take the domains and extract their IPV4 address
def convert_to_IP(domains):
    list_of_IPs = []

    count = 0

    for i in domains:

        ip = str(sh.host(i))

        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip)

        if len(ip) == 1:
            list_of_IPs.append(ip)

        else:
            for x in ip:
                list_of_IPs.append(x)

    return list_of_IPs


# now we ping the IPs in the arrays
def ping_sweep_IP(IP):

    for i in (IP):

	var = str(i)

        var = var.strip('[]')

        var = var.replace('\'','')

        print(sh.ping('-c','5', var))


def main():
    # these two values store the domains and the IPs
    list_of_domains = []
    list_of_IPs = []

    # uses bash script to find the domain list txt
    var = sh.find('.', '-name', 'clean_google.txt')

    # removes all unnessesary characters
    var = format_file(var)

    # opens the file containing the list of domains
    f = open(var, 'r')

    # stores list of domains in an array
    list_of_domains = store_domains(f)

    list_of_IPs = convert_to_IP(list_of_domains)

    ping_sweep_IP(list(list_of_IPs))


main()
