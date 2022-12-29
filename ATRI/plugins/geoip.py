from nonebot.params import ArgStr
import geoip2.webservice
from ATRI.service import Service
from ATRI import conf


geoip = Service("GEOIP查询").document("search ip in MaxMind GEOIP databases")

query_geoip = geoip.on_command("ip查询", "查询IP的地理位置", aliases={"IP查询", "查询IP"})

LANG = "zh-CN"


@query_geoip.got("ip_address", prompt="地址是?(支持ipv4/ipv6)")
async def _(ip_address: str = ArgStr()):
    with geoip2.webservice.Client(
        conf.GeoIP.account_id, conf.GeoIP.license_key, host="geolite.info"
    ) as client:
        await query_geoip.send("正在查询...请稍候")
        response = client.city(ip_address)
        country = response.country.names[LANG]
        city = response.city.names[LANG]
        org = response.traits.autonomous_system_organization
        network = str(response.traits.network)
        subdivision = ""
        if subs := response.subdivisions:
            subdivision = subs[0].names[LANG]
        await query_geoip.finish(
            f"IP: {ip_address}\n"
            f"{country}{subdivision}{city}\n"
            f"运营商{org}\n"
            f"网段{network}"
        )