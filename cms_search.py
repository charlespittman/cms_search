import pyodbc
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clock', nargs=1)
args = parser.parse_args()

with open('config.json') as config:
    config = json.load(config)

cnxn = pyodbc.connect(driver=config['driver'],
                      server=config['server'],
                      uid=config['user'],
                      pwd=config['password'],
                      database=config['database'],
                      autocommit=True)
cursor = cnxn.cursor()

class CMS:
    def __init__(self, row):
        self.clockid = '{}.{}.{}'.format(row.Eid, row.Fid, row.Cid)
        self.maintserv = row.MaintServ
        self.maintport = row.MaintPort
        self.enterprisename = row.EnterpriseName
        self.facility = row.FacilityName
        self.clockname = row.ClockName
        self.lastonline = row.LastTime
        self.model = row.ActiveModel
        self.os = row.ActiveOS
        self.firmware = row.ActiveFirmware
        self.fp = row.FPOS
        self.setcodes = row.SetCodes
        self.edb = row.EDBQty
        self.fpdb = row.FPDBQty
        self.edb2 = row.EDB2Qty
        self.bdb = row.BDBQty
        self.macaddress = row.ActiveMacAddress
        self.clocktime = row.ActiveClockTime
        self.serialnumber = row.SerialNumber
        self.pendingupdate = row.PendingUpdateInd
        self.lastupdate = row.LastUpdateDate
        self.updatesuccess = row.UpdateSuccessInd
        self.updateresults = row.UpdateResults
        self.restrictedupdate = row.RestrictedUpdateInd
        self.activemaintserv = row.ActiveMaintServ
        self.agent = row.ActiveHost
        self.agentstatus = row.HostStatus
        self.laninfo = row.LANInfo
        self.vlctail = row.VLCTail
        self.vlcid = row.VLCID

    def __str__(self):
        out = [
            'enterprise={}'.format(self.enterprisename),
            'facility={}'.format(self.facility),
            'clockname={}'.format(self.clockname),
            'clockid={}'.format(self.clockid),
            'maintport={}'.format(self.maintport),
            'lastonline={}'.format(self.lastonline),
            'model={}'.format(self.model),
            'fp={}'.format(self.fp),
            'bdb={}'.format(self.bdb),
            'edb={}'.format(self.edb),
            'edb2={}'.format(self.edb2),
            'fpdb={}'.format(self.fpdb),
            'activemaintserv={}'.format(self.activemaintserv),
            'agent={}'.format(self.agent),
            'agentstatus={}'.format(self.agentstatus),
            'clocktime={}'.format(self.clocktime),
            'firmware={}'.format(self.firmware),
            'laninfo={}'.format(self.laninfo),
            'lastupdate={}'.format(self.lastupdate),
            'macaddress={}'.format(self.macaddress),
            'maintserv={}'.format(self.maintserv),
            'os={}'.format(self.os),
            'pendingupdate={}'.format(self.pendingupdate),
            'restrictedupdate={}'.format(self.restrictedupdate),
            'serialnumber={}'.format(self.serialnumber),
            'setcodes={}'.format(self.setcodes),
            'updateresults={}'.format(self.updateresults),
            'updatesuccess={}'.format(self.updatesuccess),
            'vlcid={}'.format(self.vlcid),
            'vlctail={}'.format(self.vlctail)]
        return ','.join(out)

    def print_short(self):
        out = [
            'enterprise={}'.format(self.enterprisename),
            'facility={}'.format(self.facility),
            'clockname={}'.format(self.clockname),
            'clockid={}'.format(self.clockid),
            'maintport={}'.format(self.maintport),
            'lastonline={}'.format(self.lastonline),
            'model={}'.format(self.model),
            'fp={}'.format(self.fp),
            ]
        print(','.join(out))

def convert_clock_id(cid):
    return cid[:-2], cid[-2:]

if __name__ == '__main__':
    hosp_id, clock_id = convert_clock_id(args.clock[0])
    sql = 'SELECT * FROM dbo.VLConnect WHERE fid={} AND cid={}'.format(hosp_id, clock_id)
    res = cursor.execute(sql)
    for r in res:
        cms = CMS(r)
        cms.print_short()
