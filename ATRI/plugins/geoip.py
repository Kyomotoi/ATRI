from geoip2.webservice import AsyncClient

from nonebot.params import ArgStr

from ATRI import conf, driver
from ATRI.log import log
from ATRI.service import Service
from ATRI.message import MessageBuilder


LANG = "zh-CN"


geoip = Service("IP查询").document("通过 geoip 查询 IP 信息")


query_geoip = geoip.on_command("ip查询", "查询IP的地理位置", aliases={"IP查询", "查询IP"})


@query_geoip.got("ip_address", prompt="地址是?(支持ipv4/ipv6)")
async def _(ip_address: str = ArgStr()):
    await query_geoip.send("正在查询...请稍候")

    try:
        async with AsyncClient(
            conf.GeoIP.account_id, conf.GeoIP.license_key, host="geolite.info"
        ) as client:
            resp = await client.city(ip_address)

            country = resp.country.names[LANG]
            city = resp.city.names[LANG]
            org = resp.traits.autonomous_system_organization
            network = resp.traits.network
            subd = str()
            if subs := resp.subdivisions:
                subd = subs[0].names[LANG]

            result = (
                MessageBuilder(f"IP: {ip_address}")
                .text(f"{country}{subd}{city}")
                .text(f"运营商: {org}")
                .text(f"网段: {network}")
            )
    except Exception:
        result = "查询失败..."

    await query_geoip.finish(result)


def _check_need():
    if not conf.GeoIP.account_id or not conf.GeoIP.license_key:
        log.warning("插件 IP查询 所需的设置未配置, 将被全局禁用, 填写后请手动启用")


driver().on_startup(_check_need)
