#!/usr/bin/env python3
"""Generate a developer-oriented English Broker REST API specification."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openapi" / "b" / "openapi.json"
OUTPUT = ROOT / "openapi" / "b" / "openapi.en.json"
CJK_RE = re.compile(r"[\u3400-\u9fff]")

_PAIRS = r"""
保存风控配置|||Update risk configuration
备注|||Optional note
币种|||Currency
操作是否成功|||Whether the operation succeeded
操作原因|||Reason for the operation
策略版本|||Policy version
查询仓位|||List positions
查询成交记录|||List trades
查询当前委托|||List open orders
查询风控策略|||List risk policies
查询风控配置|||Get risk configuration
查询风险敞口|||List risk exposures
查询划转列表|||List transfers
查询划转详情|||Get transfer
查询汇总报表|||Get summary report
查询每日汇总|||List daily summaries
查询趋势报表|||List report trends
查询券商设置|||Get broker settings
查询事件|||List events
查询事件下的市场|||List event markets
查询仪表盘|||Get dashboard
查询用户 API Key|||List user API keys
查询用户列表|||List users
查询资产|||List assets
成交 ID|||Trade ID
成交价格|||Execution price
成交角色|||Execution role
成交类型|||Trade type
成交时间（Unix 毫秒）|||Execution time as a Unix-millisecond timestamp
成交时间范围起点（Unix 毫秒，包含）|||Start of the execution-time range in Unix milliseconds, inclusive
成交时间范围终点（Unix 毫秒，不包含）|||End of the execution-time range in Unix milliseconds, exclusive
成交数量|||Executed quantity
成交总额|||Total trading volume
成交总额环比变化百分比；无上期数据时为空|||Percentage change in trading volume from the previous period; null when no previous-period data exists
出金总额|||Total withdrawals
出金总额环比变化百分比；无上期数据时为空|||Percentage change in withdrawals from the previous period; null when no previous-period data exists
创建划转|||Create transfer
创建时间（Unix 毫秒）|||Creation time as a Unix-millisecond timestamp
创建时间范围起点（Unix 毫秒，包含）|||Start of the creation-time range in Unix milliseconds, inclusive
创建时间范围终点（Unix 毫秒，不包含）|||End of the creation-time range in Unix milliseconds, exclusive
创建特殊账户|||Create special account
创建用户 API Key|||Create user API key
错误原因|||Error message
待平仓的结果 Token ID|||Outcome token ID to close
单个事件最大最坏情况赔付额|||Maximum worst-case payout for one event
当前风险敞口|||Current risk exposure
当前统计周期结束时间（Unix 毫秒）|||End of the current reporting period as a Unix-millisecond timestamp
当前统计周期开始时间（Unix 毫秒）|||Start of the current reporting period as a Unix-millisecond timestamp
当前页划转记录|||Transfers on the current page
当前页用户列表|||Users on the current page
当前周期汇总指标|||Metrics for the current period
当前周期相对上一周期的变化百分比|||Percentage change from the previous period
订单 ID|||Order ID
订单状态|||Order status
返回数量，最大 100|||Number of records to return, up to 100
风控策略 ID|||Risk policy ID
风控策略列表|||Risk policies
风控策略总数|||Total number of risk policies
风控配置|||Risk configuration
风险敞口上限|||Risk exposure limit
风险敞口状态|||Risk exposure status
风险敞口总数|||Total number of risk exposures
风险状态|||Risk status
符合条件的记录总数|||Total number of matching records
符合条件的用户总数|||Total number of matching users
更新券商设置|||Update broker settings
更新时间（Unix 毫秒）|||Update time as a Unix-millisecond timestamp
更新市场|||Update market
更新事件|||Update event
更新用户|||Update user
规则类型|||Rule type
规则目标 ID|||Rule target ID
规则作用域|||Rule scope
划转方向：1 入金，2 出金|||Transfer direction: `1` for deposit, `2` for withdrawal
划转金额|||Transfer amount
划转金额，必须大于 0|||Transfer amount; must be greater than zero
划转信息|||Transfer request
划转状态|||Transfer state
汇总日期范围起点（Unix 毫秒，包含）|||Start of the summary-date range in Unix milliseconds, inclusive
汇总日期范围终点（Unix 毫秒，不包含）|||End of the summary-date range in Unix milliseconds, exclusive
活跃市场数|||Number of active markets
活跃事件数|||Number of active events
活跃用户数|||Number of active users
活跃用户数环比变化百分比；无上期数据时为空|||Percentage change in active users from the previous period; null when no previous-period data exists
结果 Token 余额列表|||Outcome token balances
结果 Token ID|||Outcome token ID
结果名称|||Outcome name
结束成交记录 ID（不包含）|||Ending trade record ID, exclusive
结束时间（Unix 毫秒，不包含）|||End time in Unix milliseconds, exclusive
结束时间（Unix 毫秒）|||End time in Unix milliseconds
开始时间（Unix 毫秒，包含）|||Start time in Unix milliseconds, inclusive
可用 USDC 余额|||Available USDC balance
可用仓位数量|||Available position quantity
可用余额|||Available balance
来源数据更新时间（Unix 毫秒）|||Source data update time as a Unix-millisecond timestamp
买卖方向|||Side: buy or sell
每页数量，最大 100|||Items per page, up to 100
模糊搜索关键词|||Fuzzy-search term
平仓|||Close position
平仓数量|||Quantity to close
平仓委托价格|||Close-order price
平仓委托结果|||Close-order result
平仓信息|||Position-close request
平均成本价|||Average cost price
平均持仓价格|||Average position price
平台划转订单 ID|||Platform transfer order ID
平台用户 UID|||Platform user UID
起始成交记录 ID（不包含）|||Starting trade record ID, exclusive
请求时间戳，支持秒或毫秒。|||Request timestamp in Unix seconds or milliseconds.
取消委托|||Cancel order
券商 App ID，用于标识调用方身份。|||Broker App ID that identifies the caller.
券商 ID|||Broker ID
券商侧唯一交易流水号|||Unique broker transaction ID
券商侧用户 ID|||Broker-side user ID
券商侧用户 ID 或平台 UID|||Broker-side user ID or platform UID
券商侧用户 ID；不传表示当前券商全部用户|||Broker-side user ID; omit to query all users owned by the current broker
券商接口-风控|||Risk management
券商接口-后管|||Broker management
券商接口-划转|||Transfers
券商接口-事件|||Events
券商接口-用户|||Users
券商名称|||Broker name
券商配置更新时间（Unix 毫秒）|||Broker configuration update time as a Unix-millisecond timestamp
券商全局风控策略|||Broker-wide risk policy
券商全局最大最坏情况赔付额|||Maximum broker-wide worst-case payout
券商设置|||Broker settings
券商用户登录令牌|||Broker user login token
券商用户总数|||Total number of broker users
券商域名|||Broker domain
券商状态|||Broker status
入金总额|||Total deposits
入金总额环比变化百分比；无上期数据时为空|||Percentage change in deposits from the previous period; null when no previous-period data exists
删除用户 API Key|||Delete user API key
上限使用率|||Exposure-limit utilization percentage
上一周期汇总指标|||Metrics for the previous period
生产环境|||Production environment
剩余可用额度|||Remaining exposure capacity
剩余数量|||Remaining quantity
使用 HMAC-SHA256 生成并经过 Base64 编码的请求签名。|||Base64-encoded HMAC-SHA256 request signature.
市场 ID|||Market ID
市场配置|||Market configuration
市场数量|||Number of markets
事件 ID|||Event ID
事件标识|||Event slug
事件标识；设置事件级配置时必填|||Event slug; required when configuring event-level risk controls
事件标识；为空时仅查询券商全局配置|||Event slug; omit to return only broker-wide configuration
事件标题|||Event title
事件分类|||Event category
事件风险敞口列表|||Event risk exposures
事件级风控策略|||Event-level risk policy
事件结束时间（Unix 毫秒）|||Event end time as a Unix-millisecond timestamp
事件开始时间（Unix 毫秒）|||Event start time as a Unix-millisecond timestamp
事件列表|||Events
事件配置|||Event configuration
事件数据来源|||Event data source
事件状态|||Event status
事件总数|||Total number of events
是否启用策略|||Whether the policy is enabled
是否启用券商全局风控|||Whether broker-wide risk controls are enabled
是否启用市场|||Whether the market is enabled
是否启用事件|||Whether the event is enabled
是否启用事件级风控|||Whether event-level risk controls are enabled
是否为隐含成交|||Whether the trade is implied
是否已为券商启用|||Whether the resource is enabled for the broker
锁定 USDC 余额|||Locked USDC balance
锁定仓位数量|||Locked position quantity
锁定余额|||Locked balance
特殊账户类型|||Special account type
特殊账户信息|||Special account request
提交位置|||Commit position
条件 ID|||Condition ID
统计周期|||Reporting period
唯一成交记录 ID，用于 from/to 流式分页|||Unique trade record ID used by `from`/`to` stream pagination
委托方向|||Order side
委托价格|||Order price
委托数量|||Order quantity
未实现盈亏|||Unrealized PnL
未实现盈亏比例|||Unrealized PnL percentage
下单是否成功|||Whether order placement succeeded
新的用户备注|||Updated user description
新的用户名称|||Updated user name
新订单 ID|||New order ID
新增用户数|||Number of new users
新增用户数环比变化百分比；无上期数据时为空|||Percentage change in new users from the previous period; null when no previous-period data exists
页码|||Page number
页码，从 1 开始|||Page number, starting from 1
已成交数量|||Filled quantity
已实现盈亏|||Realized PnL
用户 Token 同步信息|||User token synchronization request
用户备注|||User description
用户创建时间（Unix 毫秒）|||User creation time as a Unix-millisecond timestamp
用户登出|||Delete user tokens
用户登录|||Synchronize user token
用户更新时间（Unix 毫秒）|||User update time as a Unix-millisecond timestamp
用户类型|||User type
用户名称|||User name
用户信息|||User profile update
用户邮箱|||User email address
用户账户 ID|||User account ID
预留；当前版本不自动撤单|||Reserved; the current version does not cancel open orders automatically
原因码|||Reason code
原因说明|||Reason
执行结果说明|||Result message
状态原因码|||Status reason code
最近登录时间（Unix 毫秒），未登录时为空|||Last login time as a Unix-millisecond timestamp; null if the user has never signed in
最近更新时间（Unix 毫秒）|||Most recent update time as a Unix-millisecond timestamp
API Key 配置|||API key configuration
Maker 订单 ID|||Maker order ID
Maker 价格|||Maker price
Maker 买卖方向|||Maker side
Maker 账户 ID|||Maker account ID
Taker 订单 ID|||Taker order ID
Taker 价格|||Taker price
Taker 买卖方向|||Taker side
Taker 账户 ID|||Taker account ID
Unix 毫秒|||Unix time in milliseconds
USDC 余额|||USDC balance
Webhook 地址|||Webhook URL
"""


def translation_map() -> dict[str, str]:
    translations: dict[str, str] = {}
    for raw_line in _PAIRS.strip().splitlines():
        source, separator, target = raw_line.partition("|||")
        if not separator:
            raise RuntimeError(f"invalid translation entry: {raw_line}")
        if source in translations:
            raise RuntimeError(f"duplicate translation entry: {source}")
        translations[source] = target
    return translations


def translate(value, translations: dict[str, str], missing: set[str]):
    if isinstance(value, dict):
        return {key: translate(item, translations, missing) for key, item in value.items()}
    if isinstance(value, list):
        return [translate(item, translations, missing) for item in value]
    if isinstance(value, str) and CJK_RE.search(value):
        translated = translations.get(value)
        if translated is None:
            missing.add(value)
            return value
        return translated
    return value


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    missing: set[str] = set()
    translated = translate(source, translation_map(), missing)
    if missing:
        details = "\n".join(f"- {value}" for value in sorted(missing))
        raise RuntimeError(f"missing English OpenAPI translations:\n{details}")

    encoded = json.dumps(translated, ensure_ascii=False, indent=2) + "\n"
    if CJK_RE.search(encoded):
        raise RuntimeError("generated English OpenAPI still contains Chinese text")
    OUTPUT.write_text(encoded, encoding="utf-8")
    print(f"generated {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
