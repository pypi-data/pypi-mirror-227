from typing import (
    Dict,
    Any,
)

# NOTE: _server is not inherited down stream, currently

# ======================================
# Interesting for future enhancements:
# https://github.com/rfc1036/whois/blob/next/tld_serv_list
# https://github.com/rfc1036/whois/blob/next/new_gtlds_list
# seems the most up to date and maintained

# =================================================================
# Often we want to repeat regex patterns,
#   ( typically with nameservers or status fields )
#   that becomes unreadable very fast.
# Allow for a simplification that expands on usage and
#   allow forcing the first to be mandatory as default,
#   but overridable when needed


def xStr(what: str, times: int = 1, firstMandatory: bool = True) -> str:
    if times < 1:
        return ""

    if firstMandatory and what[-1] == "?":
        return what[:-1] + (what * (times - 1))
    else:
        return what * times


# =================================================================
# The database
# When we finally apply the regexes we use IGNORE CASE allways on all matches

ZZ: Dict[str, Any] = {}

# ======================================
# meta registrars start with _ are only used a s a common toll to define others
# NOTE: _server is not inherited down stream, currently

ZZ["_privateReg"] = {"_privateRegistry": True}

ZZ["_teleinfo"] = {"extend": "com", "_server": "whois.teleinfo.cn"}  # updated all downstream

ZZ["_uniregistry"] = {"extend": "com", "_server": "whois.uniregistry.net"}  # updated all downstream

ZZ["_donuts"] = {
    "extend": "com",
    "_server": "whois.donuts.co",
    "registrant": r"Registrant Organization:\s?(.+)",
    "status": r"Domain Status:\s?(.+)",
}  # updated all downstream

ZZ["_centralnic"] = {
    "extend": "com",
    "_server": "whois.centralnic.com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Domain Status:\s?(.+)",
}  # updated all downstream

ZZ["_gtldKnet"] = {"extend": "com", "_server": "whois.gtld.knet.cn", "admin": r"Admin\s*Name:\s+(.+)"}  # updated all downstream

# ======================================
# start of regular entries, simple domains are at the end

ZZ["com"] = {
    "domain_name": r"Domain Name\s*:\s*(.+)",
    "registrar": r"Registrar:\s?(.+)",
    "registrant": r"Registrant\s*Organi(?:s|z)ation:([^\n]*)",
    "registrant_country": r"Registrant Country:\s?(.+)",
    "creation_date": r"Creation Date:[ \t]*([^\n]*)",
    "expiration_date": r"(?:Expiry|Expiration) Date:[ \t]*([^\n]*)",
    "updated_date": r"Updated Date:[\t ]*([^\n]*)",
    "name_servers": r"Name Server:\s*(.+)\s*",
    "status": r"Status:\s?(.+)",
    "emails": r"([\w\.-]+@[\w\.-]+\.[\w]{2,4})",
}

# United Kingdom - academic sub-domain
ZZ["ac.uk"] = {
    "extend": "uk",
    "domain_name": r"Domain:\n\s?(.+)",
    "owner": r"Domain Owner:\n\s?(.+)",
    "registrar": r"Registered By:\n\s?(.+)",
    "registrant": r"Registered Contact:\n\s*(.+)",
    "expiration_date": r"Renewal date:\n\s*(.+)",
    "updated_date": r"Entry updated:\n\s*(.+)",
    "creation_date": r"Entry created:\n\s?(.+)",
    "name_servers": r"Servers:\s*(.+)\t\n\s*(.+)\t\n",
    "_test": "imperial.ac.uk",
}

ZZ["co.uk"] = {
    "extend": "uk",
    "domain_name": r"Domain name:\s+(.+)",
    "registrar": r"Registrar:\s+(.+)",
    "status": r"Registration status:\s*(.+)",
    "creation_date": r"Registered on:(.+)",
    "expiration_date": r"Expiry date:(.+)",
    "updated_date": r"Last updated:(.+)",
    "owner": r"Domain Owner:\s+(.+)",
    "registrant": r"Registrant:\n\s+(.+)",
    "_test": "livedns.co.uk",
}

# Armenia
ZZ["am"] = {
    "domain_name": r"Domain name:\s+(.+)",
    "status": r"Status:\s(.+)",
    "registrar": r"Registrar:\s+(.+)",
    "registrant": r"Registrant:\s+(.+)",
    "registrant_country": r"Registrant:\n.+\n.+\n.+\n\s+(.+)",
    "creation_date": r"Registered:\s+(.+)",
    "expiration_date": r"Expires:\s+(.+)",
    "updated_date": r"Last modified:\s+(.+)",
    "name_servers": r"DNS servers.*:\n%s" % xStr(r"(?:\s+(\S+)\n)?", 4),
}

# Amsterdam
ZZ["amsterdam"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Domain Status:\s?(.+)",
    "server": "whois.nic.amsterdam",
    "_test": "nic.amsterdam",
}

# Argentina
ZZ["ar"] = {
    "extend": "com",
    "domain_name": r"domain\s*:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "creation_date": r"registered:\s?(.+)",
    "expiration_date": r"expire:\s?(.+)",
    "updated_date": r"changed\s*:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)\s*",
    "_server": "whois.nic.ar",
    "_test": "nic.ar",
}

# Austria
ZZ["at"] = {
    "extend": "com",
    "_server": "whois.nic.at",
    "domain_name": r"domain:\s?(.+)",
    "updated_date": r"changed:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant": r"registrant:\s?(.+)",
}

ZZ["ax"] = {
    "extend": "com",
    "domain_name": r"domain\.+:\s*(\S+)",
    "registrar": r"registrar\.+:\s*(.+)",
    "creation_date": r"created\.+:\s*(\S+)",
    "expiration_date": r"expires\.+:\s*(\S+)",
    "updated_date": r"modified\.+:\s?(\S+)",
    "name_servers": r"nserver\.+:\s*(\S+)",
    "status": r"status\.+:\s*(\S+)",
    "registrant": r"Holder\s+name\.+:\s*(.+)\r?\n",  # not always present see meta.ax and google.ax
    "registrant_country": r"country\.+:\s*(.+)\r?\n",  # not always present see meta.ax and google.ax
}

ZZ["bank"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
}

ZZ["be"] = {
    "extend": "pl",
    "domain_name": r"\nDomain:\s*(.+)",
    "registrar": r"Company Name:\n?(.+)",
    "creation_date": r"Registered:\s*(.+)\n",
    "status": r"Status:\s?(.+)",
    "name_servers": r"Nameservers:(?:\n[ \t]+(\S+))?(?:\n[ \t]+(\S+))?(?:\n[ \t]+(\S+))?(?:\n[ \t]+(\S+))?\n\n",
}

ZZ["biz"] = {
    "extend": "com",
    "registrar": r"Registrar:\s?(.+)",
    "registrant": r"Registrant Organization:\s?(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": None,
}

ZZ["br"] = {
    "extend": "com",
    "_server": "whois.registro.br",
    "domain_name": r"domain:\s?(.+)",
    "registrar": "nic.br",
    "registrant": None,
    "owner": r"owner:\s?(.+)",
    "creation_date": r"created:\s?(.+)",
    "expiration_date": r"expires:\s?(.+)",
    "updated_date": r"changed:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)",
    "status": r"status:\s?(.+)",
}

ZZ["by"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s*(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "registrant": r"Org:\s*(.+)",
    "registrant_country": r"Country:\s*(.+)",
    "creation_date": r"Creation Date:\s*(.+)",
    "expiration_date": r"Expiration Date:\s*(.+)",
    "updated_date": r"Updated Date:\s*(.+)",
    "name_servers": r"Name Server:\s+(\S+)\n",
}

# Brittany (French Territory)
ZZ["bzh"] = {
    "extend": "fr",
    "domain_name": r"Domain Name:\s*(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "registrant": r"Registrant Organization:\s*(.+)",
    "registrant_country": r"Registrant Country:\s*(.*)",
    "creation_date": r"Creation Date:\s*(.*)",
    "expiration_date": r"Registry Expiry Date:\s*(.*)",
    "updated_date": r"Updated Date:\s*(.*)",
    "name_servers": r"Name Server:\s*(.*)",
    "status": r"Domain Status:\s*(.*)",
}

ZZ["cc"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
}

ZZ["cl"] = {
    "extend": "com",
    "registrar": "nic.cl",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Expiration Date:\s?(.+)",
    "name_servers": r"Name Server:\s*(.+)\s*",
}

ZZ["cn"] = {
    "extend": "com",
    "registrar": r"Sponsoring Registrar:\s?(.+)",
    "registrant": r"Registrant:\s?(.+)",
    "creation_date": r"Registration Time:\s?(.+)",
    "expiration_date": r"Expiration Time:\s?(.+)",
}

ZZ["com.tr"] = {
    "extend": "com",
    "domain_name": r"\*\* Domain Name:\s?(.+)",
    "registrar": r"Organization Name\s+:\s?(.+)",
    "registrant": r"\*\* Registrant:\s+?(.+)",
    "registrant_country": None,
    "creation_date": r"Created on\.+:\s?(.+).",
    "expiration_date": r"Expires on\.+:\s?(.+).",  # note the trailing . on both dates fields
    "updated_date": "",
    "name_servers": r"\*\* Domain Servers:\n(?:(\S+).*\n)?(?:(\S+).*\n)?(?:(\S+).*\n)?(?:(\S+).*\n)?",  # allow for ip addresses after the name server
    "status": None,
    "_server": "whois.trabis.gov.tr",
    "_test": "google.com.tr",
}

ZZ["co.il"] = {
    "extend": "com",
    "domain_name": r"domain:\s*(.+)",
    "registrar": r"registrar name:\s*(.+)",
    "registrant": None,
    "registrant_country": None,
    "creation_date": None,
    "expiration_date": r"validity:\s*(.+)",
    "updated_date": None,
    "name_servers": r"nserver:\s*(.+)",
    "status": r"status:\s*(.+)",
}

ZZ["cz"] = {
    "extend": "com",
    "domain_name": r"domain:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant": r"registrant:\s?(.+)",
    "registrant_country": None,
    "creation_date": r"registered:\s?(.+)",
    "expiration_date": r"expire:\s?(.+)",
    "updated_date": r"changed:\s?(.+)",
    "name_servers": r"nserver:\s+(\S+)",
    "status": r"status:\s*(.+)",
}

ZZ["de"] = {
    "extend": "com",
    "domain_name": r"\ndomain:\s*(.+)",
    "updated_date": r"\nChanged:\s?(.+)",
    "name_servers": r"Nserver:\s*(.+)",
}

# Denmark
ZZ["dk"] = {
    "domain_name": r"Domain:\s?(.+)",
    "registrar": None,
    "registrant": r"Registrant\s*Handle:\s*\w*\s*Name:\s?(.+)",
    "registrant_country": r"Country:\s?(.+)",
    "creation_date": r"Registered:\s?(.+)",
    "expiration_date": r"Expires:\s?(.+)",
    "updated_date": None,
    "name_servers": r"Hostname:\s*(.+)\s*",
    "status": r"Status:\s?(.+)",
    "emails": None,
}

ZZ["edu"] = {
    "extend": "com",
    "registrant": r"Registrant:\s*(.+)",
    "creation_date": r"Domain record activated:\s?(.+)",
    "updated_date": r"Domain record last updated:\s?(.+)",
    "expiration_date": r"Domain expires:\s?(.+)",
    "name_servers": r"Name Servers:\s?%s" % xStr(r"(?:\t(.+)\n)?", 10),
    "_test": "rutgers.edu",
}

# estonian
ZZ["ee"] = {
    "extend": "com",
    "domain_name": r"Domain:\nname:\s+(.+\.ee)\n",
    "registrar": r"Registrar:\nname:\s+(.+)\n",
    "registrant": r"Registrant:\nname:\s+(.+)\n",
    "registrant_country": r"Registrant:(?:\n+.+\n*)*country:\s+(.+)\n",
    "creation_date": r"Domain:(?:\n+.+\n*)*registered:\s+(.+)\n",
    "expiration_date": r"Domain:(?:\n+.+\n*)*expire:\s+(.+)\n",
    "updated_date": r"Domain:(?:\n+.+\n*)*changed:\s+(.+)\n",
    "name_servers": r"nserver:\s*(.+)",
    "status": r"Domain:(?:\n+.+\n*)*status:\s+(.+)\n",
}

ZZ["eu"] = {
    "extend": "com",
    "_server": "whois.eu",
    "registrar": r"Name:\s?(.+)",
    "domain_name": r"\nDomain:\s*(.+)",
    "name_servers": r"Name servers:\n(?:\s+(\S+)\n)(?:\s+(\S+)\n)?(?:\s+(\S+)\n)?(?:\s+(\S+)\n)?(?:\s+(\S+)\n)?(?:\s+(\S+)\n)\n?",
}

ZZ["fi"] = {
    "domain_name": r"domain\.+:\s?(.+)",
    "registrar": r"registrar\.+:\s?(.+)",
    "registrant_country": None,
    "creation_date": r"created\.+:\s?(.+)",
    "expiration_date": r"expires\.+:\s?(.+)",
    "updated_date": r"modified\.+:\s?(.+)",
    "name_servers": r"nserver\.+:\s*(.+)",
    "status": r"status\.+:\s?(.+)",
}

ZZ["fr"] = {
    "extend": "com",
    "domain_name": r"domain:\s?(.+)",
    "registrar": r"registrar:\s*(.+)",
    "registrant": r"contact:\s?(.+)",
    "registrant_organization": r"type:\s+ORGANIZATION\scontact:\s+(.*)",
    "creation_date": r"created:\s?(.+)",
    "expiration_date": r"Expiry Date:\s?(.+)",
    "updated_date": r"last-update:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)",
    "status": r"status:\s?(.+)",
    "_test": "sfr.fr",
    "registrant_country": r"Country:\s?(.+)",
}

# Hong Kong
ZZ["hk"] = {
    "extend": "com",
    "_server": "whois.hkirc.hk",
    "domain_name": r"Domain Name:\s+(.+)",
    "registrar": r"Registrar Name:\s?(.+)",
    "registrant": r"Company English Name.*:\s?(.+)",
    "registrant_country": None,
    "creation_date": r"Domain Name Commencement Date:\s?(.+)",
    "expiration_date": r"Expiry Date:\s?(.+)",
    "updated_date": None,
    #  name servers have trailing whitespace, lines are \n only
    "name_servers": r"Name Servers Information:\s*(?:(\S+)[ \t]*\n)(?:(\S+)[ \t]*\n)?(?:(\S+)[ \t]*\n)?(?:(\S+)[ \t]*\n)?",
    "status": None,
}

ZZ["id"] = {
    "extend": "com",
    "registrar": r"Sponsoring Registrar Organization:\s?(.+)",
    "creation_date": r"Created On:\s?(.+)",
    "expiration_date": r"Expiration Date:\s?(.+)",
    "updated_date": r"Last Updated On:\s?(.+)$",
}

ZZ["im"] = {
    "domain_name": r"Domain Name:\s+(.+)",
    "status": None,
    "registrar": None,
    "registrant_country": None,
    "creation_date": "",
    "expiration_date": r"Expiry Date:\s?(.+)",
    "updated_date": "",
    "name_servers": r"Name Server:(.+)",
}

ZZ["ir"] = {
    "domain_name": r"domain:\s?(.+)",
    "registrar": "nic.ir",
    "registrant_country": None,
    "creation_date": None,
    "status": None,
    "expiration_date": r"expire-date:\s?(.+)",
    "updated_date": r"last-updated:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)\s*",
}

ZZ["is"] = {
    "extend": "com",
    "domain_name": r"domain:\s?(.+)",
    "registrar": None,
    "registrant": r"registrant:\s?(.+)",
    "registrant_country": None,
    "creation_date": r"created:\s?(.+)",
    "expiration_date": r"expires:\s?(.+)",
    "updated_date": None,
    "name_servers": r"nserver:\s?(.+)",
    "status": None,
}

ZZ["it"] = {
    "extend": "com",
    "domain_name": r"Domain:\s?(.+)",
    "registrar": r"Registrar\s*Organization:\s*(.+)",
    "registrant": r"Registrant\s*Organization:\s*(.+)",
    "creation_date": r"Created:\s?(.+)",
    "expiration_date": r"Expire Date:\s?(.+)",
    "updated_date": r"Last Update:\s?(.+)",
    "name_servers": r"Nameservers(?:\n\s+(\S+))?(?:\n\s+(\S+))?(?:\n\s+(\S+))?(?:\n\s+(\S+))?",
    "status": r"Status:\s?(.+)",
}

# The Japanese whois servers always return English unless a Japanese locale is specified in the user's LANG environmental variable.
# See: https://www.computerhope.com/unix/uwhois.htm
# Additionally, whois qeuries can explicitly request english:
#   To suppress Japanese output, add'/e' at the end of command, e.g. 'whois -h whois.jprs.jp xxx/e'.
#
ZZ["jp"] = {
    "domain_name": r"\[Domain Name\]\s?(.+)",
    "registrar": r"\[ (.+) database provides information on network administration. Its use is    \]",
    "registrant": r"\[Registrant\]\s?(.+)",
    "registrant_country": None,
    "creation_date": r"\[Created on\]\s?(.+)",
    "expiration_date": r"\[Expires on\]\s?(.+)",
    "updated_date": r"\[Last Updated\]\s?(.+)",
    "name_servers": r"\[Name Server\]\s*(.+)",
    "status": r"\[Status\]\s?(.+)",
    "emails": r"([\w\.-]+@[\w\.-]+\.[\w]{2,4})",
}

# The Japanese whois servers always return English unless a Japanese locale is specified in the user's LANG environmental variable.
# See: https://www.computerhope.com/unix/uwhois.htm
# Additionally, whois qeuries can explicitly request english:
# 	To suppress Japanese output, add'/e' at the end of command, e.g. 'whois -h whois.jprs.jp xxx/e'.
#
ZZ["co.jp"] = {
    "extend": "jp",
    "creation_date": r"\[Registered Date\]\s?(.+)",
    "expiration_date": None,
    "updated_date": r"\[Last Update\]\s?(.+)",
    "status": r"\[State\]\s?(.+)",
}

ZZ["kg"] = {
    "domain_name": r"Domain\s+(\S+)",
    "registrar": r"Billing\sContact:\n.*\n\s+Name:\s(.+)\n",
    "registrant_country": None,
    "expiration_date": r"Record expires on:\s+(.+)",
    "creation_date": r"Record created:\s+(.+)",
    "updated_date": r"Record last updated on:\s+(.+)",
    "name_servers": r"Name servers in the listed order:\n\n(?:(\S+)[ \t]*\S*\n)(?:(\S+)[ \t]*\S*\n)?(?:(\S+)[ \t]*\S*\n)?\n",
    "status": r"Domain\s+\S+\s+\((\S+)\)",
}

ZZ["kr"] = {
    "extend": "com",
    "_server": "whois.kr",
    "domain_name": r"Domain Name\s*:\s?(.+)",
    "registrar": r"Authorized Agency\s*:\s*(.+)",
    "registrant": r"Registrant\s*:\s*(.+)",
    "creation_date": r"Registered Date\s*:\s?(.+)",
    "expiration_date": r"Expiration Date\s*:\s?(.+)",
    "updated_date": r"Last Updated Date\s*:\s?(.+)",
    "status": r"status\s*:\s?(.+)",
    "name_servers": r"Host Name\s+:\s+(\S+)\n",
}

ZZ["kz"] = {
    "domain_name": r"Domain name\.+:\s(.+)",
    "registrar": r"Current Registar:\s(.+)",
    "registrant_country": r"Country\.+:\s?(.+)",
    "expiration_date": None,
    "creation_date": r"Domain created:\s(.+)",
    "updated_date": r"Last modified :\s(.+)",
    "name_servers": r"ary server\.+:\s+(\S+)",
    "status": r"Domain status :(?:\s+([^\n]+)\n)",
}

ZZ["lt"] = {
    "extend": "com",
    "domain_name": r"Domain:\s?(.+)",
    "creation_date": r"Registered:\s?(.+)",
    "expiration_date": r"Expires:\s?(.+)",
    "name_servers": r"Nameserver:\s*(.+)\s*",
    "status": r"\nStatus:\s?(.+)",
}

ZZ["lv"] = {
    "extend": "com",
    "domain_name": r"domain:\s*(.+)",
    "creation_date": r"Registered:\s*(.+)\n",  # actually there seem to be no dates
    "updated_date": r"Changed:\s*(.+)\n",
    "expiration_date": r"paid-till:\s*(.+)",
    "name_servers": r"nserver:\s*(.+)",
    "status": r"Status:\s?(.+)",
    "_server": "whois.nic.lv",
}

ZZ["me"] = {
    "extend": "biz",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Expiry Date:\s?(.+)",
    "updated_date": None,  # some entries have no date string but not always
    "name_servers": r"Name Server:\s*(\S+)\r?\n",
    "status": r"Domain Status:\s?(.+)",
}

ZZ["ml"] = {
    "extend": "com",
    "domain_name": r"Domain name:\s*([^(i|\n)]+)",
    "registrar": r"(?<=Owner contact:\s)[\s\S]*?Organization:(.*)",
    "registrant_country": r"(?<=Owner contact:\s)[\s\S]*?Country:(.*)",
    "registrant": r"(?<=Owner contact:\s)[\s\S]*?Name:(.*)",
    "creation_date": r"Domain registered: *(.+)",
    "expiration_date": r"Record will expire on: *(.+)",
    "name_servers": r"Domain Nameservers:\s*(.+)\n\s*(.+)\n",
}

ZZ["mx"] = {
    "domain_name": r"Domain Name:\s?(.+)",
    "creation_date": r"Created On:\s?(.+)",
    "expiration_date": r"Expiration Date:\s?(.+)",
    "updated_date": r"Last Updated On:\s?(.+)",
    "registrar": r"Registrar:\s?(.+)",
    "name_servers": r"\sDNS:\s*(.+)",
    "registrant_country": None,
    "status": None,
}

# New-Caledonia (French Territory)
ZZ["nc"] = {
    "extend": "fr",
    "domain_name": r"Domain\s*:\s(.+)",
    "registrar": r"Registrar\s*:\s(.+)",
    "registrant": r"Registrant name\s*:\s(.+)",
    "registrant_country": None,
    "creation_date": r"Created on\s*:\s(.*)",
    "expiration_date": r"Expires on\s*:\s(.*)",
    "updated_date": r"Last updated on\s*:\s(.*)",
    "name_servers": r"Domain server [0-9]{1,}\s*:\s(.*)",
    "status": None,
}

ZZ["nl"] = {
    "extend": "com",
    "expiration_date": None,
    "registrant_country": None,
    "domain_name": r"Domain name:\s?(.+)",
    "name_servers": r"Domain nameservers.*:\n%s" % xStr(r"(?:\s+(\S+)\n)?", 10),
    "reseller": r"Reseller:\s?(.+)",
    "abuse_contact": r"Abuse Contact:\s?(.+)",
    "_test": "google.nl",
    "_slowdown": 5,
}

# Norway
ZZ["no"] = {
    "domain_name": r"Domain Name\.+:\s?(.+)",
    "registrar": r"Registrar Handle\.+:\s?(.+)",
    "registrant": None,
    "registrant_country": None,
    "creation_date": r"Created:\s?(.+)",
    "expiration_date": None,
    "updated_date": r"Last Updated:\s?(.+)",
    "name_servers": r"Name Server Handle\.+:\s*(.+)\s*",
    "status": None,
    "emails": None,
}

ZZ["nyc"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
}

ZZ["nz"] = {
    "domain_name": r"domain_name:\s?(.+)",
    "registrar": r"registrar_name:\s?(.+)",
    "registrant": r"registrant_contact_name:\s?(.+)",
    "registrant_country": None,
    "creation_date": r"domain_dateregistered:\s?(.+)",
    "expiration_date": r"domain_datebilleduntil:\s?(.+)",
    "updated_date": r"domain_datelastmodified:\s?(.+)",
    "name_servers": r"ns_name_[0-9]{2}:\s?(.+)",
    "status": r"query_status:\s?(.+)",
    "emails": r"([\w\.-]+@[\w\.-]+\.[\w]{2,4})",
}

ZZ["org"] = {
    "extend": "com",
    "expiration_date": r"\nRegistry Expiry Date:\s?(.+)",
    "updated_date": r"\nLast Updated On:\s?(.+)",
    "name_servers": r"Name Server:\s?(.+)\s*",
}

ZZ["pharmacy"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"status:\s?(.+)",
}

ZZ["pl"] = {
    "extend": "uk",
    "registrar": r"\nREGISTRAR:\s*(.+)\n",
    "creation_date": r"\ncreated:\s*(.+)\n",
    "updated_date": r"\nlast modified:\s*(.+)\n",
    "expiration_date": r"\noption expiration date:\s*(.+)\n",
    "name_servers": r"nameservers:%s" % xStr(r"(?:\s+(\S+)[^\n]*\n)?", 4),
    "status": r"\nStatus:\n\s*(.+)",
}

ZZ["pt"] = {
    "_server": "whois.dns.pt",
    "extend": "com",
    "domain_name": r"Domain:\s?(.+)",
    "registrar": None,
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Expiration Date:\s?(.+)",
    "updated_date": None,
    "name_servers": r"Name Server:%s" % xStr(r"(?:\s*(\S+)[^\n]*\n)?", 2),
    "status": r"Domain Status:\s?(.+)",
}

ZZ["pw"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
}

ZZ["ru"] = {
    "extend": "com",
    "domain_name": r"domain:\s*(.+)",
    "creation_date": r"created:\s*(.+)",
    "expiration_date": r"paid-till:\s*(.+)",
    "name_servers": r"nserver:\s*(.+)",
    "status": r"state:\s*(.+)",
    "_server": "whois.tcinet.ru",
}

ZZ["sa"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s*(.+\.sa)\s",
    "registrant": r"Registrant:\n*(.+)\n",
    "name_servers": r"Name Servers:\s*(.+)\s*(.+)?",
    "registrant_country": None,
    "registrar": None,
    "creation_date": None,
    "expiration_date": None,
    "updated_date": None,
    "status": None,
    "emails": None,
}

ZZ["sh"] = {
    "extend": "com",
    "registrant": r"\nRegistrant Organization:\s?(.+)",
    "expiration_date": r"\nRegistry Expiry Date:\s*(.+)",
    "status": r"\nDomain Status:\s?(.+)",
}

ZZ["se"] = {
    "domain_name": r"domain:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant_country": None,
    "creation_date": r"created:\s+(\d{4}-\d{2}-\d{2})",
    "expiration_date": r"expires:\s+(\d{4}-\d{2}-\d{2})",
    "updated_date": r"modified:\s+(\d{4}-\d{2}-\d{2})",
    "name_servers": r"nserver:\s*(.+)",
    "status": r"status:\s?(.+)",
}

# Singapore - Commercial sub-domain
ZZ["com.sg"] = {
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s?(.+)",
    "registrant": r"Registrant:\r?\n\r?\n\s*Name:\s*(.+)\r?\n",
    "registrant_country": None,
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Expiration Date:\s?(.+)",
    "updated_date": r"Modified Date:\s?(.+)",
    "name_servers": r"Name Servers:(?:\s+(\S+))(?:\s+(\S+))?(?:\s+(\S+))?(?:\s+([\.\w]+)\s+)?",
    "status": r"Domain Status:\s*(.*)\r?\n",
    "emails": r"[\w\.-]+@[\w\.-]+\.[\w]{2,4}",
}

# Slovakia
ZZ["sk"] = {
    "extend": "com",
    "domain_name": r"Domain:\s?(.+)",
    "creation_date": r"Created:\s?(.+)",
    "expiration_date": r"Valid Until:\s?(.+)",
    "updated_date": r"Updated:\s?(.+)",
    "name_servers": r"Nameserver:\s*(\S+)",
    "registrant": r"Contact:\s?(.+)",
    "registrant_country": r"Country Code:\s?(.+)\nRegistrar:",
}

ZZ["tel"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"\nRegistry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
}

# Thailand - Commercial sub-domain
ZZ["co.th"] = {
    "_server": "whois.thnic.co.th",
    "extend": "com",
    "registrant": r"Domain Holder Organization:\s?(.+)",
    "registrant_country": r"Domain Holder Country:\s?(.+)",
    "creation_date": r"Created date:\s?(.+)",
    "expiration_date": r"Exp date:\s?(.+)",
    "updated_date": r"Updated date:\s?(.+)",
}

ZZ["tn"] = {
    "extend": "com",
    "domain_name": r"Domain name\.+:(.+)\s*",
    "registrar": r"Registrar\.+:(.+)\s*",
    "registrant": r"Owner Contact\n+Name\.+:\s?(.+)",
    "registrant_country": r"Owner Contact\n(?:.+\n)+Country\.+:\s(.+)",
    "creation_date": r"Creation date\.+:\s?(.+)",
    "expiration_date": None,
    "updated_date": None,
    "name_servers": r"DNS servers\n%s" % xStr(r"(?:Name\.+:\s*(\S+)\n)?", 4),
    "status": r"Domain status\.+:(.+)",
}

ZZ["tv"] = {
    "extend": "com",
    "_server": "whois.nic.tv",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
}

ZZ["tz"] = {
    "domain_name": r"\ndomain:\s*(.+)",
    "registrar": r"\nregistrar:\s?(.+)",
    "registrant": r"\nregistrant:\s*(.+)",
    "registrant_country": None,
    "creation_date": r"\ncreated:\s*(.+)",
    "expiration_date": r"expire:\s?(.+)",
    "updated_date": r"\nchanged:\s*(.+)",
    "status": None,
    "name_servers": r"\nnserver:\s*(.+)",
}

ZZ["ua"] = {
    "extend": "com",
    "domain_name": r"\ndomain:\s*(.+)",
    "registrar": r"\nregistrar:\s*(.+)",
    "registrant_country": r"\ncountry:\s*(.+)",
    "creation_date": r"\ncreated:\s+(.+)",
    "expiration_date": r"\nexpires:\s*(.+)",
    "updated_date": r"\nmodified:\s*(.+)",
    "name_servers": r"\nnserver:\s*(.+)",
    "status": r"\nstatus:\s*(.+)",
}

ZZ["uk"] = {
    "extend": "com",
    "registrant": r"Registrant:\n\s*(.+)",
    "creation_date": r"Registered on:\s*(.+)",
    "expiration_date": r"Expiry date:\s*(.+)",
    "updated_date": r"Last updated:\s*(.+)",
    "name_servers": r"Name servers:%s\n\n" % xStr(r"(?:\n[ \t]+(\S+).*)?", 10),  # capture up to 10
    "status": r"Registration status:\n\s*(.+)",
}

ZZ["uz"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Expiration Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
    "name_servers": r"Domain servers in listed order:%s\n\n" % xStr(r"(?:\n\s+(\S+))?", 4),
    # sometimes 'not.defined is returned as a nameserver (e.g. google.uz)
}

ZZ["wiki"] = {
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
}

ZZ["work"] = {
    "extend": "com",
    "_server": "whois.nic.work",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
}

ZZ["ac"] = {
    "domain_name": r"Domain Name:\s+(.+)",
    "registrar": r"Registrar:\s+(.+)",
    "status": r"Domain Status:\s(.+)",
    "name_servers": r"Name Server:\s+(\S+)",
    "registrant_country": r"Registrant Country:\s*(.*)\r?\n",
    "updated_date": r"Updated Date:\s+(.+)",
    "creation_date": r"Creation Date:\s+(.+)",
    "expiration_date": r"Registry Expiry Date:\s+(.+)",
}

ZZ["ae"] = {
    "extend": "ar",
    "domain_name": r"Domain Name:\s+(.+)",
    "registrar": r"Registrar Name:\s+(.+)",
    "status": r"Status:\s(.+)",
    "name_servers": r"Name Server:\s+(\S+)",
    "registrant_country": None,
    "creation_date": None,
    "expiration_date": None,
    "updated_date": None,
    "_test": "google.ae",
}

ZZ["bg"] = {
    "_server": "whois.register.bg",
    "domain_name": r"DOMAIN\s+NAME:\s+(.+)",
    "status": r"registration\s+status:\s(.+)",
    "name_servers": r"NAME SERVER INFORMATION:\n%s" % xStr(r"(?:(.+)\n)?", 4),
    "creation_date": None,
    "expiration_date": None,
    "updated_date": None,
    "registrar": None,
    "registrant_country": None,
}

ZZ["bj"] = {
    "_server": "whois.nic.bj",
    "extend": "com",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Registrar:\s*(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "status": r"Status:\s?(.+)",
    "name_servers": r"Name Server:\s+(\S+)\n",
}

ZZ["cf"] = {
    "domain_name": None,
    "name_servers": r"Domain Nameservers:\n(?:(.+)\n)(?:(.+)\n)?(?:(.+)\n)?(?:(.+)\n)?",
    "registrar": r"Record maintained by:\s+(.+)",
    "creation_date": r"Domain registered:\s?(.+)",
    "expiration_date": r"Record will expire:\s?(.+)",
    "updated_date": None,
    "registrant_country": None,
    # very restrictive, after a few queries it will refuse with try again later
    "_slowdown": 5,
}

ZZ["re"] = {
    "extend": "ac",
    "registrant_country": None,
    "domain_name": r"domain:\s+(.+)",
    "registrar": r"registrar:\s+(.+)",
    "name_servers": r"nserver:\s+(.+)",
    "status": r"status:\s(.+)",
    "creation_date": r"created:\s+(.+)",
    "expiration_date": r"Expiry Date:\s+(.+)",
    "updated_date": r"last-update:\s+(.*)",
    "registrant_country": None,
}

ZZ["ro"] = {
    "domain_name": r"\s+Domain name:\s+(.+)",
    "registrar": r"\s+Registrar:\s+(.+)",
    "creation_date": r"\s+Registered On:\s+(.+)",
    "expiration_date": r"\s+Expires On:\s+(.+)",
    "status": r"\s+Domain Status:\s(.+)",
    "name_servers": r"\s+NameServer:\s+(.+)",
    "registrant_country": None,
    "updated_date": None,
}

ZZ["rs"] = {
    "domain_name": r"Domain name:\s+(.+)",
    "registrar": r"Registrar:\s+(.+)",
    "status": r"Domain status:\s(.+)",
    "creation_date": r"Registration date:\s+(.+)",
    "expiration_date": r"Expiration date:\s+(.+)",
    "updated_date": r"Modification date:\s+(.+)",
    "name_servers": r"DNS:\s+(.+)",
    "registrant_country": None,
}

# Singapore
ZZ["sg"] = {
    "_server": "whois.sgnic.sg",
    "registrar": r"Registrar:\s+(.+)",
    "domain_name": r"\s+Domain name:\s+(.+)",
    "creation_date": r"\s+Creation Date:\s+(.+)",
    "expiration_date": r"\s+Expiration Date:\s+(.+)",
    "updated_date": r"\s+Modified Date:\s+(.+)",
    "status": r"\s+Domain Status:\s(.+)",
    "registrant_country": None,
    "name_servers": r"Name Servers:%s" % xStr(r"(?:\n[ \t]+(\S+)[^\n]*)?", 4),
    # make sure the dnssec is not matched
    "_test": "google.sg",
}

ZZ["tw"] = {
    "_server": "whois.twnic.net.tw",
    "domain_name": r"Domain Name:\s+(.+)",
    "creation_date": r"\s+Record created on\s+(.+)",
    "expiration_date": r"\s+Record expires on\s+(.+)",
    "status": r"\s+Domain Status:\s+(.+)",
    "registrar": r"Registration\s+Service\s+Provider:\s+(.+)",
    "updated_date": None,
    "registrant_country": None,
    "name_servers": r"Domain servers in listed order:%s" % xStr(r"(?:\s+(\S+)[ \t]*\r?\n)?", 4),
    "_test": "google.tw",
}

ZZ["ug"] = {
    "_server": "whois.co.ug",
    "domain_name": r"Domain name:\s+(.+)",
    "creation_date": r"Registered On:\s+(.+)",
    "expiration_date": r"Expires On:\s+(.+)",
    "status": r"Status:\s+(.+)",
    "name_servers": r"Nameserver:\s+(.+)",
    "registrant_country": r"Registrant Country:\s+(.+)",
    "updated_date": r"Renewed On:\s+(.+)",
    "registrar": None,
}

ZZ["ws"] = {
    "domain_name": r"Domain Name:\s+(.+)",
    "creation_date": r"Creation Date:\s+(.+)",
    "expiration_date": r"Registrar Registration Expiration Date:\s+(.+)",
    "updated_date": r"Updated Date:\s?(.+)",
    "registrar": r"Registrar:\s+(.+)",
    "status": r"Domain Status:\s(.+)",
    "name_servers": r"Name Server:\s+(.+)",
    "registrant_country": None,
}

ZZ["re"] = {
    "domain_name": r"domain:\s+(.+)",
    "status": r"status:\s+(.+)",
    "registrar": r"registrar:\s+(.+)",
    "name_servers": r"nserver:\s+(.+)",
    "creation_date": r"created:\s+(.+)",
    "expiration_date": r"Expiry Date:\s+(.+)",
    "updated_date": r"last-update:\s+(.+)",
    "registrant_country": None,
}

ZZ["bo"] = {
    "domain_name": r"\s*NOMBRE DE DOMINIO:\s+(.+)",
    "registrant_country": r"País:\s+(.+)",
    "creation_date": r"Fecha de activación:\s+(.+)",
    "expiration_date": r"Fecha de corte:\s+(.+)",
    "registrar": None,
    "status": None,
    "name_servers": None,  # bo has no nameservers, use host -t ns <domain>
    "updated_date": None,
}

ZZ["hr"] = {
    "domain_name": r"Domain Name:\s+(.+)",
    "name_servers": r"Name Server:\s+(.+)",
    "creation_date": r"Creation Date:\s+(.+)",
    "updated_date": r"Updated Date:\s+(.+)",
    "status": None,
    "registrar": None,
    "expiration_date": r"Registrar Registration Expiration Date:\s+(.+)",
    "registrant_country": None,
}

ZZ["gg"] = {
    "domain_name": r"Domain:\s*\n\s+(.+)",
    "status": r"Domain Status:\s*\n\s+(.+)",
    "registrar": r"Registrar:\s*\n\s+(.+)",
    "name_servers": r"Name servers:(?:\n\s+(\S+))?(?:\n\s+(\S+))?(?:\n\s+(\S+))?(?:\n\s+(\S+))?\n",
    "creation_date": r"Relevant dates:\s*\n\s+Registered on(.+)",
    "expiration_date": None,
    "updated_date": None,
    "registrant_country": None,
}

ZZ["sn"] = {
    "_server": "whois.nic.sn",
    "domain_name": r"Nom de domaine:\s+(.+)",
    "status": r"Statut:\s+(.+)",
    "registrar": r"Registrar:\s+(.+)",
    "name_servers": r"Serveur de noms:\s*(.+)",
    "creation_date": r"Date de création:\s+(.+)",
    "expiration_date": r"Date d'expiration:\s+(.+)",
    "updated_date": r"Dernière modification:\s+(.+)",
    "registrant_country": None,
}

ZZ["si"] = {
    "domain_name": r"domain:\s+(.+)",
    "status": r"status:\s+(.+)",
    "registrar": r"registrar:\s+(.+)",
    "name_servers": r"nameserver:\s*(.+)",
    "creation_date": r"created:\s+(.+)",
    "expiration_date": r"expire:\s+(.+)",
    "updated_date": None,
    "registrant_country": None,
}

ZZ["st"] = {
    # .ST domains can now be registered with many different competing registrars. and hence different formats
    # >>> line appears quite early, valid info after would have been suppressed with the ^>>> cleanup rule: switched off
    "extend": "com",
    "registrant_country": r"registrant-country:\s+(\S+)",
    "registrant": r"registrant-organi(?:s|z)ation:\s*(.+)\r?\n",
    "expiration_date": r"Expiration\s+Date:\s?(.+)",
}

ZZ["mk"] = {
    "_server": "whois.marnet.mk",
    "domain_name": r"domain:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant": r"registrant:\s?(.+)",
    "registrant_country": r"Registrant Country:\s?(.+)",
    "creation_date": r"registered:\s?(.+)",
    "expiration_date": r"expire:\s?(.+)",
    "updated_date": r"changed:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)\s*",
    "status": r"Status:\s?(.+)",
    "emails": r"[\w\.-]+@[\w\.-]+\.[\w]{2,4}",
}

ZZ["si"] = {
    "_server": "whois.register.si",
    "domain_name": r"domain:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant": r"registrant:\s?(.+)",
    "registrant_country": r"Registrant Country:\s?(.+)",
    "creation_date": r"created:\s?(.+)",
    "expiration_date": r"expire:\s?(.+)",
    "updated_date": r"changed:\s?(.+)",
    "name_servers": r"nameserver:\s*(.+)\s*",
    "status": r"Status:\s?(.+)",
    "emails": r"[\w\.-]+@[\w\.-]+\.[\w]{2,4}",
}

ZZ["tc"] = {
    "extend": "com",
    "_server": "whois.nic.tc",
    "domain_name": r"Domain Name:\s?(.+)",
    "registrar": r"Sponsoring Registrar:\s?(.+)",
    "creation_date": r"Creation Date:\s?(.+)",
    "expiration_date": r"Registry Expiry Date:\s?(.+)",
    "name_servers": r"Name Server:\s*(.+)\s*",
    "status": r"Domain Status:\s?(.+)",
}

ZZ["wf"] = {
    "extend": "com",
    "_server": "whois.nic.wf",
    "domain_name": r"domain:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant": r"registrant:\s?(.+)",
    "registrant_country": r"Registrant Country:\s?(.+)",
    "creation_date": r"created:\s?(.+)",
    "expiration_date": r"Expiry Date:\s?(.+)",
    "updated_date": r"last-update:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)\s*",
    "status": r"\nstatus:\s?(.+)",
}

ZZ["mo"] = {
    "extend": "com",
    "_server": "whois.monic.mo",
    "name_servers": r"Domain name servers:\s+-+\s+(\S+)\n(?:(\S+)\n)?(?:(\S+)\n)?(?:(\S+)\n)?",
    "creation_date": r"Record created on (.+)",
    "expiration_date": r"Record expires on (.+)",
}

ZZ["tm"] = {  # Turkmenistan
    "extend": "com",
    "domain_name": r"Domain\s*:\s*(.+)",
    "expiration_date": r"Expiry\s*:\s*(\d+-\d+-\d+)",
    "name_servers": r"NS\s+\d+\s+:\s*(\S+)",
    "status": r"Status\s*:\s*(.+)",
}

# venezuela
ZZ["ve"] = {
    "extend": "com",
    "_server": "whois.nic.ve",
    "domain_name": r"domain\s*:\s?(.+)",
    "registrar": r"registrar:\s?(.+)",
    "registrant": r"registrant:\s?(.+)",
    "creation_date": r"created:\s?(.+)",
    "expiration_date": r"expire:\s?(.+)",
    "updated_date": r"changed\s*:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)\s*",
}

ZZ["lu"] = {
    "extend": "com",
    "_server": "whois.dns.lu",
    "domain_name": r"domainname\s*:\s?(.+)",
    "registrar": r"registrar-name:\s?(.+)",
    "name_servers": r"nserver:\s*(.+)\s*",
    "status": r"domaintype\s*:\s*(.+)",
    "registrant_country": r"org-country\s*:\s?(.+)",
}

ZZ["sm"] = {
    "extend": "rs",
    "_server": "whois.nic.sm",
    "domain_name": r"Domain Name:\s+(.+)",
    "status": r"Status:\s(.+)",
    "name_servers": r"DNS Servers:\s+(.+)",
}

ZZ["tg"] = {
    "_server": "whois.nic.tg",
    "extend": "com",
    "_test": "nic.tg",
    "domain_name": r"domain:\.+\s?(.+)",
    "registrar": r"registrar:\.+\s?(.+)",
    "creation_date": r"Activation:\.+\s?(.+)",
    "expiration_date": r"Expiration:\.+\s?(.+)",
    "status": r"Status:\.+\s?(.+)",
    "name_servers": r"Name Server \(DB\):\.+(.+)",
}

# ======================================
# ======================================
# ======================================

ZZ["aarp"] = {"_server": "whois.nic.aarp", "extend": "com", "_test": "nic.aarp"}
# ZZ["abarth"] = {"_server": "whois.afilias-srs.net", "extend": "com"}  # Revocation Report for .abarth 2023-06-05
ZZ["abbott"] = {"_server": "whois.nic.abbott", "extend": "com", "_test": "nic.abbott"}
ZZ["abbvie"] = {"_server": "whois.nic.abbvie", "extend": "com", "_test": "nic.abbvie"}
ZZ["abc"] = {"_server": "whois.nic.abc", "extend": "com", "_test": "nic.abc"}
ZZ["abogado"] = {"_server": "whois.nic.abogado", "extend": "com"}
ZZ["abudhabi"] = {"_server": "whois.nic.abudhabi", "extend": "com", "_test": "nic.abudhabi"}
ZZ["academy"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ac.bd"] = {"extend": "bd"}
ZZ["accountant"] = {"extend": "com", "_server": "whois.nic.accountant"}
ZZ["accountants"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ac.jp"] = {"extend": "co.jp", "_test": "icu.ac.jp"}
ZZ["ac.ke"] = {"extend": "ke"}
ZZ["aco"] = {"_server": "whois.nic.aco", "extend": "com", "_test": "nic.aco"}
ZZ["ac.rw"] = {"extend": "rw"}
ZZ["ac.th"] = {"extend": "co.th", "_test": "chula.ac.th"}
ZZ["active"] = {"_privateRegistry": True}
ZZ["actor"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ac.ug"] = {"extend": "ug", "_privateRegistry": True}
ZZ["adac"] = {"_privateRegistry": True}
ZZ["ad.jp"] = {"extend": "co.jp", "_test": "nic.ad.jp"}
ZZ["ads"] = {"_server": "whois.nic.ads", "extend": "com", "_test": "nic.ads"}
ZZ["adult"] = {"_server": "whois.nic.adult", "extend": "com"}
ZZ["aeg"] = {"_server": "whois.nic.aeg", "extend": "com", "_test": "nic.aeg"}
ZZ["aero"] = {"extend": "ac", "_server": "whois.aero", "registrant_country": r"Registrant\s+Country:\s+(.+)"}
ZZ["afamilycompany"] = {"_privateRegistry": True}
ZZ["af"] = {"extend": "ac"}
ZZ["afl"] = {"_server": "whois.nic.afl", "extend": "com", "_test": "nic.afl"}
ZZ["africa"] = {"extend": "com", "_server": "whois.nic.africa"}
ZZ["agakhan"] = {"_server": "whois.nic.agakhan", "extend": "com", "_test": "nic.agakhan"}
ZZ["agency"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ag"] = {"extend": "ac"}
ZZ["ai"] = {"extend": "com", "_server": "whois.nic.ai"}  # Anguilla
ZZ["aigo"] = {"_privateRegistry": True}
ZZ["airbus"] = {"_server": "whois.nic.airbus", "extend": "com", "_test": "nic.airbus"}
ZZ["airforce"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["airtel"] = {"_server": "whois.nic.airtel", "extend": "com", "_test": "nic.airtel"}
ZZ["akdn"] = {"_server": "whois.afilias-srs.net", "extend": "com", "_test": "nic.akdn"}
ZZ["al"] = {"extend": "_privateReg"}
# ZZ["alfaromeo"] = {"_server": "whois.afilias-srs.net", "extend": "com"} # Revocation of the .alfaromeo domain (2023-06-05)
ZZ["alibaba"] = {"_server": "whois.nic.alibaba", "extend": "com", "_test": "nic.alibaba"}
ZZ["alipay"] = {"_server": "whois.nic.alipay", "extend": "com", "_test": "nic.alipay"}
ZZ["allfinanz"] = {"_server": "whois.nic.allfinanz", "extend": "com", "_test": "nic.allfinanz"}
ZZ["allstate"] = {"_server": "whois.nic.allstate", "extend": "com", "_test": "nic.allstate"}
ZZ["ally"] = {"_server": "whois.nic.ally", "extend": "com", "_test": "nic.ally"}
ZZ["alsace"] = {"_server": "whois.nic.alsace", "extend": "com"}
ZZ["alstom"] = {"_server": "whois.nic.alstom", "extend": "com", "_test": "nic.alstom"}
ZZ["amazon"] = {"_server": "whois.nic.amazon", "extend": "com", "_test": "nic.amazon"}
ZZ["americanfamily"] = {"_server": "whois.nic.americanfamily", "extend": "com", "_test": "nic.americanfamily"}
ZZ["amfam"] = {"_server": "whois.nic.amfam", "extend": "com", "_test": "nic.amfam"}
ZZ["android"] = {"_server": "whois.nic.android", "extend": "com", "_test": "nic.android"}
ZZ["an"] = {"_privateRegistry": True}
ZZ["anquan"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["anz"] = {"_server": "whois.nic.anz", "extend": "com"}
ZZ["aol"] = {"_server": "whois.nic.aol", "extend": "com", "_test": "nic.aol"}
ZZ["apartments"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["app"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["apple"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["aquarelle"] = {"_server": "whois.nic.aquarelle", "extend": "com"}
ZZ["arab"] = {"_server": "whois.nic.arab", "extend": "com"}
ZZ["archi"] = {"_server": "whois.nic.archi", "extend": "com"}
ZZ["army"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["arte"] = {"_server": "whois.nic.arte", "extend": "com"}
ZZ["art"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["asda"] = {"_server": "whois.nic.asda", "extend": "com"}
ZZ["as"] = {"extend": "gg"}
ZZ["asia"] = {"extend": "com"}
ZZ["associates"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["attorney"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["auction"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["audible"] = {"_server": "whois.nic.audible", "extend": "com"}
ZZ["audio"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["audi"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["au"] = {"extend": "com", "registrar": r"Registrar Name:\s?(.+)", "updated_date": r"Last Modified:([^\n]*)"}
ZZ["auspost"] = {"_server": "whois.nic.auspost", "extend": "com"}
ZZ["author"] = {"_server": "whois.nic.author", "extend": "com"}
ZZ["auto"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["autos"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["avianca"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["aw"] = {"extend": "nl", "name_servers": r"Domain nameservers.*:\n%s" % xStr(r"(?:\s+(\S+)\n)?", 4)}
ZZ["aws"] = {"_server": "whois.nic.aws", "extend": "com"}
ZZ["az"] = {"extend": "_privateReg"}
ZZ["baby"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["ba"] = {"extend": "_privateReg"}
ZZ["baidu"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["band"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["barcelona"] = {"_server": "whois.nic.barcelona", "extend": "com"}
ZZ["barclaycard"] = {"_server": "whois.nic.barclaycard", "extend": "com"}
ZZ["barclays"] = {"_server": "whois.nic.barclays", "extend": "com"}
ZZ["barefoot"] = {"_server": "whois.nic.barefoot", "extend": "com"}
ZZ["bar"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["bargains"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["basketball"] = {"_server": "whois.nic.basketball", "extend": "com"}
ZZ["bauhaus"] = {"_server": "whois.nic.bauhaus", "extend": "com"}
ZZ["bayern"] = {"_server": "whois.nic.bayern", "extend": "com"}
ZZ["bbc"] = {"_server": "whois.nic.bbc", "extend": "com"}
ZZ["bbt"] = {"_server": "whois.nic.bbt", "extend": "com"}
ZZ["bbva"] = {"_server": "whois.nic.bbva", "extend": "com"}
ZZ["bcg"] = {"_server": "whois.nic.bcg", "extend": "com"}
ZZ["bcn"] = {"_server": "whois.nic.bcn", "extend": "com"}
ZZ["bd"] = {"extend": "_privateReg"}  # Bangladesh
ZZ["beats"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["beauty"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["beer"] = {"_server": "whois.nic.beer", "extend": "com"}
ZZ["bentley"] = {"_server": "whois.nic.bentley", "extend": "com"}
ZZ["berlin"] = {"_server": "whois.nic.berlin", "extend": "com"}
ZZ["bestbuy"] = {"_server": "whois.nic.bestbuy", "extend": "com"}
ZZ["best"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["bet"] = {"extend": "ac", "_server": "whois.nic.bet"}
ZZ["bf"] = {"extend": "com", "_server": "whois.nic.bf", "registrant": r"Registrant Name:\s?(.+)"}
ZZ["bible"] = {"_server": "whois.nic.bible", "extend": "com"}
ZZ["bid"] = {"extend": "ac", "_server": "whois.nic.bid"}
ZZ["bike"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["bingo"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["bio"] = {"_server": "whois.nic.bio", "extend": "com"}
ZZ["bi"] = {"_server": "whois1.nic.bi", "extend": "com"}
ZZ["blackfriday"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["black"] = {"_server": "whois.nic.black", "extend": "com"}
ZZ["blanco"] = {"_privateRegistry": True}
ZZ["blockbuster"] = {"_server": "whois.nic.blockbuster", "extend": "com"}
ZZ["blog"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["bl"] = {"_privateRegistry": True}
ZZ["blue"] = {"extend": "com"}
ZZ["bms"] = {"_server": "whois.nic.bms", "extend": "com"}
ZZ["bmw"] = {"_server": "whois.nic.bmw", "extend": "com"}
ZZ["bnl"] = {"_privateRegistry": True}
ZZ["bnpparibas"] = {"_server": "whois.afilias-srs.net", "extend": "com", "_test": "group.bnpparibas"}
ZZ["boats"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["boehringer"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["bofa"] = {"_server": "whois.nic.bofa", "extend": "com"}
ZZ["bom"] = {"extend": "com", "_server": "whois.gtlds.nic.br"}
ZZ["bond"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["book"] = {"_server": "whois.nic.book", "extend": "com"}
ZZ["boo"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["boots"] = {"_privateRegistry": True}
ZZ["bosch"] = {"_server": "whois.nic.bosch", "extend": "com"}
ZZ["bostik"] = {"_server": "whois.nic.bostik", "extend": "com"}
ZZ["boston"] = {"_server": "whois.nic.boston", "extend": "com"}
ZZ["bot"] = {"_server": "whois.nic.bot", "extend": "com"}
ZZ["boutique"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["box"] = {"_server": "whois.nic.box", "extend": "com"}
ZZ["bq"] = {"_privateRegistry": True}
ZZ["bradesco"] = {"_server": "whois.nic.bradesco", "extend": "com"}
ZZ["bridgestone"] = {"_server": "whois.nic.bridgestone", "extend": "com"}
ZZ["broadway"] = {"_server": "whois.nic.broadway", "extend": "com"}
ZZ["broker"] = {"_server": "whois.nic.broker", "extend": "com"}
ZZ["brother"] = {"_server": "whois.nic.brother", "extend": "com"}
ZZ["brussels"] = {"_server": "whois.nic.brussels", "extend": "com"}
ZZ["budapest"] = {"_privateRegistry": True}
ZZ["bugatti"] = {"_privateRegistry": True}
ZZ["builders"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["build"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["business"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["buy"] = {"_server": "whois.nic.buy", "extend": "com"}
ZZ["buzz"] = {"extend": "amsterdam"}
ZZ["bz"] = {"extend": "_privateReg"}
ZZ["cab"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ca"] = {"extend": "com"}
ZZ["cafe"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["call"] = {"_server": "whois.nic.call", "extend": "com"}
ZZ["cal"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["camera"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cam"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["camp"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cancerresearch"] = {"_privateRegistry": True}
ZZ["canon"] = {"_server": "whois.nic.canon", "extend": "com"}
ZZ["capetown"] = {"_server": "whois.nic.capetown", "extend": "com"}
ZZ["capital"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["capitalone"] = {"_server": "whois.nic.capitalone", "extend": "com"}
ZZ["cards"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["career"] = {"_server": "whois.nic.career", "extend": "com"}
ZZ["careers"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["care"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["car"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["cars"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["cartier"] = {"_privateRegistry": True}
ZZ["casa"] = {"extend": "ac", "registrant_country": r"Registrant Country:\s+(.+)"}
ZZ["caseih"] = {"_privateRegistry": True}
ZZ["case"] = {"_server": "whois.nic.case", "extend": "com"}
ZZ["cash"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["casino"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["catering"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cat"] = {"extend": "com", "_server": "whois.nic.cat"}
ZZ["catholic"] = {"_server": "whois.nic.catholic", "extend": "com"}
ZZ["ca.ug"] = {"extend": "ug"}
ZZ["cba"] = {"_server": "whois.nic.cba", "extend": "com"}
ZZ["cbs"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["cd"] = {"extend": "ac", "_server": "whois.nic.cd", "registrant_country": r"Registrant\s+Country:\s+(.+)"}
ZZ["ceb"] = {"_privateRegistry": True}
ZZ["center"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ceo"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["cern"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["cfa"] = {"_server": "whois.nic.cfa", "extend": "com"}
ZZ["cfd"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["chanel"] = {"_server": "whois.nic.chanel", "extend": "com"}
ZZ["channel"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["charity"] = {"extend": "_donuts", "_server": "whois.nic.charity"}
ZZ["chat"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cheap"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ch"] = {"extend": "_privateReg"}
ZZ["chintai"] = {"_server": "whois.nic.chintai", "extend": "com"}
ZZ["chloe"] = {"_privateRegistry": True}
ZZ["christmas"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["chrome"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["chrysler"] = {"_privateRegistry": True}
ZZ["church"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cipriani"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["circle"] = {"_server": "whois.nic.circle", "extend": "com"}
ZZ["ci"] = {"_server": "whois.nic.ci", "extend": "com"}
ZZ["cityeats"] = {"_server": "whois.nic.cityeats", "extend": "com"}
ZZ["city"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["claims"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cleaning"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["click"] = {"extend": "com"}
ZZ["clinic"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["clinique"] = {"_server": "whois.nic.clinique", "extend": "com"}
ZZ["clothing"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cloud"] = {"extend": "com"}
ZZ["club"] = {"extend": "com"}
ZZ["clubmed"] = {"_server": "whois.nic.clubmed", "extend": "com"}
ZZ["cm"] = {"extend": "com"}
ZZ["coach"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["codes"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["co"] = {"extend": "biz", "status": r"Status:\s?(.+)"}
ZZ["coffee"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["co.ke"] = {"extend": "ke"}
ZZ["college"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["cologne"] = {"_server": "whois.ryce-rsp.com", "extend": "com"}
ZZ["com.au"] = {"extend": "au"}
ZZ["com.bd"] = {"extend": "bd"}
ZZ["com.bo"] = {"extend": "bo"}
ZZ["comcast"] = {"_server": "whois.nic.comcast", "extend": "com"}
ZZ["com.cn"] = {"extend": "cn"}
ZZ["com.do"] = {"extend": "_privateReg"}
ZZ["com.ec"] = {"extend": "ec"}
ZZ["com.eg"] = {"extend": "_privateReg"}  # Egipt
ZZ["com.ly"] = {"extend": "ly"}
ZZ["commbank"] = {"_server": "whois.nic.commbank", "extend": "com"}
ZZ["com.mo"] = {"extend": "mo"}
ZZ["community"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["com.np"] = {"extend": "np"}
ZZ["company"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["compare"] = {"_server": "whois.nic.compare", "extend": "com"}
ZZ["com.ph"] = {"extend": "ph"}
ZZ["computer"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["com.py"] = {"extend": "_privateReg"}
ZZ["com.ru"] = {"extend": "ru", "_server": "whois.nic.ru", "_test": "mining.com.ru"}
ZZ["comsec"] = {"_server": "whois.nic.comsec", "extend": "com"}
ZZ["com.tm"] = {"extend": "tm", "_privateRegistry": True}
ZZ["com.tw"] = {"extend": "tw"}
ZZ["com.ua"] = {"extend": "ua"}
ZZ["com.ve"] = {"extend": "ve"}
ZZ["com.zw"] = {"extend": "zw"}
ZZ["condos"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["construction"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["consulting"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["contact"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["contractors"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["cookingchannel"] = {"_server": "whois.nic.cookingchannel", "extend": "com"}
ZZ["cooking"] = {"_server": "whois.nic.cooking", "extend": "com"}
ZZ["cool"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["coop"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["coop.rw"] = {"extend": "rw"}
ZZ["corsica"] = {"_server": "whois.nic.corsica", "extend": "com"}
ZZ["co.rw"] = {"extend": "rw"}
ZZ["co.ug"] = {"extend": "ug"}
ZZ["country"] = {"_server": "whois.nic.country", "extend": "com"}
ZZ["coupons"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["courses"] = {"extend": "com"}
ZZ["co.ve"] = {"extend": "ve"}
ZZ["co.za"] = {"extend": "za", "_server": "coza-whois.registry.net.za"}
ZZ["cpa"] = {"_server": "whois.nic.cpa", "extend": "com"}
ZZ["creditcard"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["credit"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["creditunion"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["cr"] = {"extend": "cz"}
ZZ["cricket"] = {"extend": "com", "_server": "whois.nic.cricket"}
ZZ["cruise"] = {"_server": "whois.nic.cruise", "extend": "com"}
ZZ["cruises"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["csc"] = {"_privateRegistry": True}
ZZ["cuisinella"] = {"_server": "whois.nic.cuisinella", "extend": "com"}
ZZ["cv"] = {"extend": "_privateReg"}  # Cape Verde
ZZ["cw"] = {"extend": "_privateReg"}
ZZ["cx"] = {"extend": "com"}
ZZ["cymru"] = {"_server": "whois.nic.cymru", "extend": "com"}
ZZ["cyou"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["dabur"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["dad"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["dance"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["data"] = {"_server": "whois.nic.data", "extend": "com"}
ZZ["date"] = {"extend": "com", "_server": "whois.nic.date"}
ZZ["dating"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["datsun"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["day"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["dclk"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["dds"] = {"_server": "whois.nic.dds", "extend": "com"}
ZZ["dealer"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["deal"] = {"_server": "whois.nic.deal", "extend": "com"}
ZZ["deals"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["degree"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["delivery"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["deloitte"] = {"_server": "whois.nic.deloitte", "extend": "com"}
ZZ["delta"] = {"_server": "whois.nic.delta", "extend": "com"}
ZZ["democrat"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["dental"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["dentist"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["desi"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["design"] = {"extend": "ac"}
ZZ["dev"] = {"extend": "com"}
ZZ["diamonds"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["diet"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["digital"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["direct"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["directory"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["discount"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["dish"] = {"_server": "whois.nic.dish", "extend": "com"}
ZZ["diy"] = {"_server": "whois.nic.diy", "extend": "com"}
ZZ["dm"] = {"_server": "whois.dmdomains.dm", "extend": "com"}
ZZ["dnp"] = {"_server": "whois.nic.dnp", "extend": "com"}
ZZ["docs"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["doctor"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["dodge"] = {"_privateRegistry": True}
ZZ["do"] = {"extend": "bzh", "_server": "whois.nic.do"}
ZZ["do"] = {"extend": "_privateReg"}
ZZ["dog"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["doha"] = {"_privateRegistry": True}
ZZ["domains"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["doosan"] = {"_privateRegistry": True}
ZZ["dot"] = {"_server": "whois.nic.dot", "extend": "com"}
ZZ["download"] = {"extend": "amsterdam", "name_servers": r"Name Server:[ \t]+(\S+)", "status": r"Domain Status:\s*([a-zA-z]+)"}
ZZ["drive"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["dtv"] = {"_server": "whois.nic.dtv", "extend": "com"}
ZZ["dubai"] = {"_server": "whois.nic.dubai", "extend": "com"}
ZZ["duckdns.org"] = {"extend": "_privateReg"}
ZZ["duck"] = {"_privateRegistry": True}
ZZ["dunlop"] = {"_server": "whois.nic.dunlop", "extend": "com"}
ZZ["duns"] = {"_privateRegistry": True}
ZZ["durban"] = {"_server": "whois.nic.durban", "extend": "com"}
ZZ["dvag"] = {"_server": "whois.nic.dvag", "extend": "com"}
ZZ["dvr"] = {"_server": "whois.nic.dvr", "extend": "com"}
ZZ["dz"] = {"extend": "_privateReg"}
ZZ["earth"] = {"_server": "whois.nic.earth", "extend": "com"}
ZZ["eat"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["ec"] = {"extend": "_privateReg"}
ZZ["eco"] = {"_server": "whois.nic.eco", "extend": "com"}
ZZ["edeka"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["ed.jp"] = {"extend": "co.jp"}
ZZ["education"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["edu.tr"] = {"extend": "com.tr", "_server": "whois.trabis.gov.tr", "_test": "anadolu.edu.tr"}
ZZ["edu.ua"] = {"extend": "ua", "creation_date": r"\ncreated:\s+0-UANIC\s+(.+)"}
ZZ["eg"] = {"extend": "_privateReg"}  # Egipt
ZZ["eh"] = {"_privateRegistry": True}
ZZ["email"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["emerck"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["energy"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["engineer"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["engineering"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["enterprises"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["epost"] = {"_privateRegistry": True}
ZZ["epson"] = {"_server": "whois.nic.epson", "extend": "com"}
ZZ["equipment"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ericsson"] = {"_server": "whois.nic.ericsson", "extend": "com"}
ZZ["erni"] = {"_server": "whois.nic.erni", "extend": "com"}
ZZ["es"] = {"extend": "_privateReg"}
ZZ["esq"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["estate"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["esurance"] = {"_privateRegistry": True}
ZZ["et"] = {"extend": "com", "_server": "whois.ethiotelecom.et"}
ZZ["etisalat"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["eurovision"] = {"_server": "whois.nic.eurovision", "extend": "com"}
ZZ["eus"] = {"extend": "ac"}
ZZ["events"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["everbank"] = {"_privateRegistry": True}
ZZ["exchange"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["expert"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["exposed"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["express"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["extraspace"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["fage"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["fail"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fairwinds"] = {"_server": "whois.nic.fairwinds", "extend": "com"}
ZZ["faith"] = {"extend": "com", "_server": "whois.nic.faith"}
ZZ["family"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fan"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fans"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["farm"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fashion"] = {"extend": "com", "_server": "whois.nic.fashion"}
ZZ["fast"] = {"_server": "whois.nic.fast", "extend": "com"}
ZZ["fedex"] = {"_server": "whois.nic.fedex", "extend": "com"}
ZZ["feedback"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["ferrari"] = {"_server": "whois.nic.ferrari", "extend": "com"}
ZZ["fiat"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["fidelity"] = {"_server": "whois.nic.fidelity", "extend": "com"}
ZZ["fido"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["film"] = {"_server": "whois.nic.film", "extend": "com"}
ZZ["final"] = {"_server": "whois.gtlds.nic.br", "extend": "bom"}
ZZ["finance"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["financial"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fire"] = {"_server": "whois.nic.fire", "extend": "com"}
ZZ["firestone"] = {"_server": "whois.nic.firestone", "extend": "com"}
ZZ["firmdale"] = {"_server": "whois.nic.firmdale", "extend": "com"}
ZZ["fish"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fishing"] = {"_server": "whois.nic.fishing", "extend": "com"}
ZZ["fit"] = {"extend": "com"}
ZZ["fitness"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["flights"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["florist"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["flowers"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["flsmidth"] = {"_privateRegistry": True}
ZZ["fly"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["fm"] = {"extend": "com"}
ZZ["fo"] = {"extend": "com", "registrant": None}
ZZ["foodnetwork"] = {"_server": "whois.nic.foodnetwork", "extend": "com"}
ZZ["foo"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["football"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["forex"] = {"_server": "whois.nic.forex", "extend": "com"}
ZZ["forsale"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["forum"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["foundation"] = {"extend": "_donuts", "_server": "whois.nic.foundation"}
ZZ["fox"] = {"_server": "whois.nic.fox", "extend": "com"}
ZZ["free"] = {"_server": "whois.nic.free", "extend": "com"}
ZZ["fresenius"] = {"_server": "whois.nic.fresenius", "extend": "com"}
ZZ["frl"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["frogans"] = {"_server": "whois.nic.frogans", "extend": "com"}
ZZ["frontdoor"] = {"_server": "whois.nic.frontdoor", "extend": "com"}
ZZ["fujitsu"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["fujixerox"] = {"_privateRegistry": True}
ZZ["fund"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fun"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["furniture"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["futbol"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["fyi"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ga"] = {"extend": "_privateReg"}
ZZ["gallery"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gallo"] = {"_server": "whois.nic.gallo", "extend": "com"}
ZZ["gallup"] = {"_server": "whois.nic.gallup", "extend": "com"}
ZZ["gal"] = {"_server": "whois.nic.gal", "extend": "com"}
ZZ["game"] = {"extend": "amsterdam"}
ZZ["games"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["garden"] = {"extend": "com", "_server": "whois.nic.garden"}
ZZ["gay"] = {"extend": "com", "_server": "whois.nic.gay"}
ZZ["gbiz"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["gd"] = {"extend": "com"}
ZZ["gdn"] = {"_server": "whois.nic.gdn", "extend": "com"}
ZZ["gea"] = {"_server": "whois.nic.gea", "extend": "com"}
ZZ["gent"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["genting"] = {"_server": "whois.nic.genting", "extend": "com"}
ZZ["geo.jp"] = {"extend": "co.jp"}
ZZ["george"] = {"_server": "whois.nic.george", "extend": "com"}
ZZ["ge"] = {"_server": "whois.nic.ge", "extend": "ac", "updated_date": None}
ZZ["gf"] = {"extend": "si", "_server": "whois.mediaserv.net"}
ZZ["ggee"] = {"_server": "whois.nic.ggee", "extend": "com"}
ZZ["gift"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["gifts"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gi"] = {"_server": "whois2.afilias-grs.net", "extend": "com"}
ZZ["gives"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["giving"] = {"_server": "whois.nic.giving", "extend": "com"}
ZZ["glade"] = {"_privateRegistry": True}
ZZ["glass"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gle"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["global"] = {"extend": "amsterdam", "name_servers": r"Name Server: (.+)"}
ZZ["globo"] = {"_server": "whois.gtlds.nic.br", "extend": "bom"}
ZZ["gl"] = {"_server": "whois.nic.gl", "extend": "com"}
ZZ["gmail"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["gmbh"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gmo"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["gmx"] = {"_server": "whois.nic.gmx", "extend": "com"}
ZZ["gob.ec"] = {"extend": "ec"}
ZZ["godaddy"] = {"_server": "whois.nic.godaddy", "extend": "com"}
ZZ["go.jp"] = {"extend": "co.jp"}
ZZ["go.ke"] = {"extend": "ke"}
ZZ["gold"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["goldpoint"] = {"_server": "whois.nic.goldpoint", "extend": "com"}
ZZ["golf"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["goodhands"] = {"_privateRegistry": True}
ZZ["goodyear"] = {"_server": "whois.nic.goodyear", "extend": "com"}
ZZ["google"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["goog"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["goo"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["gop"] = {"_server": "whois.nic.gop", "extend": "com"}
ZZ["go.th"] = {"extend": "co.th"}
ZZ["got"] = {"_server": "whois.nic.got", "extend": "com"}
ZZ["gov.bd"] = {"extend": "bd"}
ZZ["gov"] = {"extend": "com"}
ZZ["gov.rw"] = {"extend": "rw"}
ZZ["gov.tr"] = {"extend": "com.tr", "_server": "whois.trabis.gov.tr", "_test": "www.turkiye.gov.tr"}
ZZ["gov.uk"] = {"extend": "ac.uk"}
ZZ["gq"] = {"extend": "ml", "_server": "whois.domino.gq"}
ZZ["graphics"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gratis"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["green"] = {"extend": "com"}
ZZ["gr"] = {"extend": "_privateReg"}
ZZ["gripe"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gr.jp"] = {"extend": "co.jp"}
ZZ["group"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gs"] = {"_server": "whois.nic.gs", "extend": "com"}
ZZ["gt"] = {"extend": "_privateReg"}
ZZ["gucci"] = {"_server": "whois.nic.gucci", "extend": "com"}
ZZ["guge"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["guide"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["guitars"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["guru"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["gy"] = {"extend": "com"}
ZZ["hair"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["hamburg"] = {"_server": "whois.nic.hamburg", "extend": "com"}
ZZ["hangout"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["haus"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["hdfcbank"] = {"_server": "whois.nic.hdfcbank", "extend": "com"}
ZZ["hdfc"] = {"_server": "whois.nic.hdfc", "extend": "com"}
ZZ["healthcare"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["health"] = {"extend": "com", "_server": "whois.nic.health"}
ZZ["help"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["helsinki"] = {"_server": "whois.nic.helsinki", "extend": "com"}
ZZ["here"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["hermes"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["hgtv"] = {"_server": "whois.nic.hgtv", "extend": "com"}
ZZ["hiphop"] = {"extend": "com", "_server": "whois.nic.hiphop"}
ZZ["hisamitsu"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["hitachi"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["hiv"] = {"_server": "whois.nic.hiv", "extend": "com"}
ZZ["hkt"] = {"_server": "whois.nic.hkt", "extend": "com"}
ZZ["hn"] = {"extend": "com"}  # Honduras
ZZ["hockey"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["holdings"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["holiday"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["homedepot"] = {"_server": "whois.nic.homedepot", "extend": "com"}
ZZ["homes"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["honda"] = {"_server": "whois.nic.honda", "extend": "com"}
ZZ["honeywell"] = {"_privateRegistry": True}
ZZ["hopto.org"] = {"extend": "_privateReg"}  # dynamic dns without any whois
ZZ["horse"] = {"_server": "whois.nic.horse", "extend": "com"}
ZZ["hospital"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["host"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["hosting"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["hot"] = {"_server": "whois.nic.hot", "extend": "com"}
ZZ["house"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["how"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["htc"] = {"_privateRegistry": True}
ZZ["ht"] = {"_server": "whois.nic.ht", "extend": "com"}
ZZ["hu"] = {"extend": "_privateReg"}
ZZ["hughes"] = {"_server": "whois.nic.hughes", "extend": "com"}
ZZ["hyundai"] = {"_server": "whois.nic.hyundai", "extend": "com"}
ZZ["ibm"] = {"_server": "whois.nic.ibm", "extend": "com"}
ZZ["icbc"] = {"_server": "whois.nic.icbc", "extend": "com"}
ZZ["ice"] = {"_server": "whois.nic.ice", "extend": "com"}
ZZ["icu"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["ie"] = {"extend": "com"}  # Ireland
ZZ["ifm"] = {"_server": "whois.nic.ifm", "extend": "com"}
ZZ["iinet"] = {"_privateRegistry": True}
ZZ["ikano"] = {"_server": "whois.nic.ikano", "extend": "com"}
ZZ["imamat"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["imdb"] = {"_server": "whois.nic.imdb", "extend": "com"}
ZZ["immobilien"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["immo"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["inc"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["industries"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["in"] = {"extend": "com", "_server": "whois.registry.in"}
ZZ["infiniti"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["info"] = {"extend": "com"}
ZZ["info.ke"] = {"extend": "ke"}
ZZ["info.ve"] = {"extend": "ve"}
ZZ["ing"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["ink"] = {"extend": "amsterdam"}
ZZ["institute"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["insurance"] = {"_server": "whois.nic.insurance", "extend": "com"}
ZZ["insure"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["intel"] = {"_privateRegistry": True}
ZZ["international"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["in.th"] = {"extend": "co.th"}
ZZ["investments"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["io"] = {"extend": "com", "expiration_date": r"\nRegistry Expiry Date:\s?(.+)"}
ZZ["irish"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["iselect"] = {"_privateRegistry": True}
ZZ["ismaili"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["istanbul"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["ist"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["itv"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["iveco"] = {"_privateRegistry": True}
ZZ["iwc"] = {"_privateRegistry": True}
ZZ["jaguar"] = {"_server": "whois.nic.jaguar", "extend": "com"}
ZZ["java"] = {"_server": "whois.nic.java", "extend": "com"}
ZZ["jcb"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["jcp"] = {"_privateRegistry": True}
ZZ["jeep"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["je"] = {"extend": "gg"}
ZZ["jetzt"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["jewelry"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["jio"] = {"_server": "whois.nic.jio", "extend": "com"}
ZZ["jlc"] = {"_privateRegistry": True}
ZZ["jll"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["jobs"] = {"_server": "whois.nic.jobs", "extend": "com"}
ZZ["joburg"] = {"_server": "whois.nic.joburg", "extend": "com"}
ZZ["jot"] = {"_server": "whois.nic.jot", "extend": "com"}
ZZ["joy"] = {"_server": "whois.nic.joy", "extend": "com"}
ZZ["juegos"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["juniper"] = {"_server": "whois.nic.juniper", "extend": "com"}
ZZ["kaufen"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["kddi"] = {"_server": "whois.nic.kddi", "extend": "com"}
ZZ["ke"] = {"extend": "com", "_server": "whois.kenic.or.ke"}
ZZ["kerryhotels"] = {"_server": "whois.nic.kerryhotels", "extend": "com"}
ZZ["kerrylogistics"] = {"_server": "whois.nic.kerrylogistics", "extend": "com"}
ZZ["kerryproperties"] = {"_server": "whois.nic.kerryproperties", "extend": "com"}
ZZ["kfh"] = {"_server": "whois.nic.kfh", "extend": "com"}
ZZ["kia"] = {"_server": "whois.nic.kia", "extend": "com"}
ZZ["kids"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["ki"] = {"extend": "com", "_server": "whois.nic.ki"}
ZZ["kim"] = {"_server": "whois.nic.kim", "extend": "com"}
ZZ["kindle"] = {"_server": "whois.nic.kindle", "extend": "com"}
ZZ["kitchen"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["kiwi"] = {"extend": "com"}
ZZ["kn"] = {"extend": "com"}  # Saint Kitts and Nevis
ZZ["koeln"] = {"_server": "whois.ryce-rsp.com", "extend": "com"}
ZZ["komatsu"] = {"_server": "whois.nic.komatsu", "extend": "com"}
ZZ["kosher"] = {"_server": "whois.nic.kosher", "extend": "com"}
ZZ["krd"] = {"_server": "whois.nic.krd", "extend": "com"}
ZZ["kred"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["kuokgroup"] = {"_server": "whois.nic.kuokgroup", "extend": "com"}
ZZ["kyoto"] = {"_server": "whois.nic.kyoto", "extend": "com"}
ZZ["ky"] = {"_server": "whois.kyregistry.ky", "extend": "com"}
ZZ["lacaixa"] = {"_server": "whois.nic.lacaixa", "extend": "com"}
ZZ["ladbrokes"] = {"_privateRegistry": True}
ZZ["la"] = {"extend": "com"}
ZZ["lamborghini"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["lamer"] = {"_server": "whois.nic.lamer", "extend": "com"}
ZZ["lancaster"] = {"_server": "whois.nic.lancaster", "extend": "com"}
ZZ["lancia"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["lancome"] = {"_privateRegistry": True}
ZZ["land"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["landrover"] = {"_server": "whois.nic.landrover", "extend": "com"}
ZZ["lasalle"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["lat"] = {"extend": "com"}
ZZ["latino"] = {"_server": "whois.nic.latino", "extend": "com"}
ZZ["latrobe"] = {"_server": "whois.nic.latrobe", "extend": "com"}
ZZ["law"] = {"_server": "whois.nic.law", "extend": "com"}
ZZ["lawyer"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["lb"] = {"_server": "whois.lbdr.org.lb", "extend": "com"}
ZZ["lc"] = {"extend": "com", "_server": "whois2.afilias-grs.net"}
ZZ["lds"] = {"_server": "whois.nic.lds", "extend": "com"}
ZZ["lease"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["leclerc"] = {"_server": "whois.nic.leclerc", "extend": "com"}
ZZ["lefrak"] = {"_server": "whois.nic.lefrak", "extend": "com"}
ZZ["legal"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["lego"] = {"_server": "whois.nic.lego", "extend": "com"}
ZZ["lexus"] = {"_server": "whois.nic.lexus", "extend": "com"}
ZZ["lgbt"] = {"_server": "whois.nic.lgbt", "extend": "com"}
ZZ["lg.jp"] = {"extend": "co.jp"}
ZZ["liaison"] = {"_privateRegistry": True}
ZZ["lidl"] = {"_server": "whois.nic.lidl", "extend": "com"}
ZZ["li"] = {"extend": "_privateReg"}
ZZ["life"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["lifestyle"] = {"_server": "whois.nic.lifestyle", "extend": "com"}
ZZ["lighting"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["like"] = {"_server": "whois.nic.like", "extend": "com"}
ZZ["limited"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["limo"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["linde"] = {"_server": "whois.nic.linde", "extend": "com"}
ZZ["link"] = {"extend": "amsterdam"}
ZZ["lipsy"] = {"_server": "whois.nic.lipsy", "extend": "com"}
ZZ["live"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["lixil"] = {"_privateRegistry": True}
ZZ["lk"] = {"extend": "_privateReg"}  # Sri Lanka
ZZ["llc"] = {"_server": "whois.nic.llc", "extend": "com"}
ZZ["llp"] = {"_server": "whois.nic.llp", "extend": "com"}
ZZ["loan"] = {"extend": "com", "_server": "whois.nic.loan"}
ZZ["loans"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["locker"] = {"_server": "whois.nic.locker", "extend": "com"}
ZZ["locus"] = {"_server": "whois.nic.locus", "extend": "com"}
ZZ["loft"] = {"_privateRegistry": True}
ZZ["lol"] = {"extend": "amsterdam"}
ZZ["london"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["lotte"] = {"_server": "whois.nic.lotte", "extend": "com"}
ZZ["lotto"] = {"_server": "whois.nic.lotto", "extend": "com"}
ZZ["love"] = {"extend": "ac", "registrant_country": r"Registrant\s+Country:\s+(.+)"}
ZZ["lplfinancial"] = {"_server": "whois.nic.lplfinancial", "extend": "com"}
ZZ["lpl"] = {"_server": "whois.nic.lpl", "extend": "com"}
ZZ["ls"] = {"extend": "cz", "_server": "whois.nic.ls"}
ZZ["ltda"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["ltd"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["lundbeck"] = {"_server": "whois.nic.lundbeck", "extend": "com"}
ZZ["lupin"] = {"_privateRegistry": True}
ZZ["luxe"] = {"_server": "whois.nic.luxe", "extend": "com"}
ZZ["luxury"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["lviv.ua"] = {"extend": "com"}
ZZ["ly"] = {"extend": "ac", "_server": "whois.nic.ly", "registrant_country": r"Registrant\s+Country:\s+(.+)"}
ZZ["macys"] = {"_server": "whois.nic.macys", "extend": "com"}
ZZ["madrid"] = {"_server": "whois.nic.madrid", "extend": "com"}
ZZ["ma"] = {"extend": "ac", "_server": "whois.registre.ma", "registrar": r"Sponsoring Registrar:\s*(.+)"}
ZZ["maison"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["makeup"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["management"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["mango"] = {"_server": "whois.nic.mango", "extend": "com"}
ZZ["man"] = {"_server": "whois.nic.man", "extend": "com"}
ZZ["map"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["market"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["marketing"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["markets"] = {"_server": "whois.nic.markets", "extend": "com"}
ZZ["marriott"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["maserati"] = {"_server": "whois.nic.maserati", "extend": "com"}
ZZ["mba"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["mcdonalds"] = {"_privateRegistry": True}
ZZ["mcd"] = {"_privateRegistry": True}
ZZ["mckinsey"] = {"_server": "whois.nic.mckinsey", "extend": "com"}
ZZ["md"] = {"extend": "ug", "_server": "whois.nic.md"}
ZZ["media"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["med"] = {"_server": "whois.nic.med", "extend": "com"}
ZZ["meet"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["me.ke"] = {"extend": "ke"}
ZZ["melbourne"] = {"_server": "whois.nic.melbourne", "extend": "com"}
ZZ["meme"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["memorial"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["men"] = {"_server": "whois.nic.men", "extend": "com"}
ZZ["menu"] = {"_server": "whois.nic.menu", "extend": "com"}
ZZ["meo"] = {"_privateRegistry": True}
ZZ["metlife"] = {"_privateRegistry": True}
ZZ["mf"] = {"_privateRegistry": True}
ZZ["mg"] = {"extend": "ac", "registrant_country": r"Registrant\s+Country:\s+(.+)"}
ZZ["miami"] = {"_server": "whois.nic.miami", "extend": "com"}
ZZ["mil.rw"] = {"extend": "rw"}
ZZ["mini"] = {"_server": "whois.nic.mini", "extend": "com"}
ZZ["mit"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["mitsubishi"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["mls"] = {"_server": "whois.nic.mls", "extend": "com"}
ZZ["mma"] = {"_server": "whois.nic.mma", "extend": "com"}
ZZ["mn"] = {"extend": "com"}
ZZ["mn"] = {"extend": "com", "_server": "whois.nic.mn"}
ZZ["mobi"] = {"extend": "com", "expiration_date": r"\nRegistry Expiry Date:\s?(.+)", "updated_date": r"\nUpdated Date:\s?(.+)"}
ZZ["mobi.ke"] = {"extend": "ke"}
ZZ["mobile"] = {"_server": "whois.nic.mobile", "extend": "com"}
ZZ["mobily"] = {"_privateRegistry": True}
ZZ["moda"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["moe"] = {"extend": "ac", "registrant_country": r"Registrant\s+Country:\s+(.+)"}
ZZ["moi"] = {"_server": "whois.nic.moi", "extend": "com"}
ZZ["mom"] = {"_server": "whois.nic.mom", "extend": "com"}
ZZ["monash"] = {"_server": "whois.nic.monash", "extend": "com"}
ZZ["money"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["monster"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["montblanc"] = {"_privateRegistry": True}
ZZ["mopar"] = {"_privateRegistry": True}
ZZ["mormon"] = {"_server": "whois.nic.mormon", "extend": "com", "_test": "nic.mormon"}
ZZ["mortgage"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["moscow"] = {"_server": "whois.nic.moscow", "extend": "com"}
ZZ["motorcycles"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["mov"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["movie"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["movistar"] = {"_privateRegistry": True}
ZZ["mp"] = {"extend": "_privateReg"}
ZZ["mq"] = {"extend": "si", "_server": "whois.mediaserv.net"}
ZZ["mr"] = {"_server": "whois.nic.mr", "extend": "com"}
ZZ["msk.ru"] = {"extend": "com.ru"}  # test with: mining.msk.ru
ZZ["ms"] = {"_server": "whois.nic.ms", "extend": "com"}
ZZ["mtn"] = {"_server": "whois.nic.mtn", "extend": "com"}
ZZ["mtpc"] = {"_privateRegistry": True}
ZZ["mtr"] = {"_server": "whois.nic.mtr", "extend": "com"}
ZZ["mu"] = {"extend": "bank"}
ZZ["mu"] = {"extend": "bank"}
ZZ["museum"] = {"_server": "whois.nic.museum", "extend": "com"}
ZZ["music"] = {"_server": "whois.nic.music", "extend": "com"}
ZZ["mutuelle"] = {"_privateRegistry": True}
ZZ["my"] = {"extend": "_privateReg"}
ZZ["mz"] = {"_server": "whois.nic.mz", "extend": "com"}
ZZ["nab"] = {"_server": "whois.nic.nab", "extend": "com"}
ZZ["nadex"] = {"_privateRegistry": True}
ZZ["nagoya"] = {"_server": "whois.nic.nagoya", "extend": "com"}
ZZ["name"] = {"extend": "com", "status": r"Domain Status:\s?(.+)"}
ZZ["na"] = {"_server": "whois.na-nic.com.na", "extend": "com"}
ZZ["nationwide"] = {"_privateRegistry": True}
ZZ["natura"] = {"_server": "whois.gtlds.nic.br", "extend": "bom"}
ZZ["navy"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["nec"] = {"_server": "whois.nic.nec", "extend": "com"}
ZZ["ne.jp"] = {"extend": "co.jp"}
ZZ["ne.ke"] = {"extend": "ke"}
ZZ["netbank"] = {"_server": "whois.nic.netbank", "extend": "com"}
ZZ["net.bd"] = {"extend": "bd"}
ZZ["net"] = {"extend": "com"}
ZZ["net.ph"] = {"extend": "ph"}
ZZ["net.rw"] = {"extend": "rw"}
ZZ["net.tr"] = {"extend": "com.tr", "_server": "whois.trabis.gov.tr", "_test": "trt.net.tr"}
ZZ["net.ua"] = {"extend": "ua"}
ZZ["net.ve"] = {"extend": "ve"}
ZZ["network"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["net.za"] = {"extend": "za", "_server": "net-whois.registry.net.za"}
ZZ["newholland"] = {"_privateRegistry": True}
ZZ["new"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["news"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["nextdirect"] = {"_server": "whois.nic.nextdirect", "extend": "com"}
ZZ["next"] = {"_server": "whois.nic.next", "extend": "com"}
ZZ["nexus"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["nf"] = {"_server": "whois.nic.nf", "extend": "com"}
ZZ["ngo"] = {"_server": "whois.nic.ngo", "extend": "com"}
ZZ["ng"] = {"_server": "whois.nic.net.ng", "extend": "ac", "registrant_country": r"Registrant Country:\s+(.+)"}
ZZ["nhk"] = {"_server": "whois.nic.nhk", "extend": "com"}
ZZ["nico"] = {"_server": "whois.nic.nico", "extend": "com"}
ZZ["nikon"] = {"_server": "whois.nic.nikon", "extend": "com"}
ZZ["ninja"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["nissan"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["nissay"] = {"_server": "whois.nic.nissay", "extend": "com"}
ZZ["noip.com"] = {"extend": "_privateReg"}
ZZ["noip.org"] = {"extend": "_privateReg"}
ZZ["nokia"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["norton"] = {"_server": "whois.nic.norton", "extend": "com"}
ZZ["nowruz"] = {"_server": "whois.nic.nowruz", "extend": "com"}
ZZ["now"] = {"_server": "whois.nic.now", "extend": "com"}
ZZ["nowtv"] = {"_server": "whois.nic.nowtv", "extend": "com"}
ZZ["np"] = {"extend": "_privateReg"}
ZZ["nra"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["nrw"] = {"extend": "com"}
ZZ["nu"] = {"extend": "se"}
ZZ["obi"] = {"_server": "whois.nic.obi", "extend": "com"}
ZZ["observer"] = {"extend": "com", "_server": "whois.nic.observer"}
ZZ["off"] = {"_privateRegistry": True}
ZZ["okinawa"] = {"_server": "whois.nic.okinawa", "extend": "com"}
ZZ["olayangroup"] = {"_server": "whois.nic.olayangroup", "extend": "com"}
ZZ["olayan"] = {"_server": "whois.nic.olayan", "extend": "com"}
ZZ["ollo"] = {"_server": "whois.nic.ollo", "extend": "com"}
ZZ["omega"] = {"_server": "whois.nic.omega", "extend": "com"}
ZZ["om"] = {"_server": "whois.registry.om", "extend": "com", "_test": "registry.om"}
ZZ["one"] = {"extend": "com", "_server": "whois.nic.one"}
ZZ["ong"] = {"extend": "ac", "registrant_country": r"Registrant Country:\s+(.+)"}
ZZ["onion"] = {"extend": "_privateReg"}
ZZ["onl"] = {"extend": "com"}
ZZ["online"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["onyourside"] = {"_privateRegistry": True}
ZZ["ooo"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["oracle"] = {"_server": "whois.nic.oracle", "extend": "com"}
ZZ["orange"] = {"_server": "whois.nic.orange", "extend": "com"}
ZZ["organic"] = {"_server": "whois.nic.organic", "extend": "com"}
ZZ["org.ph"] = {"extend": "ph"}
ZZ["org.rw"] = {"extend": "rw"}
ZZ["org.tr"] = {"extend": "com.tr", "_server": "whois.trabis.gov.tr", "_test": "dergipark.org.tr"}
ZZ["org.uk"] = {"extend": "co.uk"}
ZZ["org.ve"] = {"extend": "ve"}
ZZ["org.za"] = {"extend": "za", "_server": "org-whois.registry.net.za"}
ZZ["org.zw"] = {"extend": "zw"}
ZZ["orientexpress"] = {"_privateRegistry": True}
ZZ["origins"] = {"_server": "whois.nic.origins", "extend": "com"}
ZZ["or.jp"] = {"extend": "co.jp"}
ZZ["or.ke"] = {"extend": "ke"}
ZZ["osaka"] = {"_server": "whois.nic.osaka", "extend": "com"}
ZZ["otsuka"] = {"_server": "whois.nic.otsuka", "extend": "com"}
ZZ["ott"] = {"_server": "whois.nic.ott", "extend": "com"}
ZZ["ovh"] = {"extend": "com", "_server": "whois.nic.ovh"}
ZZ["page"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["pamperedchef"] = {"_privateRegistry": True}
ZZ["panasonic"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["panerai"] = {"_privateRegistry": True}
ZZ["paris"] = {"_server": "whois.nic.paris", "extend": "com"}
ZZ["pars"] = {"_server": "whois.nic.pars", "extend": "com"}
ZZ["partners"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["parts"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["party"] = {"extend": "com", "_server": "whois.nic.party"}
ZZ["pay"] = {"_server": "whois.nic.pay", "extend": "com"}
ZZ["pccw"] = {"_server": "whois.nic.pccw", "extend": "com"}
ZZ["pe"] = {"extend": "com", "registrant": r"Registrant Name:\s?(.+)", "admin": r"Admin Name:\s?(.+)"}
ZZ["pet"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["phd"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["ph"] = {"extend": "_privateReg"}
ZZ["ph"] = {"extend": "_privateReg"}
ZZ["philips"] = {"_server": "whois.nic.philips", "extend": "com"}
ZZ["phone"] = {"_server": "whois.nic.phone", "extend": "com"}
ZZ["photo"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["photography"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["photos"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["physio"] = {"_server": "whois.nic.physio", "extend": "com"}
ZZ["piaget"] = {"_privateRegistry": True}
ZZ["pics"] = {"extend": "ac"}
ZZ["pictures"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["pid"] = {"_server": "whois.nic.pid", "extend": "com"}
ZZ["pink"] = {"_server": "whois.nic.pink", "extend": "com"}
ZZ["pin"] = {"_server": "whois.nic.pin", "extend": "com"}
ZZ["pioneer"] = {"_server": "whois.nic.pioneer", "extend": "com"}
ZZ["pizza"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["pk"] = {"extend": "_privateReg"}
ZZ["place"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["play"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["playstation"] = {"_server": "whois.nic.playstation", "extend": "com"}
ZZ["plumbing"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["plus"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["pm"] = {"extend": "re", "_server": "whois.nic.pm"}
ZZ["pnc"] = {"_server": "whois.nic.pnc", "extend": "com"}
ZZ["pohl"] = {"_server": "whois.nic.pohl", "extend": "com"}
ZZ["poker"] = {"_server": "whois.nic.poker", "extend": "com"}
ZZ["politie"] = {"_server": "whois.nic.politie", "extend": "com"}
ZZ["porn"] = {"_server": "whois.nic.porn", "extend": "com"}
ZZ["press"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["prime"] = {"_server": "whois.nic.prime", "extend": "com"}
ZZ["테스트"] = {"_privateRegistry": True}
ZZ["prod"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["productions"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["pro"] = {"extend": "com", "_test": "nic.pro"}
ZZ["prof"] = {"extend": "com", "_server": "whois.nic.google"}
ZZ["progressive"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["promo"] = {"extend": "com", "_server": "whois.nic.promo"}
ZZ["properties"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["property"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["protection"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["pr"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["ps"] = {"_privateRegistry": True}  # no host can be contacted only http://www.nic.ps
ZZ["pub"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["pwc"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["pyc"] = {"extend": "com"}
ZZ["py"] = {"extend": "_privateReg"}  # Paraguay
ZZ["qa"] = {"_server": "whois.registry.qa", "extend": "com"}
ZZ["qpon"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["quebec"] = {"_server": "whois.nic.quebec", "extend": "com"}
ZZ["quest"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["qvc"] = {"_privateRegistry": True}
ZZ["racing"] = {"extend": "com", "_server": "whois.nic.racing"}
ZZ["radio"] = {"extend": "com", "_server": "whois.nic.radio"}
ZZ["raid"] = {"_privateRegistry": True}
ZZ["read"] = {"_server": "whois.nic.read", "extend": "com"}
ZZ["realestate"] = {"_server": "whois.nic.realestate", "extend": "com"}
ZZ["realty"] = {"_server": "whois.nic.realty", "extend": "com"}
ZZ["recipes"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["red"] = {"extend": "com"}
ZZ["redstone"] = {"_server": "whois.nic.redstone", "extend": "com"}
ZZ["redumbrella"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["rehab"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["reise"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["reisen"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["reit"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["reliance"] = {"_server": "whois.nic.reliance", "extend": "com"}
ZZ["ren"] = {"extend": "com", "_server": "whois.nic.ren"}
ZZ["rentals"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["rent"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["repair"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["report"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["republican"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["restaurant"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["rest"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["review"] = {"extend": "com", "_server": "whois.nic.review"}
ZZ["reviews"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["rexroth"] = {"_server": "whois.nic.rexroth", "extend": "com"}
ZZ["richardli"] = {"_server": "whois.nic.richardli", "extend": "com"}
ZZ["rich"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["ricoh"] = {"_server": "whois.nic.ricoh", "extend": "com"}
ZZ["rightathome"] = {"_privateRegistry": True}
ZZ["ril"] = {"_server": "whois.nic.ril", "extend": "com"}
ZZ["rio"] = {"_server": "whois.gtlds.nic.br", "extend": "bom"}
ZZ["rip"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["rmit"] = {"_privateRegistry": True}
ZZ["rocks"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["rodeo"] = {"_server": "whois.nic.rodeo", "extend": "com"}
ZZ["rogers"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["room"] = {"_server": "whois.nic.room", "extend": "com"}
ZZ["rsvp"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["rugby"] = {"_server": "whois.nic.rugby", "extend": "com"}
ZZ["ruhr"] = {"_server": "whois.nic.ruhr", "extend": "com"}
ZZ["run"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ru_online"] = {"extend": "com"}
ZZ["ru.rf"] = {"extend": "ru"}
ZZ["rwe"] = {"_server": "whois.nic.rwe", "extend": "com"}
ZZ["rw"] = {"extend": "com", "_server": "whois.ricta.org.rw"}
ZZ["ryukyu"] = {"_server": "whois.nic.ryukyu", "extend": "com"}
ZZ["saarland"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["safe"] = {"_server": "whois.nic.safe", "extend": "com"}
ZZ["safety"] = {"_server": "whois.nic.safety", "extend": "com"}
ZZ["sale"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["salon"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["samsclub"] = {"_server": "whois.nic.samsclub", "extend": "com"}
ZZ["samsung"] = {"_server": "whois.nic.samsung", "extend": "com"}
ZZ["sandvikcoromant"] = {"_server": "whois.nic.sandvikcoromant", "extend": "com"}
ZZ["sandvik"] = {"_server": "whois.nic.sandvik", "extend": "com"}
ZZ["sanofi"] = {"_server": "whois.nic.sanofi", "extend": "com"}
ZZ["sapo"] = {"_privateRegistry": True}
ZZ["sap"] = {"_server": "whois.nic.sap", "extend": "com"}
ZZ["sarl"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["save"] = {"_server": "whois.nic.save", "extend": "com"}
ZZ["saxo"] = {"_server": "whois.nic.saxo", "extend": "com"}
ZZ["sb"] = {"extend": "com", "_server": "whois.nic.net.sb"}
ZZ["sbi"] = {"_server": "whois.nic.sbi", "extend": "com"}
ZZ["sbs"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["sca"] = {"_server": "whois.nic.sca", "extend": "com"}
ZZ["scb"] = {"_server": "whois.nic.scb", "extend": "com"}
ZZ["schaeffler"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["schmidt"] = {"_server": "whois.nic.schmidt", "extend": "com"}
ZZ["scholarships"] = {"_server": "whois.nic.scholarships", "extend": "com"}
ZZ["school"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["schule"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["schwarz"] = {"_server": "whois.nic.schwarz", "extend": "com"}
ZZ["science"] = {"extend": "com", "_server": "whois.nic.science"}
ZZ["scjohnson"] = {"_privateRegistry": True}
ZZ["sc.ke"] = {"extend": "ke"}
ZZ["scor"] = {"_privateRegistry": True}
ZZ["scot"] = {"_server": "whois.nic.scot", "extend": "com"}
ZZ["sc"] = {"_server": "whois2.afilias-grs.net", "extend": "com"}
ZZ["sd"] = {"extend": "com", "_server": "whois.sdnic.sd"}
ZZ["search"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["seat"] = {"_server": "whois.nic.seat", "extend": "com"}
ZZ["secure"] = {"_server": "whois.nic.secure", "extend": "com"}
ZZ["security"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["seek"] = {"_server": "whois.nic.seek", "extend": "com"}
ZZ["select"] = {"_server": "whois.nic.select", "extend": "com"}
ZZ["한국"] = {"_server": "whois.kr", "extend": "kr"}
ZZ["삼성"] = {"_server": "whois.kr", "extend": "kr"}
ZZ["닷컴"] = {"_server": "whois.nic.xn--mk1bu44c", "extend": "xn--mk1bu44c"}
ZZ["닷넷"] = {"_server": "whois.nic.xn--t60b56a", "extend": "xn--t60b56a"}
ZZ["services"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["ses"] = {"_privateRegistry": True}
ZZ["seven"] = {"_server": "whois.nic.seven", "extend": "com"}
ZZ["sew"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["sex"] = {"_server": "whois.nic.sex", "extend": "com"}
ZZ["sexy"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["sfr"] = {"_server": "whois.nic.sfr", "extend": "com"}
ZZ["shangrila"] = {"_server": "whois.nic.shangrila", "extend": "com"}
ZZ["sharp"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["shaw"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["shell"] = {"_server": "whois.nic.shell", "extend": "com"}
ZZ["shia"] = {"_server": "whois.nic.shia", "extend": "com"}
ZZ["shiksha"] = {"_server": "whois.nic.shiksha", "extend": "com"}
ZZ["shoes"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["shop"] = {"extend": "com"}
ZZ["shopping"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["shouji"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["show"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["showtime"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["shriram"] = {"_privateRegistry": True}
ZZ["silk"] = {"_server": "whois.nic.silk", "extend": "com"}
ZZ["sina"] = {"_server": "whois.nic.sina", "extend": "com"}
ZZ["singles"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["site"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["skin"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["ski"] = {"_server": "whois.nic.ski", "extend": "com"}
ZZ["sky"] = {"_server": "whois.nic.sky", "extend": "com"}
ZZ["sl"] = {"extend": "com", "_server": "whois.nic.sl"}
ZZ["sling"] = {"_server": "whois.nic.sling", "extend": "com"}
ZZ["smart"] = {"_server": "whois.nic.smart", "extend": "com"}
ZZ["smile"] = {"_server": "whois.nic.smile", "extend": "com"}
ZZ["sncf"] = {"_server": "whois.nic.sncf", "extend": "com"}
ZZ["soccer"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["social"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["so"] = {"extend": "com"}
ZZ["softbank"] = {"_server": "whois.nic.softbank", "extend": "com"}
ZZ["software"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["solar"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["solutions"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["sony"] = {"_server": "whois.nic.sony", "extend": "com"}
ZZ["soy"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["space"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["spa"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["spb.ru"] = {"extend": "com.ru", "_test": "iac.spb.ru"}
ZZ["spiegel"] = {"_privateRegistry": True}
ZZ["sport"] = {"_server": "whois.nic.sport", "extend": "com"}
ZZ["spot"] = {"_server": "whois.nic.spot", "extend": "com"}
ZZ["spreadbetting"] = {"_privateRegistry": True}
ZZ["sr"] = {"extend": "_privateReg"}
ZZ["srl"] = {"_server": "whois.afilias-srs.net", "extend": "ac", "registrant_country": r"Registrant Country:\s+(.+)"}
ZZ["srt"] = {"_privateRegistry": True}
ZZ["ss"] = {"_server": "whois.nic.ss", "extend": "com"}
ZZ["stada"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["starhub"] = {"_privateRegistry": True}
ZZ["star"] = {"_server": "whois.nic.star", "extend": "com"}
ZZ["statebank"] = {"_server": "whois.nic.statebank", "extend": "com"}
ZZ["statoil"] = {"_privateRegistry": True}
ZZ["stcgroup"] = {"_server": "whois.nic.stcgroup", "extend": "com"}
ZZ["stc"] = {"_server": "whois.nic.stc", "extend": "com"}
ZZ["stockholm"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["storage"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["store"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["stream"] = {"_server": "whois.nic.stream", "extend": "com"}
ZZ["studio"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["study"] = {"extend": "com"}
ZZ["style"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["sucks"] = {"_server": "whois.nic.sucks", "extend": "com"}
ZZ["su"] = {"extend": "ru"}
ZZ["supplies"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["supply"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["support"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["surf"] = {"_server": "whois.nic.surf", "extend": "com"}
ZZ["surgery"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["suzuki"] = {"_server": "whois.nic.suzuki", "extend": "com"}
ZZ["swatch"] = {"_server": "whois.nic.swatch", "extend": "com"}
ZZ["swiftcover"] = {"_privateRegistry": True}
ZZ["swiss"] = {"_server": "whois.nic.swiss", "extend": "com"}
ZZ["sx"] = {"extend": "com", "_server": "whois.sx"}
ZZ["sydney"] = {"_server": "whois.nic.sydney", "extend": "com"}
ZZ["sy"] = {"extend": "com", "_server": "whois.tld.sy", "_test": "tld.sy"}
ZZ["symantec"] = {"_privateRegistry": True}
ZZ["systems"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tab"] = {"_server": "whois.nic.tab", "extend": "com"}
ZZ["taipei"] = {"_server": "whois.nic.taipei", "extend": "com"}
ZZ["talk"] = {"_server": "whois.nic.talk", "extend": "com"}
ZZ["taobao"] = {"_server": "whois.nic.taobao", "extend": "com"}
ZZ["tatamotors"] = {"_server": "whois.nic.tatamotors", "extend": "com"}
ZZ["tatar"] = {"_server": "whois.nic.tatar", "extend": "com"}
ZZ["tattoo"] = {"extend": "_uniregistry", "_server": "whois.uniregistry.net"}
ZZ["tax"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["taxi"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tci"] = {"_server": "whois.nic.tci", "extend": "com"}
ZZ["tdk"] = {"_server": "whois.nic.tdk", "extend": "com"}
ZZ["td"] = {"_server": "whois.nic.td", "extend": "ac", "registrant_country": r"Registrant Country:\s+(.+)"}
ZZ["team"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tech"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["technology"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["telecity"] = {"_privateRegistry": True}
ZZ["telefonica"] = {"_privateRegistry": True}
ZZ["temasek"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["tennis"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["teva"] = {"_server": "whois.nic.teva", "extend": "com"}
ZZ["tf"] = {"extend": "re", "_server": "whois.nic.tf"}
ZZ["thd"] = {"_server": "whois.nic.thd", "extend": "com"}
ZZ["theater"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["theatre"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["th"] = {"_server": "whois.thnic.co.th", "extend": "co.th", "_test": "thnic.co.th"}
ZZ["tiaa"] = {"_server": "whois.nic.tiaa", "extend": "com"}
ZZ["tickets"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["tienda"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
# ZZ["tiffany"] = {"_server": "whois.nic.tiffany", "extend": "com"} # Revocation of the .tiffany domain (2023-07-25)
ZZ["tips"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tires"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tirol"] = {"_server": "whois.nic.tirol", "extend": "com"}
ZZ["tk"] = {"extend": "_privateReg"}
ZZ["tl"] = {"extend": "com"}
ZZ["tmall"] = {"_server": "whois.nic.tmall", "extend": "com"}
ZZ["today"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["to"] = {"extend": "_privateReg"}
ZZ["tokyo"] = {"extend": "com", "_server": "whois.nic.tokyo"}
ZZ["tools"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["top"] = {"extend": "com"}
ZZ["toray"] = {"_server": "whois.nic.toray", "extend": "com"}
ZZ["toshiba"] = {"_server": "whois.nic.toshiba", "extend": "com"}
ZZ["total"] = {"_server": "whois.nic.total", "extend": "com"}
ZZ["tours"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["town"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["toyota"] = {"_server": "whois.nic.toyota", "extend": "com"}
ZZ["toys"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tp"] = {"_privateRegistry": True}
ZZ["trade"] = {"extend": "amsterdam"}
ZZ["trading"] = {"_server": "whois.nic.trading", "extend": "com"}
ZZ["training"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
# ZZ["travelchannel"] = {"_server": "whois.nic.travelchannel", "extend": "com"} # Revocation of the .travelchannel domain (2023-06-14)
ZZ["travelersinsurance"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["travelers"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["travel"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["tr"] = {"extend": "_privateReg"}
ZZ["trust"] = {"_server": "whois.nic.trust", "extend": "com"}
ZZ["trv"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["tt"] = {"extend": "_privateReg"}
ZZ["tube"] = {"extend": "com", "_server": "whois.nic.tube"}
ZZ["tui"] = {"_server": "whois.nic.tui", "extend": "com"}
ZZ["tunes"] = {"_server": "whois.nic.tunes", "extend": "com"}
ZZ["tushu"] = {"_server": "whois.nic.tushu", "extend": "com"}
ZZ["tvs"] = {"_server": "whois.nic.tvs", "extend": "com"}
ZZ["ubank"] = {"_server": "whois.nic.ubank", "extend": "com"}
ZZ["ubs"] = {"_server": "whois.nic.ubs", "extend": "com"}
ZZ["uconnect"] = {"_privateRegistry": True}
ZZ["um"] = {"_privateRegistry": True}
ZZ["unicom"] = {"_server": "whois.nic.unicom", "extend": "com"}
ZZ["university"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["uno"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["uol"] = {"_server": "whois.gtlds.nic.br", "extend": "bom"}
ZZ["ups"] = {"_server": "whois.nic.ups", "extend": "com"}
ZZ["us"] = {"extend": "name"}
ZZ["uy"] = {"extend": "_privateReg"}  # Uruguay
ZZ["vacations"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["va"] = {"extend": "_privateReg"}  # This TLD has no whois server.
ZZ["vana"] = {"_server": "whois.nic.vana", "extend": "com"}
ZZ["vanguard"] = {"_server": "whois.nic.vanguard", "extend": "com"}
ZZ["vc"] = {"extend": "com"}
ZZ["vegas"] = {"_server": "whois.nic.vegas", "extend": "com"}
ZZ["ventures"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["verisign"] = {"_server": "whois.nic.verisign", "extend": "com"}
ZZ["vermögensberater"] = {"_server": "whois.nic.xn--vermgensberater-ctb", "extend": "xn--vermgensberater-ctb"}
ZZ["vermögensberatung"] = {"_server": "whois.nic.xn--vermgensberatung-pwb", "extend": "xn--vermgensberatung-pwb"}
ZZ["versicherung"] = {"_server": "whois.nic.versicherung", "extend": "com"}
ZZ["vet"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["vg"] = {"_server": "whois.nic.vg", "extend": "com"}
ZZ["viajes"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["video"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["vig"] = {"extend": "com", "_server": "whois.afilias-srs.net"}
ZZ["viking"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["villas"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["vin"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["vip"] = {"_server": "whois.nic.vip", "extend": "com", "updated_date": None}
ZZ["virgin"] = {"_server": "whois.nic.virgin", "extend": "com"}
ZZ["visa"] = {"_server": "whois.nic.visa", "extend": "com"}
ZZ["vision"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["vistaprint"] = {"_privateRegistry": True}
ZZ["vista"] = {"_privateRegistry": True}
ZZ["viva"] = {"_server": "whois.nic.viva", "extend": "com"}
ZZ["vlaanderen"] = {"_server": "whois.nic.vlaanderen", "extend": "com"}
ZZ["vn"] = {"extend": "_privateReg"}
ZZ["vodka"] = {"_server": "whois.nic.vodka", "extend": "com"}
ZZ["volkswagen"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["volvo"] = {"_server": "whois.nic.volvo", "extend": "com"}
ZZ["vote"] = {"_server": "whois.nic.vote", "extend": "com"}
ZZ["voting"] = {"_server": "whois.nic.voting", "extend": "com"}
ZZ["voto"] = {"_server": "whois.nic.voto", "extend": "com"}
ZZ["vig"] = {"_server": "whois.nic.vig", "extend": "com", "_test": "nic.vig"}

ZZ["voyage"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["vu"] = {"extend": "_privateReg"}  # all dates 1970 , no furter relevant info
ZZ["wales"] = {"_server": "whois.nic.wales", "extend": "com"}
ZZ["walmart"] = {"_server": "whois.nic.walmart", "extend": "com"}
ZZ["walter"] = {"_server": "whois.nic.walter", "extend": "com"}
ZZ["wang"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["wanggou"] = {"_server": "whois.nic.wanggou", "extend": "com"}
ZZ["warman"] = {"_privateRegistry": True}
ZZ["watches"] = {"_server": "whois.nic.watches", "extend": "com"}
ZZ["watch"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["webcam"] = {"extend": "com", "_server": "whois.nic.webcam"}
ZZ["weber"] = {"_server": "whois.nic.weber", "extend": "com"}
ZZ["website"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["web.ve"] = {"extend": "ve"}
ZZ["web.za"] = {"extend": "za", "_server": "web-whois.registry.net.za"}
ZZ["wedding"] = {"_server": "whois.nic.wedding", "extend": "com"}
ZZ["wed"] = {"_server": "whois.nic.wed", "extend": "com"}
ZZ["weibo"] = {"_server": "whois.nic.weibo", "extend": "com"}
ZZ["whoswho"] = {"_server": "whois.nic.whoswho", "extend": "com"}
ZZ["wien"] = {"_server": "whois.nic.wien", "extend": "com"}
ZZ["wine"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["win"] = {"extend": "com"}
ZZ["wme"] = {"_server": "whois.nic.wme", "extend": "com"}
ZZ["wolterskluwer"] = {"_server": "whois.nic.wolterskluwer", "extend": "com"}
ZZ["woodside"] = {"_server": "whois.nic.woodside", "extend": "com"}
ZZ["works"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["world"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["wow"] = {"_server": "whois.nic.wow", "extend": "com"}
ZZ["wtc"] = {"_server": "whois.nic.wtc", "extend": "com"}
ZZ["wtf"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["xerox"] = {"_server": "whois.nic.xerox", "extend": "com"}
ZZ["xfinity"] = {"_server": "whois.nic.xfinity", "extend": "com"}
ZZ["xihuan"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["xin"] = {"extend": "com", "_server": "whois.nic.xin"}
ZZ["xn--0zwm56d"] = {"_privateRegistry": True}
ZZ["xn--11b4c3d"] = {"_server": "whois.nic.xn--11b4c3d", "extend": "com"}
ZZ["xn--11b5bs3a9aj6g"] = {"_privateRegistry": True}
ZZ["xn--1qqw23a"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["xn--2scrj9c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--30rr7y"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["xn--3bst00m"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["xn--3ds443g"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["xn--3e0b707e"] = {"_server": "whois.kr", "extend": "kr"}
ZZ["xn--3hcrj9c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--3oq18vl8pn36a"] = {"_privateRegistry": True}
ZZ["xn--3pxu8k"] = {"_server": "whois.nic.xn--3pxu8k", "extend": "com"}
ZZ["xn--42c2d9a"] = {"_server": "whois.nic.xn--42c2d9a", "extend": "com"}
ZZ["xn--45br5cyl"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--45brj9c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--45q11c"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["xn--4gbrim"] = {"_server": "whois.nic.xn--4gbrim", "extend": "com"}
ZZ["xn--55qx5d"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["xn--5su34j936bgsg"] = {"_server": "whois.nic.xn--5su34j936bgsg", "extend": "com"}
ZZ["xn--5tzm5g"] = {"_server": "whois.nic.xn--5tzm5g", "extend": "com"}
ZZ["xn--6frz82g"] = {"_server": "whois.nic.xn--6frz82g", "extend": "com"}
ZZ["xn--6qq986b3xl"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["xn--80adxhks"] = {"_server": "whois.nic.xn--80adxhks", "extend": "com"}
ZZ["xn--80akhbyknj4f"] = {"_privateRegistry": True}
ZZ["xn--80aqecdr1a"] = {"_server": "whois.nic.xn--80aqecdr1a", "extend": "com"}
ZZ["xn--80asehdb"] = {"extend": "com"}
ZZ["xn--80asehdb"] = {"_server": "whois.nic.xn--80asehdb", "extend": "com"}
ZZ["xn--80aswg"] = {"_server": "whois.nic.xn--80aswg", "extend": "com"}
ZZ["xn--8y0a063a"] = {"_server": "whois.nic.xn--8y0a063a", "extend": "com"}
ZZ["xn--9dbq2a"] = {"_server": "whois.nic.xn--9dbq2a", "extend": "com"}
ZZ["xn--9et52u"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["xn--9krt00a"] = {"_server": "whois.nic.xn--9krt00a", "extend": "com"}
ZZ["xn--9t4b11yi5a"] = {"_privateRegistry": True}
ZZ["xn--b4w605ferd"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["xn--c1avg"] = {"_server": "whois.nic.xn--c1avg", "extend": "com"}
ZZ["xn--c2br7g"] = {"_server": "whois.nic.xn--c2br7g", "extend": "com"}
ZZ["xn--cckwcxetd"] = {"_server": "whois.nic.xn--cckwcxetd", "extend": "com"}
ZZ["xn--cg4bki"] = {"_server": "whois.kr", "extend": "kr"}
ZZ["xn--clchc0ea0b2g2a9gcd"] = {"_server": "whois.sgnic.sg", "extend": "sg"}
ZZ["xn--czrs0t"] = {"_server": "whois.nic.xn--czrs0t", "extend": "com"}
ZZ["xn--czru2d"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["xn--d1alf"] = {"_server": "whois.marnet.mk", "extend": "mk"}
ZZ["xn--deba0ad"] = {"_privateRegistry": True}
ZZ["xn--e1a4c"] = {"_server": "whois.eu", "extend": "eu"}
ZZ["xn--efvy88h"] = {"_server": "whois.nic.xn--efvy88h", "extend": "com"}
ZZ["xn--estv75g"] = {"_privateRegistry": True}
ZZ["xn--fhbei"] = {"_server": "whois.nic.xn--fhbei", "extend": "com"}
ZZ["xn--fiq228c5hs"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["xn--fiq64b"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["xn--fiqs8s"] = {"_server": "cwhois.cnnic.cn", "extend": "com"}
ZZ["xn--fiqz9s"] = {"_server": "cwhois.cnnic.cn", "extend": "com"}
ZZ["xn--fjq720a"] = {"_server": "whois.nic.xn--fjq720a", "extend": "com"}
ZZ["xn--flw351e"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["xn--fpcrj9c3d"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--fzys8d69uvgm"] = {"_server": "whois.nic.xn--fzys8d69uvgm", "extend": "com"}
ZZ["xn--g6w251d"] = {"_privateRegistry": True}
ZZ["xn--gecrj9c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--h2breg3eve"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--h2brj9c8c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--h2brj9c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--hgbk6aj7f53bba"] = {"_privateRegistry": True}
ZZ["xn--hlcj6aya9esc7a"] = {"_privateRegistry": True}
ZZ["xn--hxt814e"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["xn--i1b6b1a6a2e"] = {"_server": "whois.nic.xn--i1b6b1a6a2e", "extend": "com"}
ZZ["xn--io0a7i"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["xn--j1aef"] = {"_server": "whois.nic.xn--j1aef", "extend": "com"}
ZZ["xn--j6w193g"] = {"_server": "whois.hkirc.hk", "extend": "hk", "_test": "hkirc.hk"}
ZZ["xn--jlq480n2rg"] = {"_server": "whois.nic.xn--jlq480n2rg", "extend": "com"}
ZZ["xn--jlq61u9w7b"] = {"_privateRegistry": True}
ZZ["xn--jxalpdlp"] = {"_privateRegistry": True}
ZZ["xn--kcrx77d1x4a"] = {"_server": "whois.nic.xn--kcrx77d1x4a", "extend": "com"}
ZZ["xn--kgbechtv"] = {"_privateRegistry": True}
ZZ["xn--kprw13d"] = {"extend": "tw", "_test": "google.xn--kprw13d"}
ZZ["xn--kpry57d"] = {"extend": "tw", "_test": "google.xn--kpry57d"}
ZZ["xn--kpu716f"] = {"_privateRegistry": True}
ZZ["xn--kput3i"] = {"_server": "whois.nic.xn--kput3i", "extend": "com"}
ZZ["xn--mgb9awbf"] = {"_server": "whois.registry.om", "extend": "om"}
ZZ["xn--mgba7c0bbn0a"] = {"_server": "whois.nic.xn--mgba7c0bbn0a", "extend": "com"}
ZZ["xn--mgbaakc7dvf"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["xn--mgbab2bd"] = {"_server": "whois.nic.xn--mgbab2bd", "extend": "com"}
ZZ["xn--mgbah1a3hjkrd"] = {"_server": "whois.nic.mr", "extend": "mr"}
ZZ["xn--mgbb9fbpob"] = {"_privateRegistry": True}
ZZ["xn--mgbbh1a71e"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--mgbbh1a"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--mgbca7dzdo"] = {"_server": "whois.nic.xn--mgbca7dzdo", "extend": "com"}
ZZ["xn--mgbgu82a"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--mgbi4ecexp"] = {"_server": "whois.nic.xn--mgbi4ecexp", "extend": "com"}
ZZ["xn--mgbt3dhd"] = {"_server": "whois.nic.xn--mgbt3dhd", "extend": "com"}
ZZ["xn--mix891f"] = {"_server": "whois.monic.mo", "extend": "mo"}
ZZ["xn--mk1bu44c"] = {"_server": "whois.nic.xn--mk1bu44c", "extend": "com"}
ZZ["xn--mxtq1m"] = {"_server": "whois.nic.xn--mxtq1m", "extend": "com"}
ZZ["xn--ngbc5azd"] = {"_server": "whois.nic.xn--ngbc5azd", "extend": "com"}
ZZ["xn--ngbe9e0a"] = {"_server": "whois.nic.xn--ngbe9e0a", "extend": "com"}
ZZ["xn--ngbrx"] = {"_server": "whois.nic.xn--ngbrx", "extend": "com"}
ZZ["xn--nqv7fs00ema"] = {"_server": "whois.nic.xn--nqv7fs00ema", "extend": "com"}
ZZ["xn--nqv7f"] = {"_server": "whois.nic.xn--nqv7f", "extend": "com"}
ZZ["xn--o3cw4h"] = {"_server": "whois.thnic.co.th", "extend": "co.th"}
ZZ["xn--ogbpf8fl"] = {"_server": "whois.tld.sy", "extend": "sy", "_test": "tld.sy"}
ZZ["xn--p1acf"] = {"extend": "com"}
ZZ["xn--p1ai"] = {"extend": "ru"}
ZZ["xn--pbt977c"] = {"_privateRegistry": True}
ZZ["xn--pssy2u"] = {"_server": "whois.nic.xn--pssy2u", "extend": "com"}
ZZ["xn--q9jyb4c"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["xn--qcka1pmc"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["xn--qxa6a"] = {"_server": "whois.eu", "extend": "eu"}
ZZ["xn--rvc1e0am3e"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--s9brj9c"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--ses554g"] = {"_server": "whois.nic.xn--ses554g", "extend": "com"}
ZZ["xn--t60b56a"] = {"_server": "whois.nic.xn--t60b56a", "extend": "com"}
ZZ["xn--tckwe"] = {"_server": "whois.nic.xn--tckwe", "extend": "com"}
ZZ["xn--tiq49xqyj"] = {"_server": "whois.nic.xn--tiq49xqyj", "extend": "com"}
ZZ["xn--unup4y"] = {"_server": "whois.nic.xn--unup4y", "extend": "com"}
ZZ["xn--vermgensberater-ctb"] = {"_server": "whois.nic.xn--vermgensberater-ctb", "extend": "com"}
ZZ["xn--vermgensberatung-pwb"] = {"_server": "whois.nic.xn--vermgensberatung-pwb", "extend": "com"}
ZZ["xn--vhquv"] = {"_server": "whois.nic.xn--vhquv", "extend": "com"}
ZZ["xn--vuq861b"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["xn--w4r85el8fhu5dnra"] = {"_server": "whois.nic.xn--w4r85el8fhu5dnra", "extend": "com"}
ZZ["xn--w4rs40l"] = {"_server": "whois.nic.xn--w4rs40l", "extend": "com"}
ZZ["xn--wgbl6a"] = {"_server": "whois.registry.qa", "extend": "qa", "_test": "registry.qa"}
ZZ["xn--xhq521b"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["xn--xkc2dl3a5ee0h"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["xn--yfro4i67o"] = {"_server": "whois.sgnic.sg", "extend": "sg"}
ZZ["xn--zckzah"] = {"_privateRegistry": True}
ZZ["xperia"] = {"_privateRegistry": True}
ZZ["xxx"] = {"_server": "whois.nic.xxx", "extend": "com"}
ZZ["xyz"] = {"extend": "_centralnic", "_server": "whois.nic.xyz"}
ZZ["yachts"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["yamaxun"] = {"_server": "whois.nic.yamaxun", "extend": "com"}
ZZ["ye"] = {"extend": "com", "_server": "whois.y.net.ye", "_test": "net.ye"}
ZZ["yodobashi"] = {"_server": "whois.nic.gmo", "extend": "com"}
ZZ["yoga"] = {"_server": "whois.nic.yoga", "extend": "com"}
ZZ["yokohama"] = {"_server": "whois.nic.yokohama", "extend": "com"}
ZZ["you"] = {"_server": "whois.nic.you", "extend": "com"}
ZZ["youtube"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["yt"] = {"extend": "re", "_server": "whois.nic.yt"}
ZZ["yun"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["za"] = {"extend": "com"}
ZZ["zappos"] = {"_server": "whois.nic.zappos", "extend": "com", "_test": "nic.zappos"}
ZZ["zara"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["zip"] = {"extend": "com", "_server": "whois.nic.zip", "_test": "nic.zip"}
ZZ["zippo"] = {"_privateRegistry": True}
ZZ["zm"] = {"extend": "com"}
ZZ["zone"] = {"extend": "_donuts", "_server": "whois.donuts.co"}
ZZ["zuerich"] = {"extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["zw"] = {"extend": "_privateReg"}  # Zimbabwe
ZZ["δοκιμή"] = {"_privateRegistry": True}
ZZ["ευ"] = {"_server": "whois.eu", "extend": "eu"}
ZZ["ею"] = {"_server": "whois.eu", "extend": "eu"}
ZZ["испытание"] = {"_privateRegistry": True}
ZZ["католик"] = {"_server": "whois.nic.xn--80aqecdr1a", "extend": "xn--80aqecdr1a"}
ZZ["ком"] = {"_server": "whois.nic.xn--j1aef", "extend": "xn--j1aef"}
ZZ["мкд"] = {"_server": "whois.marnet.mk", "extend": "mk"}
ZZ["москва"] = {"_server": "whois.nic.xn--80adxhks", "extend": "xn--80adxhks"}
ZZ["онлайн"] = {"extend": "com"}
ZZ["орг"] = {"_server": "whois.nic.xn--c1avg", "extend": "xn--c1avg"}
ZZ["рус"] = {"extend": "com"}
ZZ["РУС"] = {"extend": "com"}
ZZ["рф"] = {"extend": "ru"}
ZZ["сайт"] = {"_server": "whois.nic.xn--80aswg", "extend": "xn--80aswg"}
ZZ["טעסט"] = {"_privateRegistry": True}
ZZ["קום"] = {"_server": "whois.nic.xn--9dbq2a", "extend": "xn--9dbq2a"}
ZZ["آزمایشی"] = {"_privateRegistry": True}
ZZ["إختبار"] = {"_privateRegistry": True}
ZZ["ابوظبي"] = {"_server": "whois.nic.xn--mgbca7dzdo", "extend": "xn--mgbca7dzdo"}
ZZ["اتصالات"] = {"_server": "whois.centralnic.com", "extend": "_centralnic", "_server": "whois.centralnic.com"}
ZZ["العليان"] = {"_server": "whois.nic.xn--mgba7c0bbn0a", "extend": "xn--mgba7c0bbn0a"}
ZZ["بارت"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["بازار"] = {"_server": "whois.nic.xn--mgbab2bd", "extend": "xn--mgbab2bd"}
ZZ["بھارت"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["بيتك"] = {"_server": "whois.nic.xn--ngbe9e0a", "extend": "xn--ngbe9e0a"}
ZZ["ڀارت"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["سورية"] = {"_server": "whois.tld.sy", "extend": "sy"}
ZZ["شبكة"] = {"_server": "whois.nic.xn--ngbc5azd", "extend": "xn--ngbc5azd"}
ZZ["عرب"] = {"_server": "whois.nic.xn--ngbrx", "extend": "xn--ngbrx"}
ZZ["عمان"] = {"_server": "whois.registry.om", "extend": "om"}
ZZ["قطر"] = {"_server": "whois.registry.qa", "extend": "qa"}
ZZ["كاثوليك"] = {"_server": "whois.nic.xn--mgbi4ecexp", "extend": "xn--mgbi4ecexp"}
ZZ["كوم"] = {"_server": "whois.nic.xn--fhbei", "extend": "xn--fhbei"}
ZZ["موبايلي"] = {"_privateRegistry": True}
ZZ["موريتانيا"] = {"_server": "whois.nic.mr", "extend": "mr"}
ZZ["موقع"] = {"_server": "whois.nic.xn--4gbrim", "extend": "xn--4gbrim"}  #
ZZ["همراه"] = {"_server": "whois.nic.xn--mgbt3dhd", "extend": "xn--mgbt3dhd"}
ZZ["नट"] = {"_server": "whois.nic.xn--c2br7g", "extend": "xn--c2br7g"}
ZZ["परकष"] = {"_privateRegistry": True}
ZZ["भरत"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["भरत"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["भरतम"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["सगठन"] = {"_server": "whois.nic.xn--i1b6b1a6a2e", "extend": "xn--i1b6b1a6a2e"}
ZZ["ভরত"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["ভৰত"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["ਭਰਤ"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["ભરત"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["ଭରତ"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["இநதய"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["சஙகபபர"] = {"_server": "whois.sgnic.sg", "extend": "sg"}
ZZ["பரடச"] = {"_privateRegistry": True}
ZZ["భరత"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["ಭರತ"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["ഭരത"] = {"_server": "whois.registry.in", "extend": "com"}
ZZ["คอม"] = {"_server": "whois.nic.xn--42c2d9a", "extend": "xn--42c2d9a"}  #
ZZ["ไทย"] = {"_server": "whois.thnic.co.th", "extend": "co.th"}
ZZ["アマゾン"] = {"_server": "whois.nic.xn--cckwcxetd", "extend": "xn--cckwcxetd"}
ZZ["グーグル"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["コム"] = {"_server": "whois.nic.xn--tckwe", "extend": "xn--tckwe"}
ZZ["テスト"] = {"_privateRegistry": True}
ZZ["みんな"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["中信"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["中国"] = {"_server": "cwhois.cnnic.cn", "extend": "xn--fiqs8s"}
ZZ["中國"] = {"_server": "cwhois.cnnic.cn", "extend": "xn--fiqs8s"}
ZZ["中文网"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["亚马逊"] = {"_server": "whois.nic.xn--jlq480n2rg", "extend": "xn--jlq480n2rg"}
ZZ["企业"] = {"_server": "whois.nic.xn--vhquv", "extend": "xn--vhquv"}
ZZ["佛山"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["信息"] = {"_server": "whois.teleinfo.cn", "extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["八卦"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["公司"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["台湾"] = {"_server": "whois.twnic.net.tw", "extend": "tw", "_test": "google.台湾"}
ZZ["台灣"] = {"_server": "whois.twnic.net.tw", "extend": "tw", "_test": "google.台灣"}
ZZ["商城"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["商店"] = {"_server": "whois.nic.xn--czrs0t", "extend": "xn--czrs0t"}
ZZ["嘉里"] = {"_server": "whois.nic.xn--w4rs40l", "extend": "xn--w4rs40l"}
ZZ["嘉里大酒店"] = {"_server": "whois.nic.xn--w4r85el8fhu5dnra", "extend": "xn--w4r85el8fhu5dnra"}
ZZ["在线"] = {"extend": "_teleinfo", "_server": "whois.teleinfo.cn"}
ZZ["大众汽车"] = {"_privateRegistry": True}
ZZ["大拿"] = {"_server": "whois.nic.xn--pssy2u", "extend": "xn--pssy2u"}
ZZ["天主教"] = {"_server": "whois.nic.xn--tiq49xqyj", "extend": "xn--tiq49xqyj"}
ZZ["娱乐"] = {"_server": "whois.nic.xn--fjq720a", "extend": "xn--fjq720a"}
ZZ["工行"] = {"_privateRegistry": True}
ZZ["广东"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["微博"] = {"_server": "whois.nic.xn--9krt00a", "extend": "xn--9krt00a"}
ZZ["慈善"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["我爱你"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["手机"] = {"_server": "whois.nic.xn--kput3i", "extend": "xn--kput3i"}
ZZ["手表"] = {"_privateRegistry": True}
ZZ["政府"] = {"_server": "whois.nic.xn--mxtq1m", "extend": "xn--mxtq1m"}
ZZ["新加坡"] = {"_server": "whois.sgnic.sg", "extend": "sg"}
ZZ["新闻"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["时尚"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["机构"] = {"_server": "whois.nic.xn--nqv7f", "extend": "xn--nqv7f"}
ZZ["测试"] = {"_privateRegistry": True}
ZZ["淡马锡"] = {"_server": "whois.afilias-srs.net", "extend": "com"}
ZZ["測試"] = {"_privateRegistry": True}
ZZ["游戏"] = {"_server": "whois.nic.xn--unup4y", "extend": "xn--unup4y"}
ZZ["澳門"] = {"_server": "whois.monic.mo", "extend": "mo"}
ZZ["点看"] = {"_server": "whois.nic.xn--3pxu8k", "extend": "xn--3pxu8k"}
ZZ["珠宝"] = {"_privateRegistry": True}
ZZ["移动"] = {"_server": "whois.nic.xn--6frz82g", "extend": "xn--6frz82g"}
ZZ["组织机构"] = {"_server": "whois.nic.xn--nqv7fs00ema", "extend": "xn--nqv7fs00ema"}
ZZ["网址"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["网店"] = {"extend": "_gtldKnet", "_server": "whois.gtld.knet.cn"}
ZZ["网站"] = {"_server": "whois.nic.xn--5tzm5g", "extend": "xn--5tzm5g"}
ZZ["网络"] = {"_server": "whois.ngtld.cn", "extend": "com"}
ZZ["联通"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["诺基亚"] = {"_privateRegistry": True}
ZZ["cy"] = {"_privateRegistry": True}
ZZ["gh"] = {"_privateRegistry": True}
ZZ["pa"] = {"_privateRegistry": True}
ZZ["sv"] = {"_privateRegistry": True}

ZZ["谷歌"] = {"_server": "whois.nic.google", "extend": "com"}
ZZ["集团"] = {"_server": "whois.gtld.knet.cn", "extend": "com"}
ZZ["電訊盈科"] = {"_server": "whois.nic.xn--fzys8d69uvgm", "extend": "xn--fzys8d69uvgm"}
ZZ["飞利浦"] = {"_server": "whois.nic.xn--kcrx77d1x4a", "extend": "xn--kcrx77d1x4a"}
ZZ["香格里拉"] = {"_server": "whois.nic.xn--5su34j936bgsg", "extend": "xn--5su34j936bgsg"}
ZZ["香港"] = {"_server": "whois.hkirc.hk", "extend": "hk"}
