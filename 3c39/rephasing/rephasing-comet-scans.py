# part III: Rephase to desired target by changing the phase center
with open('comet67P_scans.txt', 'r') as fin:
    scans = fin.readlines()
SCANS = [tuple(scan.strip().split(',')) for scan in scans]
TARGET= "67P"

for scan, utc, phasecenter in SCANS:
    print(f'Generate this input from MS: {scan}, {utc}, {phasecenter}')
    source = '1627186165_sdp_l0-3c39-{}.ms'.format(scan)
    print(f'Input MS from split: {source}')
    target = '1627186165_sdp_l0-{}-{}.ms'.format(TARGET, scan)
    print(f'Output MS for rephasing: {target}')
    os.system("rm -fr {}*".format(target))

#     print("updating CORRECTED_DATA")
#     os.system("taql update {} set CORRECTED_DATA=CORRECTED_DD_DATA-MODEL_DATA".format(source))
    print("splitting")
    split(vis=source, outputvis=target, datacolumn='corrected')
    _, ra, dec = phasecenter.split()
    os.system("chgcentre {} {} {}".format(target, ra, dec))

# -fin-
