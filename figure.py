import os
from os.path import join, basename
import sys
import random
random.seed(0)
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from json import load


# Hyperparameters
run_stats = int(sys.argv[1]) if len(sys.argv) > 1 else 0 # 1 to run stats.py for all csv file
url_to_pkt_size = {
    'example.com' : 81,
    'plus.google.com' : 81,
    'www.bittorrent.com': 81,
    'www.roxypalace.com': 81,
    'www.survive.org.uk': 81,
    'www.youporn.com': 81,
    'empty_url_': 66
}
scan_to_flag = {
    'zmap/scan/scan1' : 'SYN',
    # 'zmap/scan/scan2' : 'PSH',
    # 'zmap/scan/scan3' : 'PSH+ACK',
    'zmap_multiple_probes/scan/scan4' : '<SYN;PSH>',
    'zmap_multiple_probes/scan/scan5' : '<SYN;PSH+ACK>'
}
scan_to_hdr_size = {key:14 if not 'multiple' in key else 28 for key in scan_to_flag.keys()}
urls = list(url_to_pkt_size.keys())
scans = list(scan_to_flag.keys())
# headers = 'saddr,len,payloadlen,flags,validation_type'.split(',')


# analyze raw results by stats.py
if run_stats:
    for scan in scans:
        for url in urls:
            csv_file = join(scan, '{}_{}.csv'.format(basename(scan), url))
            os.system('python stats.py {} {}'.format(csv_file, url_to_pkt_size[url]+scan_to_hdr_size[scan]))


# calculate amplification factor and total receiving data size in bytes for each unique ip
all_ips = []
for scan in scans:
    for url in urls:
        result_file = join(scan, '{}_{}_total_by_ip_bytes.txt'.format(basename(scan), url))
        with open(result_file, 'r') as f:
            for line in f.readlines():
                _, ip, _ = line.split()
                all_ips.append(ip)
all_ips = list(set(all_ips))

ip_to_index = {ip:i for i, ip in enumerate(all_ips)} # for better time efficiency
amp_factor = np.zeros((len(all_ips), len(urls), len(scans))) # n*i*j
receive_data_size = np.zeros_like(amp_factor)
for j, scan in tqdm(enumerate(scans), ascii=True, desc='Reading results of all scans', total=len(scans)):
    for i, url in enumerate(urls):
        result_file = join(scan, '{}_{}_total_by_ip_bytes.txt'.format(basename(scan), url))
        with open(result_file, 'r') as f:
            for line in f.readlines():
                byte, ip, _ = line.split()
                byte = int(byte)
                n = ip_to_index[ip]
                send_pkt_size = url_to_pkt_size[url]+scan_to_hdr_size[scan]
                assert amp_factor[n,i,j] == 0 and receive_data_size[n,i,j] == 0
                amp_factor[n,i,j] = byte/send_pkt_size
                receive_data_size[n,i,j] = byte
print('Number of unique ips: {}'.format(len(all_ips)))


# figure 1: maximum amplification factor per ip based on multiple scans
print('\n*****')
y = amp_factor.mean(axis=(1,2))
x = np.array(range(len(y)))+1
y_old = 10**(8-(8/6)*np.log10(x))
desc_order = np.argsort(y)[::-1]
fig, ax = plt.subplots(figsize=(6,4))
ax.set_xscale('log')
ax.set_yscale('log')
ax.tick_params(left=True, bottom=True, direction='in')
ax.tick_params(axis='x', which='minor', direction='in')
ax.tick_params(axis='y', which='minor', direction='in')
ax.set_axisbelow(True)
ax.grid(linestyle='--')
ax.plot(x, y[desc_order], label='April 2023', color='#0000FF')
ax.plot(x, y_old, ':', label='April 2020\n(Approx.)', color='#0000FF')
ax.set_xlabel('IP Address Rank', weight='bold', fontsize=12)
ax.set_ylabel('Amplification Factor', weight='bold', fontsize=12)
plt.legend(fontsize=12)
plt.savefig('figure1.png', bbox_inches='tight')
plt.close('all')
print('Saved figure1.png')
print('*****')

# figure 2: amplification factor for quack ips
print('\n*****')
quack_file = 'quack/genevadata.txt'
y = []
with open(quack_file, 'r') as f:
    total_lines = f.readlines()
    for line in total_lines:
        ip, url = line.split()
        if ip in ip_to_index:
            index = ip_to_index[ip]
            y.append(np.max(amp_factor[index]))
print('Number of ips in quack: {}'.format(len(total_lines)))
print('Number of quack ips scanned: {}'.format(len(y)))
print('*****')

# figure 4: amplification factor for www.youporn.com for every scan 
print('\n*****')
url = 'www.youporn.com'
y = amp_factor[:, urls.index(url),:]
x = np.array(range(y.shape[0]))+1
fig, ax = plt.subplots(figsize=(6,4))
ax.set_xscale('log')
ax.set_yscale('log')
ax.tick_params(left=True, bottom=True, direction='in')
ax.tick_params(axis='x', which='minor', direction='in')
ax.tick_params(axis='y', which='minor', direction='in')
ax.set_axisbelow(True)
ax.grid(linestyle='--')
for i in range(y.shape[1]):
    y_each = y[:,i]
    desc_order = np.argsort(y_each)[::-1]
    ax.plot(x, y_each[desc_order], label=scan_to_flag[scans[i]])
ax.set_xlabel('IP Address Rank', weight='bold', fontsize=12)
ax.set_ylabel('Amplification Factor', weight='bold', fontsize=12)
plt.legend(fontsize=12)
plt.savefig('figure4.png', bbox_inches='tight')
plt.close('all')
print('Saved figure4.png')
print('*****')

# figure 5: amplification factor for <SYN;PSH+ACK> for every url
print('\n*****')
flag = '<SYN;PSH+ACK>'
flog_to_scan = {val:key for key, val in scan_to_flag.items()}
y = amp_factor[:, :, scans.index(flog_to_scan[flag])]
x = np.array(range(y.shape[0]))+1
fig, ax = plt.subplots(figsize=(6,4))
ax.set_xscale('log')
ax.set_yscale('log')
ax.tick_params(left=True, bottom=True, direction='in')
ax.tick_params(axis='x', which='minor', direction='in')
ax.tick_params(axis='y', which='minor', direction='in')
ax.set_axisbelow(True)
ax.grid(linestyle='--')
for i in range(y.shape[1]):
    y_each = y[:,i]
    desc_order = np.argsort(y_each)[::-1]
    ax.plot(x, y_each[desc_order], label=urls[i])
ax.set_xlabel('IP Address Rank', weight='bold', fontsize=12)
ax.set_ylabel('Amplification Factor', weight='bold', fontsize=12)
plt.legend(fontsize=10)
plt.savefig('figure5.png', bbox_inches='tight')
plt.close('all')
print('Saved figure5.png')
print('*****')

# figure 8: countries
print('\n*****')
output_npy_file = 'figure_ip_to_country.npy'
num_ip_to_find = 20000
if os.path.exists(output_npy_file):
    ip_to_country = np.load(output_npy_file, allow_pickle=True).item()
    print('Loaded country information for {} amplifying IPs'.format(len(ip_to_country)))
else:
    def get_ip_country(result_dict, addr):
        req = Request(
            url='https://ipinfo.io/' + addr + '?token=8695e0f699fa56', 
            headers={'User-Agent': 'XYZ/3.0'}
        )
        try:
            res = urlopen(req)
        except:
            return 0
        data = load(res)
        result_dict[ip] = data['country']
        return 1

    amp_ips = np.array(all_ips)[amp_factor.max(axis=(1,2))>1]
    subsample_amp_ips = random.choices(amp_ips, k=num_ip_to_find)
    ip_to_country = {}
    success = 0
    for ip in tqdm(subsample_amp_ips, ascii=True, desc='Find country for {} amplifying ip'.format(num_ip_to_find)):
        result = get_ip_country(ip_to_country, ip)
        success += result
    print('Successfully located {} IPs'.format(success))
    np.save(output_npy_file, ip_to_country, allow_pickle=True)
unique_countries, counts = np.unique(list(ip_to_country.values()), return_counts=True)
desc_order = np.argsort(counts)[::-1]

# specific plots for most amplifying countries
country_names = {
    'US' : "United States",
    'CN' : 'China',
    'RU' : 'Russia',
    'HK' : 'Hong Kong',
    'TW' : 'Taiwan',
    'KR' : 'South Korea',
    'IR' : 'Iran',
    'EG' : 'Egypt',
    'BD' : 'Bangladesh',
    'SA' : 'Saudi Arabia',
    'OM' : 'Oman',
    'QA' : 'Qatar',
    'UZ' : 'Uzbekistan',
    'KW' : 'Kuwait',
    'AE' : 'United Arab Emirates'

}
top_k = 5
flog_to_scan = {val:key for key, val in scan_to_flag.items()}
y = amp_factor.max(axis=(1,2))
fig, ax = plt.subplots(figsize=(6,4))
ax.set_xscale('log')
ax.set_yscale('log')
ax.tick_params(left=True, bottom=True, direction='in')
ax.tick_params(axis='x', which='minor', direction='in')
ax.tick_params(axis='y', which='minor', direction='in')
ax.set_axisbelow(True)
ax.grid(linestyle='--')
for i in range(top_k):
    country = unique_countries[desc_order][i]
    country_ind = [ip_to_index[key] for key, val in ip_to_country.items() if val==country]
    y_each = y[country_ind]
    x = np.array(range(y_each.shape[0]))+1
    ax.plot(x, y_each[np.argsort(y_each)[::-1]], label=country_names[country])
ax.set_xlabel('IP Address Rank', weight='bold', fontsize=12)
ax.set_ylabel('Amplification Factor', weight='bold', fontsize=12)
plt.legend(fontsize=10)
plt.savefig('figure8.png', bbox_inches='tight')
plt.close('all')
print('Saved figure8.png')
print('*****')

# table 4: countries
# censor_nations = ['CN', 'KR', 'IR', 'EG', 'BD', 'SA', 'OM', 'QA', 'UZ', 'KW', 'AE']
# censor_nation_counts = [counts[unique_countries.tolist().index(it)] if it in unique_countries else 0 for it in censor_nations]


# table 2: Total data received (GB) from the top 100,000 IP addresses for each combination of target URL and packet sequence
print('\n*****')
print('table 2')
total_receive_data_size = receive_data_size.sum(axis=0)/1000000
table = np.concatenate((np.asarray(urls).reshape(-1,1), total_receive_data_size), axis=1)
table = np.concatenate((np.asarray(['None']+[scan_to_flag[it] for it in scans]).reshape(1,-1),table), axis=0)
print(table)
print('*****')

# table 3: Number of IP addresses with ampliﬁcation factor over 10× for each combination of target URL and packet sequence.
print('\n*****')
print('table 3')
threshold = 10
table = (amp_factor>threshold).sum(axis=0)
table = np.concatenate((np.asarray(urls).reshape(-1,1), table), axis=1)
table = np.concatenate((np.asarray(['None']+[scan_to_flag[it] for it in scans]).reshape(1,-1),table), axis=0)
print(table)
print('*****')
