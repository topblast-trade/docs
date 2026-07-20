export const BrokerApiDebugger = () => {
  const inputClassName =
    "w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100";
  const labelClassName =
    "mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-200";
  const panelClassName =
    "rounded-xl border border-gray-200 bg-gray-50 p-5 dark:border-gray-800 dark:bg-gray-950";
  const defaultApiKey = "ba11_90ea03143437e68fc1c2eb6b";
  const defaultApiSecret =
    "bs11_f154c04553ddd705662184d3728bfb398aa78182d014e8b09a7c2ee7e9c28b57";
  const credentialStorageKey = "topblast-broker-api-debugger-credentials";
  const endpoints = [
    ["POST", "/v1/broker/user/login", "用户登录"],
    ["POST", "/v1/broker/user/logout", "用户登出"],
    ["POST", "/v1/broker/user/update", "更新用户"],
    ["POST", "/v1/broker/user/createSpecial", "创建特殊账户"],
    ["GET", "/v1/broker/user/users", "查询用户列表"],
    ["POST", "/v1/broker/transfer", "创建划转"],
    ["GET", "/v1/broker/transfer/list", "查询划转列表"],
    ["GET", "/v1/broker/transfer/detail", "查询划转详情"],
    ["GET", "/v1/broker/assets", "查询资产"],
    ["GET", "/v1/broker/trade/trades", "查询成交记录"],
    ["GET", "/v1/broker/trade/positions", "查询仓位"],
    ["GET", "/v1/broker/trade/openOrders", "查询当前委托"],
    ["POST", "/v1/broker/trade/orders/cancel", "取消委托"],
    ["POST", "/v1/broker/trade/positions/close", "平仓"],
    ["GET", "/v1/broker/reports/summary", "查询汇总报表"],
    ["GET", "/v1/broker/reports/trend", "查询趋势报表"],
    ["GET", "/v1/broker/dailySummaries", "查询每日汇总"],
    ["GET", "/v1/broker/dashboard", "查询仪表盘"],
    ["GET", "/v1/broker/events", "查询事件"],
    ["POST", "/v1/broker/events/{eventSlug}/enable", "启用事件"],
    ["POST", "/v1/broker/events/{eventSlug}/disable", "停用事件"],
    ["GET", "/v1/broker/events/{eventSlug}/markets", "查询事件市场"],
    ["POST", "/v1/broker/events/{eventSlug}/markets/{marketId}/enable", "启用市场"],
    ["POST", "/v1/broker/events/{eventSlug}/markets/{marketId}/disable", "停用市场"],
    ["GET", "/v1/broker/risk/policies", "查询风控策略"],
    ["GET", "/v1/broker/risk/exposures", "查询风险敞口"],
    ["GET", "/v1/broker/risk/config", "查询风控配置"],
    ["POST", "/v1/broker/risk/config", "保存风控配置"],
  ].map(([method, path, summary]) => ({
    id: `${method} ${path}`,
    method,
    path,
    summary,
  }));

  const [selectedID, setSelectedID] = useState(endpoints[0].id);
  const [environment, setEnvironment] = useState("https://api.topblast.trade");
  const [apiKey, setApiKey] = useState(defaultApiKey);
  const [apiSecret, setApiSecret] = useState(defaultApiSecret);
  const [credentialStatus, setCredentialStatus] = useState("");
  const [requestPath, setRequestPath] = useState(endpoints[0].path);
  const [rawQuery, setRawQuery] = useState("");
  const [requestBody, setRequestBody] = useState("{}");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const selectedEndpoint = endpoints.find((endpoint) => endpoint.id === selectedID);

  useEffect(() => {
    try {
      const savedCredentials = JSON.parse(
        localStorage.getItem(credentialStorageKey) || "null",
      );
      if (savedCredentials?.apiKey && savedCredentials?.apiSecret) {
        setApiKey(savedCredentials.apiKey);
        setApiSecret(savedCredentials.apiSecret);
        setCredentialStatus("已从本地恢复 AK / SK");
      }
    } catch (_) {
      localStorage.removeItem(credentialStorageKey);
    }
  }, []);

  const toBase64 = (buffer) => {
    const bytes = new Uint8Array(buffer);
    let binary = "";
    bytes.forEach((byte) => {
      binary += String.fromCharCode(byte);
    });
    return btoa(binary);
  };

  const fromBase64 = (value) => {
    const binary = atob(value);
    const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
    return new TextDecoder().decode(bytes);
  };

  const calculateSignature = async (secret, payload) => {
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
      "raw",
      encoder.encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"],
    );
    const digest = await crypto.subtle.sign("HMAC", key, encoder.encode(payload));
    return toBase64(digest);
  };

  const selectEndpoint = (id) => {
    const endpoint = endpoints.find((item) => item.id === id);
    setSelectedID(id);
    setRequestPath(endpoint.path);
    setRawQuery("");
    setRequestBody(endpoint.method === "GET" ? "" : "{}");
    setResult(null);
    setError("");
  };

  const sendRequest = async () => {
    setError("");
    setResult(null);

    if (!apiKey.trim() || !apiSecret) {
      setError("请填写 AK 和 SK。");
      return;
    }
    if (!requestPath.startsWith("/")) {
      setError("请求路径必须以 / 开头，且不能包含域名。");
      return;
    }
    if (requestPath.includes("{") || requestPath.includes("}")) {
      setError("请将请求路径中的占位符替换为实际值，例如 eventSlug。");
      return;
    }
    if (requestBody.trim()) {
      try {
        JSON.parse(requestBody);
      } catch (jsonError) {
        setError(`请求 Body 不是有效 JSON：${jsonError.message}`);
        return;
      }
    }

    setSending(true);
    const startedAt = Date.now();
    try {
      const query = rawQuery.startsWith("?") ? rawQuery.slice(1) : rawQuery;
      const body = requestBody.trim() ? requestBody : "";
      const timestamp = String(Date.now());
      const stringToSign =
        timestamp +
        selectedEndpoint.method +
        requestPath +
        (query ? `?${query}` : "") +
        body;
      const signature = await calculateSignature(apiSecret, stringToSign);
      const requestURL = `${environment}${requestPath}${query ? `?${query}` : ""}`;
      const headers = {
        "x-api-key": apiKey.trim(),
        "x-timestamp": timestamp,
        "x-signature": signature,
      };
      if (body) headers["Content-Type"] = "application/json";

      const response = await fetch("/_mintlify/api/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          method: selectedEndpoint.method,
          url: requestURL,
          header: headers,
          body: body || undefined,
          cookie: {},
          query: {},
        }),
      });
      const proxyResult = await response.json();
      if (!response.ok || proxyResult.error || !proxyResult.response) {
        throw new Error(
          proxyResult.errorMessage || `Mintlify 代理请求失败（HTTP ${response.status}）`,
        );
      }

      const proxiedResponse = proxyResult.response;
      const encodedResponseData = proxiedResponse.data ?? "";
      let responseData = encodedResponseData;
      if (typeof encodedResponseData === "string" && encodedResponseData) {
        try {
          responseData = fromBase64(encodedResponseData);
        } catch (_) {
          // Keep the original value if the proxy returns plain text.
        }
      }
      let responseBody =
        typeof responseData === "string"
          ? responseData
          : JSON.stringify(responseData, null, 2);
      if (typeof responseData === "string") {
        try {
          responseBody = JSON.stringify(JSON.parse(responseData), null, 2);
        } catch (_) {
          // Keep non-JSON responses as text.
        }
      }
      setResult({
        ok: proxiedResponse.status >= 200 && proxiedResponse.status < 300,
        status: proxiedResponse.status,
        statusText: proxiedResponse.statusText,
        duration: Date.now() - startedAt,
        requestURL,
        timestamp,
        signature,
        stringToSign,
        responseBody,
      });
    } catch (requestError) {
      setError(`请求发送失败：${requestError.message}`);
    } finally {
      setSending(false);
    }
  };

  const saveCredentials = () => {
    if (!apiKey.trim() || !apiSecret) {
      setCredentialStatus("请先填写 AK 和 SK");
      return;
    }
    localStorage.setItem(
      credentialStorageKey,
      JSON.stringify({ apiKey: apiKey.trim(), apiSecret }),
    );
    setApiKey(apiKey.trim());
    setCredentialStatus("AK / SK 已保存到当前浏览器");
  };

  const clearCredentials = () => {
    localStorage.removeItem(credentialStorageKey);
    setApiKey(defaultApiKey);
    setApiSecret(defaultApiSecret);
    setCredentialStatus("已清除本地保存值并恢复默认 AK / SK");
    setResult(null);
  };

  return (
    <div className="my-6 space-y-5">
      <div className={panelClassName}>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className={labelClassName}>环境</label>
            <select
              className={inputClassName}
              value={environment}
              onChange={(event) => setEnvironment(event.target.value)}
            >
              <option value="https://api.topblast.trade">生产环境</option>
              <option value="https://api-test.topblast.trade">测试环境</option>
              <option value="https://api-dev.topblast.trade">开发环境</option>
            </select>
          </div>
          <div>
            <label className={labelClassName}>接口</label>
            <select
              className={inputClassName}
              value={selectedID}
              onChange={(event) => selectEndpoint(event.target.value)}
            >
              {endpoints.map((endpoint) => (
                <option key={endpoint.id} value={endpoint.id}>
                  {endpoint.method} {endpoint.path} — {endpoint.summary}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className={labelClassName}>AK（API Key）</label>
            <input
              className={inputClassName}
              value={apiKey}
              onChange={(event) => {
                setApiKey(event.target.value);
                setCredentialStatus("");
              }}
              placeholder="输入 x-api-key"
              autoComplete="off"
            />
          </div>
          <div>
            <label className={labelClassName}>SK（API Secret）</label>
            <input
              className={inputClassName}
              type="password"
              value={apiSecret}
              onChange={(event) => {
                setApiSecret(event.target.value);
                setCredentialStatus("");
              }}
              placeholder="输入 x-api-secret"
              autoComplete="new-password"
            />
          </div>
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={saveCredentials}
            className="rounded-md bg-orange-600 px-2 py-1 text-xs font-medium text-white hover:bg-orange-700"
          >
            保存 AK / SK
          </button>
          <button
            type="button"
            onClick={clearCredentials}
            className="text-sm text-gray-500 underline dark:text-gray-400"
          >
            清除 AK / SK
          </button>
          {credentialStatus && (
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {credentialStatus}
            </span>
          )}
        </div>
      </div>

      <div className={panelClassName}>
        <div>
          <label className={labelClassName}>请求路径</label>
          <input
            className={inputClassName}
            value={requestPath}
            onChange={(event) => setRequestPath(event.target.value)}
            placeholder="/v1/broker/user/login"
          />
        </div>
        <div className="mt-4">
          <label className={labelClassName}>Query（原始字符串，可省略开头的 ?）</label>
          <input
            className={inputClassName}
            value={rawQuery}
            onChange={(event) => setRawQuery(event.target.value)}
            placeholder="userId=10001&page=1&pageSize=20"
          />
        </div>
        <div className="mt-4">
          <label className={labelClassName}>请求 Body（无请求体时留空）</label>
          <textarea
            className={`${inputClassName} min-h-56 font-mono`}
            value={requestBody}
            onChange={(event) => setRequestBody(event.target.value)}
            placeholder={'{"userId":"broker-user-10001","token":"token-value"}'}
            spellCheck={false}
          />
        </div>
      </div>

      {error && (
        <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
          {error}
        </div>
      )}

      <button
        type="button"
        onClick={sendRequest}
        disabled={sending}
        className="rounded-lg bg-orange-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-orange-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {sending ? "发送中..." : "Send"}
      </button>

      {result && (
        <div className={panelClassName}>
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <span
              className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
                result.ok
                  ? "bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300"
                  : "bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300"
              }`}
            >
              HTTP {result.status} {result.statusText}
            </span>
            <span className="text-xs text-gray-500">{result.duration} ms</span>
          </div>
          <div className={labelClassName}>请求地址</div>
          <pre className="mb-4 overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.requestURL}
          </pre>
          <div className={labelClassName}>待签名字符串</div>
          <pre className="mb-4 overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.stringToSign}
          </pre>
          <div className={labelClassName}>请求签名</div>
          <pre className="mb-4 overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.signature}
          </pre>
          <div className={labelClassName}>响应结果</div>
          <pre className="max-h-96 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.responseBody || "（空响应）"}
          </pre>
        </div>
      )}
    </div>
  );
};
