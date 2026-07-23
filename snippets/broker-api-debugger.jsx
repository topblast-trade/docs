export const BrokerApiDebugger = ({ locale = "zh" }) => {
  const isEnglish = locale === "en";
  const copy = isEnglish
    ? {
        restored: "Restored App ID / App Secret from local storage",
        missingCredentials: "Enter the App ID and App Secret.",
        invalidPath: "The request path must start with / and must not include a domain.",
        unresolvedPath: "Replace every path placeholder with an actual value, such as eventSlug.",
        invalidJson: "The request body is not valid JSON",
        proxyFailed: "Mintlify proxy request failed",
        requestFailed: "Request failed",
        credentialsRequired: "Enter the App ID and App Secret first",
        credentialsSaved: "Saved App ID / App Secret in this browser",
        credentialsCleared: "Cleared local values and restored the default App ID / App Secret",
        environment: "Environment",
        testEnvironment: "Test environment",
        operation: "Operation",
        appIdPlaceholder: "Enter x-app-id",
        secretPlaceholder: "Enter the App Secret",
        saveCredentials: "Save App ID / App Secret",
        clearCredentials: "Clear App ID / App Secret",
        requestPath: "Request path",
        query: "Query string (omit the leading ?)",
        body: "Request body (leave empty when unused)",
        sending: "Sending...",
        send: "Send",
        requestUrl: "Request URL",
        signaturePayload: "Signature payload",
        requestSignature: "Request signature",
        response: "Response",
        emptyResponse: "(empty response)",
      }
    : {
        restored: "已从本地恢复 App ID / App Secret",
        missingCredentials: "请填写 App ID 和 App Secret。",
        invalidPath: "请求路径必须以 / 开头，且不能包含域名。",
        unresolvedPath: "请将请求路径中的占位符替换为实际值，例如 eventSlug。",
        invalidJson: "请求 Body 不是有效 JSON",
        proxyFailed: "Mintlify 代理请求失败",
        requestFailed: "请求发送失败",
        credentialsRequired: "请先填写 App ID 和 App Secret",
        credentialsSaved: "App ID / App Secret 已保存到当前浏览器",
        credentialsCleared: "已清除本地保存值并恢复默认 App ID / App Secret",
        environment: "环境",
        testEnvironment: "测试环境",
        operation: "接口",
        appIdPlaceholder: "输入 x-app-id",
        secretPlaceholder: "输入 App Secret",
        saveCredentials: "保存 App ID / App Secret",
        clearCredentials: "清除 App ID / App Secret",
        requestPath: "请求路径",
        query: "Query（原始字符串，可省略开头的 ?）",
        body: "请求 Body（无请求体时留空）",
        sending: "发送中...",
        send: "发送",
        requestUrl: "请求地址",
        signaturePayload: "待签名字符串",
        requestSignature: "请求签名",
        response: "响应结果",
        emptyResponse: "（空响应）",
      };
  const inputClassName =
    "w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100";
  const labelClassName =
    "mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-200";
  const panelClassName =
    "rounded-xl border border-gray-200 bg-gray-50 p-5 dark:border-gray-800 dark:bg-gray-950";
  const defaultAppId = "ba11_90ea03143437e68fc1c2eb6b";
  const defaultAppSecret =
    "bs11_f154c04553ddd705662184d3728bfb398aa78182d014e8b09a7c2ee7e9c28b57";
  const credentialStorageKey = "topblast-broker-api-debugger-credentials";
  const endpoints = [
    ["POST", "/v1/broker/tokens", "同步用户 Token", "Synchronize user token"],
    ["DELETE", "/v1/broker/{userId}/tokens", "删除用户 Token", "Delete user token"],
    ["GET", "/v1/broker/users", "查询用户列表", "List users"],
    ["PATCH", "/v1/broker/users/{userId}", "更新用户", "Update user"],
    ["POST", "/v1/broker/special-users", "创建特殊账户", "Create special account"],
    ["GET", "/v1/broker/users/{userId}/api-keys", "查询用户 API Key", "List user API keys"],
    ["POST", "/v1/broker/users/{userId}/api-keys", "创建用户 API Key", "Create user API key"],
    ["DELETE", "/v1/broker/users/{userId}/api-keys/{apiKey}", "删除用户 API Key", "Delete user API key"],
    ["GET", "/v1/broker/settings", "查询券商设置", "Get broker settings"],
    ["PATCH", "/v1/broker/settings", "更新券商设置", "Update broker settings"],
    ["POST", "/v1/broker/transfers", "创建划转", "Create transfer"],
    ["GET", "/v1/broker/transfers", "查询划转列表", "List transfers"],
    ["GET", "/v1/broker/transfers/{transferId}", "查询划转详情", "Get transfer"],
    ["GET", "/v1/broker/assets", "查询资产", "List assets"],
    ["GET", "/v1/broker/trades", "查询成交记录", "List trades"],
    ["GET", "/v1/broker/orders", "查询当前委托", "List open orders"],
    ["DELETE", "/v1/broker/orders/{orderId}", "取消委托", "Cancel order"],
    ["GET", "/v1/broker/positions", "查询仓位", "List positions"],
    ["POST", "/v1/broker/positions/closures", "平仓", "Close position"],
    ["GET", "/v1/broker/reports/summaries/{period}", "查询汇总报表", "Get summary report"],
    ["GET", "/v1/broker/reports/daily-summaries", "查询每日汇总", "List daily summaries"],
    ["GET", "/v1/broker/reports/trends", "查询趋势报表", "List report trends"],
    ["GET", "/v1/broker/reports/dashboard", "查询仪表盘", "Get dashboard"],
    ["GET", "/v1/broker/events", "查询事件", "List events"],
    ["PATCH", "/v1/broker/events/{eventSlug}", "更新事件", "Update event"],
    ["GET", "/v1/broker/events/{eventSlug}/markets", "查询事件市场", "List event markets"],
    ["PATCH", "/v1/broker/events/{eventSlug}/markets/{marketId}", "更新市场", "Update market"],
    ["GET", "/v1/broker/risk/policies", "查询风控策略", "List risk policies"],
    ["GET", "/v1/broker/risk/exposures", "查询风险敞口", "List risk exposures"],
    ["GET", "/v1/broker/risk/config", "查询风控配置", "Get risk configuration"],
    ["PATCH", "/v1/broker/risk/config", "保存风控配置", "Save risk configuration"],
  ].map(([method, path, zhSummary, enSummary]) => ({
    id: `${method} ${path}`,
    method,
    path,
    summary: isEnglish ? enSummary : zhSummary,
  }));

  const [selectedID, setSelectedID] = useState(endpoints[0].id);
  const [environment, setEnvironment] = useState("https://api-test.topblast.trade");
  const [appId, setAppId] = useState(defaultAppId);
  const [appSecret, setAppSecret] = useState(defaultAppSecret);
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
      if (savedCredentials?.appId && savedCredentials?.appSecret) {
        setAppId(savedCredentials.appId);
        setAppSecret(savedCredentials.appSecret);
        setCredentialStatus(copy.restored);
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

    if (!appId.trim() || !appSecret) {
      setError(copy.missingCredentials);
      return;
    }
    if (!requestPath.startsWith("/")) {
      setError(copy.invalidPath);
      return;
    }
    if (requestPath.includes("{") || requestPath.includes("}")) {
      setError(copy.unresolvedPath);
      return;
    }
    if (requestBody.trim()) {
      try {
        JSON.parse(requestBody);
      } catch (jsonError) {
        setError(`${copy.invalidJson}: ${jsonError.message}`);
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
      const signature = await calculateSignature(appSecret, stringToSign);
      const requestURL = `${environment}${requestPath}${query ? `?${query}` : ""}`;
      const headers = {
        "x-app-id": appId.trim(),
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
          proxyResult.errorMessage || `${copy.proxyFailed} (HTTP ${response.status})`,
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
      setError(`${copy.requestFailed}: ${requestError.message}`);
    } finally {
      setSending(false);
    }
  };

  const saveCredentials = () => {
    if (!appId.trim() || !appSecret) {
      setCredentialStatus(copy.credentialsRequired);
      return;
    }
    localStorage.setItem(
      credentialStorageKey,
      JSON.stringify({ appId: appId.trim(), appSecret }),
    );
    setAppId(appId.trim());
    setCredentialStatus(copy.credentialsSaved);
  };

  const clearCredentials = () => {
    localStorage.removeItem(credentialStorageKey);
    setAppId(defaultAppId);
    setAppSecret(defaultAppSecret);
    setCredentialStatus(copy.credentialsCleared);
    setResult(null);
  };

  return (
    <div className="my-6 space-y-5">
      <div className={panelClassName}>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className={labelClassName}>{copy.environment}</label>
            <select
              className={inputClassName}
              value={environment}
              onChange={(event) => setEnvironment(event.target.value)}
            >
              <option value="https://api-test.topblast.trade">{copy.testEnvironment}</option>
            </select>
          </div>
          <div>
            <label className={labelClassName}>{copy.operation}</label>
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
            <label className={labelClassName}>App ID</label>
            <input
              className={inputClassName}
              value={appId}
              onChange={(event) => {
                setAppId(event.target.value);
                setCredentialStatus("");
              }}
              placeholder={copy.appIdPlaceholder}
              autoComplete="off"
            />
          </div>
          <div>
            <label className={labelClassName}>App Secret</label>
            <input
              className={inputClassName}
              type="password"
              value={appSecret}
              onChange={(event) => {
                setAppSecret(event.target.value);
                setCredentialStatus("");
              }}
              placeholder={copy.secretPlaceholder}
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
            {copy.saveCredentials}
          </button>
          <button
            type="button"
            onClick={clearCredentials}
            className="text-sm text-gray-500 underline dark:text-gray-400"
          >
            {copy.clearCredentials}
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
          <label className={labelClassName}>{copy.requestPath}</label>
          <input
            className={inputClassName}
            value={requestPath}
            onChange={(event) => setRequestPath(event.target.value)}
            placeholder="/v1/broker/tokens"
          />
        </div>
        <div className="mt-4">
          <label className={labelClassName}>{copy.query}</label>
          <input
            className={inputClassName}
            value={rawQuery}
            onChange={(event) => setRawQuery(event.target.value)}
            placeholder="page=1&size=20"
          />
        </div>
        <div className="mt-4">
          <label className={labelClassName}>{copy.body}</label>
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
        {sending ? copy.sending : copy.send}
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
          <div className={labelClassName}>{copy.requestUrl}</div>
          <pre className="mb-4 overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.requestURL}
          </pre>
          <div className={labelClassName}>{copy.signaturePayload}</div>
          <pre className="mb-4 overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.stringToSign}
          </pre>
          <div className={labelClassName}>{copy.requestSignature}</div>
          <pre className="mb-4 overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.signature}
          </pre>
          <div className={labelClassName}>{copy.response}</div>
          <pre className="max-h-96 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
            {result.responseBody || copy.emptyResponse}
          </pre>
        </div>
      )}
    </div>
  );
};
