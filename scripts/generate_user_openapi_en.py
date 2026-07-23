#!/usr/bin/env python3
"""Generate the developer-oriented English Trading REST API specification."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openapi" / "c" / "openapi.json"
OUTPUT = ROOT / "openapi" / "c" / "openapi.en.json"
CJK_RE = re.compile(r"[\u3400-\u9fff]")

_PAIRS = r"""
`/v1/public` 提供公开事件与行情数据；`/v1/private` 提供交易和账户接口，支持用户 Token 或 API Key 鉴权。|||`/v1/public` exposes public event and market data. `/v1/private` provides trading and account operations authenticated with a user token or API key.
按 ID 查询标签|||Get tag by ID
按标签、关闭状态和排序条件分页查询事件，返回当前页事件和筛选后的总数。若按 slug 查询，请使用 GET /v1/public/events/slug/{slug}。|||List events by tag, closed state, and sort order. The response includes the current page and the filtered total. To look up an event by slug, use `GET /v1/public/events/slug/{slug}`.
按标识查询标签|||Get tag by slug
按标识查询事件|||Get event by slug
按固定时间窗口查询指定结果 Token 的价格点。时间戳为 Unix 毫秒。|||Return price points for an outcome token over a fixed time window. Timestamps use Unix milliseconds.
按事件、状态和排序条件分页查询当前券商可见的市场，返回当前页市场和筛选后的总数。|||List markets visible to the current broker by event, status, and sort order. The response includes the current page and the filtered total.
按事件标题、描述、标识或代码进行不区分大小写的模糊搜索。|||Run a case-insensitive fuzzy search across event titles, descriptions, slugs, and codes.
按事件或市场筛选最近成交；eventId 与 marketId 必须且只能传一个。|||List recent trades for an event or market. Provide exactly one of `eventId` and `marketId`.
按平均成交价计算的持仓成本|||Position cost at the average execution price
按当前价格计算的持仓价值|||Position value at the current price
本次成交实现盈亏，十进制字符串|||Realized PnL for this trade, as a decimal string
本次返回数量|||Number of records returned
标签 ID|||Tag ID
标签 ID 无效|||Invalid tag ID
标签 slug|||Tag slug
标签 slug 无效|||Invalid tag slug
标签 slug，例如 sports|||Tag slug, for example `sports`
标签 slug；为空时不按标签筛选|||Tag slug. Omit to disable tag filtering.
标签不存在|||Tag not found
标签查询失败|||Failed to query tags
标签列表|||Tag list
标签显示名称|||Tag display name
标签详情|||Tag details
补充说明|||Additional notes
参与 HMAC 签名的毫秒时间戳。|||Unix timestamp in milliseconds included in the HMAC signature.
测试环境|||Test environment
查询标签列表|||List tags
查询持仓|||List positions
查询当前登录账户的成交记录。eventId/event 为同义参数，优先使用 eventId。|||List trades for the authenticated account. `eventId` and `event` are aliases; prefer `eventId`.
查询当前登录账户的成交记录，结果按时间和成交 ID 倒序返回。eventId/event 为同义参数，优先使用 eventId。|||List trades for the authenticated account, ordered by time and trade ID descending. `eventId` and `event` are aliases; prefer `eventId`.
查询当前登录账户的持仓，并计算当前价值和未实现盈亏。eventId/event 为同义参数，优先使用 eventId。|||List positions for the authenticated account, including current value and unrealized PnL. `eventId` and `event` are aliases; prefer `eventId`.
查询当前登录账户的持仓，并计算当前价值和未实现盈亏。可用 eventId 按事件过滤。|||List positions for the authenticated account, including current value and unrealized PnL. Use `eventId` to filter by event.
查询当前登录账户的历史委托。afterCursor 是上一页最后一条订单的 ID，仅用于继续向后翻页。|||List historical orders for the authenticated account. Set `afterCursor` to the last order ID from the previous page to continue forward.
查询当前登录账户的历史委托，结果按时间和订单 ID 倒序返回。|||List historical orders for the authenticated account, ordered by time and order ID descending.
查询当前登录账户的未完成委托。|||List open orders for the authenticated account.
查询当前登录账户下的指定委托。|||Get an order owned by the authenticated account.
查询当前委托|||List open orders
查询订单簿|||Get order book
查询公开成交|||List public trades
查询价格历史|||Get price history
查询历史委托|||List order history
查询买卖价差|||Get bid-ask spread
查询市场列表|||List markets
查询市场行情|||Get market ticker
查询委托详情|||Get order details
查询账户成交|||List account trades
查询账户汇总|||Get account summary
查询中间价|||Get midpoint price
查询市场价格|||Get market price
撤单处理状态|||Cancellation processing status
撤单结果|||Cancellation result
成交 ID|||Trade ID
成交后的平均成本价；无数据时为空|||Average cost after the trade. Empty when unavailable.
成交记录|||Trade
成交记录查询失败|||Failed to query trades
成交价|||Execution price
成交价，十进制字符串|||Execution price as a decimal string
成交类型；默认 MATCH|||Trade type. Defaults to `MATCH`.
成交时间戳（Unix 毫秒）|||Trade timestamp in Unix milliseconds
成交数量|||Executed quantity
成交数量，十进制字符串|||Executed quantity as a decimal string
本次成交实现盈亏|||Realized PnL for this trade
持仓记录|||Position
持仓列表|||Position list
持仓平均成交价|||Average execution price of the position
持仓总数量|||Total position quantity
初始成交价值|||Initial execution value
处理状态|||Processing status
创建时间|||Created at
创建时间（Unix 毫秒）|||Creation time in Unix milliseconds
创建委托|||Create order
撮合角色：MAKER 或 TAKER|||Matching role: `MAKER` or `TAKER`
待创建委托，1 至 50 项|||Orders to create, from 1 to 50 items
待取消的订单列表|||Orders to cancel
待取消订单，1 至 100 项|||Orders to cancel, from 1 to 100 items
当前估值|||Current valuation
当前价格|||Current price
当前市场价格|||Current market price
当前委托|||Open order
当前委托列表|||Open-order list
当前页标签|||Tags on the current page
当前页市场列表；与 events.markets 使用同一字段契约|||Markets on the current page. Uses the same field contract as `events.markets`.
当前页事件|||Events on the current page
到期时间，Unix 秒或毫秒；传 0 表示未指定|||Expiration time in Unix seconds or milliseconds. Use `0` when unspecified.
到期时间（Unix 毫秒字符串）；0 表示无指定到期|||Expiration time as a Unix-millisecond string. `0` means no expiration.
订单 ID|||Order ID
订单 ID 或请求参数无效|||Invalid order ID or request parameters
订单 ID 无效|||Invalid order ID
订单 ID，十进制正整数|||Order ID as a positive decimal integer
订单簿快照|||Order-book snapshot
订单受理状态|||Order acceptance status
订单状态|||Order status
返回当前登录账户的 USDC 可用/锁定余额及各结果 Token 余额。|||Return available and locked USDC balances plus balances for each outcome token owned by the authenticated account.
返回数量，默认 20，最大 100|||Number of records to return. Defaults to 20; maximum 100.
返回指定 slug 的标签。|||Return the tag identified by `slug`.
返回指定 slug 的事件及其市场信息。|||Return the event identified by `slug`, including its markets.
返回指定结果 Token 的买卖盘快照；缓存未命中时触发 orderbook rebroadcast 并等待本地缓存更新，超时仍无数据时返回结构完整的空订单簿。|||Return the bid and ask snapshot for an outcome token. On a cache miss, the service requests an order-book rebroadcast and waits for the local cache. If the wait times out, it returns a structurally valid empty order book.
返回指定结果 Token 的市场价格。|||Return the market price for an outcome token.
返回指定结果 Token 的最优买价与最优卖价之差。|||Return the difference between the best ask and best bid for an outcome token.
返回指定结果 Token 的最优买价与最优卖价中间值。|||Return the midpoint between the best bid and best ask for an outcome token.
返回指定字符串 ID 的标签。|||Return the tag identified by its string ID.
方向：BUY 或 SELL|||Side: `BUY` or `SELL`
费率（基点）|||Fee rate in basis points
分页查询活动标签。|||List active tags with pagination.
分页查询事件|||List events
分组展示标题|||Group display title
该游标分页接口已废弃并固定返回 HTTP 410；请改用 GET /v1/public/events。|||This cursor-based operation is deprecated and always returns HTTP `410`. Use `GET /v1/public/events` instead.
各订单处理结果|||Per-order processing results
各结果 Token 行情|||Market data for each outcome token
各结果 Token 余额|||Balances for each outcome token
各结果 Token 的余额|||Balances for each outcome token
根据结果 Token 定位所属市场，返回市场级行情和市场内各结果 Token 的最优买卖价、最新价及更新时间。|||Resolve the market from an outcome token and return market-level data plus the best bid, best ask, latest price, and update time for every outcome token in that market.
更新时间|||Updated at
更新时间（Unix 毫秒）|||Update time in Unix milliseconds
公开成交|||Public trade
公开成交列表|||Public-trade list
挂单数量|||Open-order quantity
关联订单 ID|||Related order ID
价差数据不存在|||Spread data not found
价格|||Price
价格不存在|||Price not found
价格点|||Price point
价格精度类型|||Price precision type
最小价格步长，十进制字符串；创建委托时价格必须是其整数倍|||Minimum tick size as a decimal string. Order prices must be an integer multiple of this value.
价格历史|||Price history
价格历史不存在|||Price history not found
交易集群不可用|||Trading cluster unavailable
接口已废弃|||Operation deprecated
结果 Token ID|||Outcome token ID
结果 Token ID，十进制正整数|||Outcome token ID as a positive decimal integer
结果 Token ID；可省略，但建议传入|||Outcome token ID. Optional, but recommended.
结果 Token ID；已知时传入可减少一次订单查询|||Outcome token ID. Provide it when known to avoid an additional order lookup.
结果成立时可兑付金额|||Payout if the outcome resolves true
结果命中时的最大兑付金额|||Maximum payout if the outcome resolves true
结果名称|||Outcome name
结果数量|||Outcome count
结束时间|||End time
结束时间（Unix 毫秒）|||End time in Unix milliseconds
结束成交 ID 游标|||Ending trade-ID cursor
结束订单 ID 游标|||Ending order-ID cursor
结算来源|||Resolution source
拒绝或失败原因|||Rejection or failure reason
拒绝或失败原因码|||Rejection or failure reason code
拒绝原因码；成功时通常为 0|||Rejection reason code. Usually `0` on success.
开始时间|||Start time
起始时间（Unix 毫秒）|||Start time in Unix milliseconds
起始成交 ID 游标|||Starting trade-ID cursor
起始订单 ID 游标|||Starting order-ID cursor
可读错误信息，通常包含稳定错误标识|||Human-readable error message, usually containing a stable error identifier
可用持仓数量|||Available position quantity
可用数量|||Available quantity
可用余额|||Available balance
快照时间戳（Unix 毫秒）|||Snapshot timestamp in Unix milliseconds
累计成交量|||Cumulative trading volume
历史窗口，默认 1h|||History window. Defaults to `1h`.
历史委托|||Historical order
历史委托列表|||Order-history list
列表为空、超过 100 条或订单参数无效|||The list is empty, exceeds 100 items, or contains invalid order parameters
列表为空、超过 50 条或委托参数无效|||The list is empty, exceeds 50 items, or contains invalid order parameters
买卖价差|||Bid-ask spread
买盘，按价格排序|||Bids sorted by price
卖盘，按价格排序|||Asks sorted by price
卖一价减买一价|||Best ask minus best bid
每页数量，默认 20，最大 100|||Items per page. Defaults to 20; maximum 100.
页码，从 1 开始|||Page number, starting at 1.
符合条件的委托总数|||Total number of matching open orders
排序方向，默认 desc|||Sort direction. Defaults to `desc`.
排序字段，默认 volume|||Sort field. Defaults to `volume`.
排序字段；为空时使用服务默认顺序|||Sort field. Omit to use the service default.
批次是否成功提交|||Whether the batch was submitted successfully
批量撤单结果|||Batch cancellation result
批量创建委托|||Create orders in batch
批量取消委托|||Cancel orders in batch
批量委托参数|||Batch order request
批量委托受理结果|||Batch order acceptance result
匹配事件|||Matching events
匹配数量|||Number of matches
偏移量，默认 0|||Offset. Defaults to 0.
平均成本价|||Average cost
请求参数错误|||Invalid request parameters
请求参数无效|||Invalid request parameters
请求取消的订单 ID|||Order ID requested for cancellation
请求时间（Unix 毫秒）；每次提交取当前时间|||Request time in Unix milliseconds. Use the current time for every submission.
取消当前登录账户下的指定委托。tokenId 可省略，服务端会先从订单详情解析。|||Cancel an order owned by the authenticated account. `tokenId` is optional; when omitted, the service resolves it from the order details.
取消委托|||Cancel order
券商应用 ID，用于识别请求所属券商。|||Broker application ID used to route the request.
券商域名不存在|||Broker domain not found
筛选后的标签总数|||Total tags after filtering
筛选后的市场总数|||Total markets after filtering
筛选后的事件总数|||Total events after filtering
上一页末尾订单 ID；首次请求不传|||Last order ID from the previous page. Omit on the first request.
失败原因|||Failure reason
失败原因码|||Failure reason code
时间戳（Unix 毫秒）|||Timestamp in Unix milliseconds
实际使用的历史窗口|||History window applied by the service
实时数据频道|||Real-time data channel
使用 Secret Key 生成并经过 Base64 编码的 HMAC-SHA256 签名。|||Base64-encoded HMAC-SHA256 signature generated with the Secret Key.
市场 ID|||Market ID
市场 slug|||Market slug
市场不可交易或风控拒绝|||Market is not tradable or the request was rejected by risk controls
市场当前不允许撤单|||The market does not currently allow cancellations
市场累计成交量|||Cumulative market trading volume
市场列表|||Market list
市场条件 ID|||Market condition ID
市场问题|||Market question
市场行情|||Market ticker
市场行情不存在|||Market data not found
市场行情时间戳（Unix 毫秒）|||Market-data timestamp in Unix milliseconds
市场状态|||Market status
市场状态；为空时不筛选|||Market status. Omit to disable status filtering.
事件 ID|||Event ID
事件 ID 的兼容参数；eventId 为空时生效|||Compatibility alias for `eventId`; used only when `eventId` is omitted
事件 slug|||Event slug
事件 slug 无效|||Invalid event slug
事件 slug，例如 world-cup-2026|||Event slug, for example `world-cup-2026`
事件 slug；为空时查询全部事件下的市场|||Event slug. Omit to query markets across all events.
事件标题|||Event title
事件不存在|||Event not found
事件列表和事件总数|||Event list and total count
事件描述|||Event description
事件下的市场|||Markets in the event
事件下所有市场的累计成交量之和|||Sum of cumulative trading volume across all markets in the event
事件详情|||Event details
事件状态|||Event status
是否包含模板标签，默认 false|||Whether to include template tags. Defaults to `false`.
是否查询已关闭事件；不传表示不按关闭状态筛选|||Whether to include closed events. Omit to disable closed-state filtering.
是否撤单成功|||Whether the cancellation succeeded
是否处于争议状态|||Whether the event is disputed
是否仅返回轮播标签；不传表示不按该字段筛选|||Whether to return only carousel tags. Omit to disable this filter.
是否强制隐藏|||Whether the event is force-hidden
是否强制展示|||Whether the event is force-shown
是否受理成功|||Whether the request was accepted
是否为轮播标签|||Whether this is a carousel tag
是否为组合/隐含成交|||Whether this is a combined or implied trade
是否已关闭|||Whether the event is closed
搜索关键词；去除首尾空格后不能为空|||Search term. Must not be empty after trimming whitespace.
搜索结果|||Search results
搜索事件|||Search events
锁定数量|||Locked quantity
锁定持仓数量|||Locked position quantity
锁定余额|||Locked balance
条件 ID|||Condition ID
同步创建 1 至 50 笔委托并返回每笔处理结果。每项 timestamp 使用 Unix 毫秒且每次请求都应取当前时间；expiration 支持 Unix 秒或毫秒，传秒时服务端自动转换。|||Synchronously submit 1 to 50 orders and return the result for each item. Set each `timestamp` to the current Unix time in milliseconds. `expiration` accepts Unix seconds or milliseconds; the service converts seconds to milliseconds.
同步取消 1 至 100 笔委托。每项 tokenId 可省略，但建议传入以完成事件权限和市场生命周期校验。|||Synchronously cancel 1 to 100 orders. `tokenId` is optional, but providing it enables event-permission and market-lifecycle validation.
图标 URL|||Icon URL
图片 URL|||Image URL
委托不存在|||Order not found
委托参数|||Order request
委托参数无效|||Invalid order parameters
委托方向：BUY 或 SELL|||Order side: `BUY` or `SELL`
委托价|||Order price
委托价；MARKET 可为空，其他类型取值 (0,1)|||Order price. Optional for `MARKET`; otherwise must be between 0 and 1, exclusive.
委托价；MARKET 可为空，其他类型取值 (0,1) 且须符合价格步长|||Order price. Optional for `MARKET`; otherwise must be between 0 and 1, exclusive, and align with the tick size.
委托类型|||Order type
委托类型：GTC、FOK、GTD、FAK、MARKET；默认 GTC|||Order type: `GTC`, `FOK`, `GTD`, `FAK`, or `MARKET`. Defaults to `GTC`.
委托类型：LIMIT 或 MARKET；默认 LIMIT|||Order type: `LIMIT` or `MARKET`. Defaults to `LIMIT`.
委托受理结果|||Order acceptance result
委托数量，正整数份数|||Order quantity in whole shares as a positive integer
委托数量，十进制正整数字符串|||Order quantity as a positive decimal integer string
委托锁定数量|||Quantity locked by open orders
委托详情|||Order details
为当前登录账户创建委托。timestamp 使用 Unix 毫秒且每次请求都应取当前时间；GTD 的 expiration 必填，支持 Unix 秒或毫秒，服务端会将秒转换为毫秒。非 MARKET 委托的 price 必须在 0 到 1 之间并符合市场最小价格步长。|||Create an order for the authenticated account. Set `timestamp` to the current Unix time in milliseconds for every request. `expiration` is required for `GTD` and accepts Unix seconds or milliseconds; the service converts seconds to milliseconds. For non-`MARKET` orders, `price` must be between 0 and 1, exclusive, and align with the market tick size.
为当前登录账户创建委托。timestamp 使用 Unix 毫秒且每次请求都应取当前时间；GTD 的 expiration 必填且使用 Unix 毫秒。非 MARKET 委托的 price 必须在 0 到 1 之间并符合市场最小价格步长。|||Create an order for the authenticated account. Set `timestamp` to the current Unix time in milliseconds for every request. `expiration` is required for `GTD` and must use Unix milliseconds. For non-`MARKET` orders, `price` must be between 0 and 1, exclusive, and align with the market tick size.
未实现盈亏|||Unrealized PnL
未实现盈亏百分比|||Unrealized PnL percentage
有效方式；LIMIT 默认 GTC，MARKET 仅支持 IOC|||Time in force. `LIMIT` orders default to `GTC`; `MARKET` orders support only `IOC`.
有效方式：GTC、FOK、GTD 或 IOC|||Time in force: `GTC`, `FOK`, `GTD`, or `IOC`.
稳定业务错误码|||Stable business error code
行情时间戳（Unix 毫秒）|||Ticker timestamp in Unix milliseconds
页码，默认 1|||Page number. Defaults to 1.
已成交数量|||Filled quantity
用户 API Key（AK），用于 API Key 鉴权。|||User API key (AK) used for API Key authentication.
用户登录后获得的访问 Token。仅 `/v1/private` 接口需要传入。|||Access token issued after sign-in. Required only for `/v1/private` operations.
用户接口-成交|||Trades
用户接口-市场|||Market data
用户接口-事件|||Events
用户接口-委托|||Orders
用户接口-元数据|||Metadata
用户接口-账户|||Accounts
游标分页查询事件（已废弃）|||List events with cursor pagination (deprecated)
原始委托数量|||Original order quantity
账户 ID|||Account ID
账户成交列表|||Account-trade list
账户汇总缓存未就绪或刷新失败|||Account summary cache is not ready or could not be refreshed
账户资产汇总|||Account asset summary
中间价|||Midpoint price
中间价不存在|||Midpoint price not found
总持仓数量|||Total position quantity
最小价格步长；创建委托时价格必须是其整数倍|||Minimum tick size. Order prices must be an integer multiple of this value.
最小委托数量|||Minimum order quantity
最新成交价|||Latest execution price
市场价格|||Market price
最优买价|||Best bid
最优买卖价中间值|||Midpoint of the best bid and best ask
最优卖价|||Best ask
catalog 或 ticker 全量快照尚未就绪|||The full `catalog` or `ticker` snapshot is not ready
GTD 到期时间，Unix 秒或毫秒；其他类型可为 0|||`GTD` expiration time in Unix seconds or milliseconds. Use `0` for other order types.
GTD 到期时间（Unix 毫秒）；其他类型必须为 0|||`GTD` expiration time in Unix milliseconds. Must be `0` for other order types.
NO 结果 Token ID|||NO outcome token ID
NO 结果展示名|||NO outcome display name
read-service 不可用|||The read service is unavailable
Token 或时间窗口无效|||Invalid token or time window
Token 无效或缺失|||Token is invalid or missing
Token ID 无效|||Invalid token ID
USDC 余额|||USDC balance
YES 结果 Token ID|||YES outcome token ID
YES 结果展示名|||YES outcome display name
zpm 预测市场用户 API v2|||topblast Prediction Market Trading API v2
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
