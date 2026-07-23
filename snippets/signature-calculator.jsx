export const SignatureCalculator = ({ locale = "zh" }) => {
  const isEnglish = locale === "en";
  const copy = isEnglish
    ? {
        missingFields: "Enter the App ID, App Secret, timestamp, and request path.",
        invalidPath: "The request path must start with / and must not include a domain.",
        calculationFailed: "Signature calculation failed",
        appIdPlaceholder: "Enter x-app-id",
        secretPlaceholder: "Used only in this browser",
        timestamp: "Timestamp",
        timestampPlaceholder: "Unix seconds or milliseconds",
        useCurrentTime: "Use current time",
        method: "HTTP method",
        requestPath: "Request path",
        query: "Query string (omit the leading ?)",
        body: "Request body (raw JSON; leave empty when unused)",
        calculate: "Calculate signature",
        payload: "Signature payload",
        copied: "Copied",
        copyHeaders: "Copy headers",
      }
    : {
        missingFields: "请填写 App ID、App Secret、时间戳和请求路径。",
        invalidPath: "请求路径必须以 / 开头，且不能包含域名。",
        calculationFailed: "签名计算失败",
        appIdPlaceholder: "输入 x-app-id",
        secretPlaceholder: "仅在当前浏览器中参与计算",
        timestamp: "时间戳",
        timestampPlaceholder: "秒或毫秒时间戳",
        useCurrentTime: "使用当前时间",
        method: "HTTP 方法",
        requestPath: "请求路径",
        query: "Query 参数（原始字符串，可省略开头的 ?）",
        body: "请求 Body（原始 JSON，无请求体时留空）",
        calculate: "计算签名",
        payload: "待签名字符串",
        copied: "已复制",
        copyHeaders: "复制请求头",
      };
  const inputClassName =
    "w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-orange-500 focus:ring-2 focus:ring-orange-100 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100";
  const labelClassName =
    "mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-200";
  const toBase64 = (buffer) => {
    const bytes = new Uint8Array(buffer);
    let binary = "";
    bytes.forEach((byte) => {
      binary += String.fromCharCode(byte);
    });
    return btoa(binary);
  };

  const [appId, setAppId] = useState("");
  const [appSecret, setAppSecret] = useState("");
  const [timestamp, setTimestamp] = useState(() => String(Date.now()));
  const [method, setMethod] = useState("POST");
  const [path, setPath] = useState("/v1/broker/tokens");
  const [query, setQuery] = useState("");
  const [body, setBody] = useState("");
  const [stringToSign, setStringToSign] = useState("");
  const [signature, setSignature] = useState("");
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const refreshTimestamp = () => {
    setTimestamp(String(Date.now()));
  };

  const calculate = async () => {
    setError("");
    setCopied(false);

    if (!appId.trim() || !appSecret || !timestamp.trim() || !path.trim()) {
      setError(copy.missingFields);
      return;
    }

    if (!path.startsWith("/")) {
      setError(copy.invalidPath);
      return;
    }

    try {
      const rawQuery = query.startsWith("?") ? query.slice(1) : query;
      const payload =
        timestamp.trim() +
        method.toUpperCase() +
        path +
        (rawQuery ? `?${rawQuery}` : "") +
        body;
      const encoder = new TextEncoder();
      const key = await crypto.subtle.importKey(
        "raw",
        encoder.encode(appSecret),
        { name: "HMAC", hash: "SHA-256" },
        false,
        ["sign"],
      );
      const digest = await crypto.subtle.sign("HMAC", key, encoder.encode(payload));

      setStringToSign(payload);
      setSignature(toBase64(digest));
    } catch (calculationError) {
      setError(`${copy.calculationFailed}: ${calculationError.message}`);
    }
  };

  const copyHeaders = async () => {
    if (!signature) return;
    await navigator.clipboard.writeText(
      `x-app-id: ${appId.trim()}\nx-timestamp: ${timestamp.trim()}\nx-signature: ${signature}`,
    );
    setCopied(true);
  };

  return (
    <div className="my-6 rounded-xl border border-gray-200 bg-gray-50 p-5 dark:border-gray-800 dark:bg-gray-950">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className={labelClassName}>App ID</label>
          <input
            className={inputClassName}
            value={appId}
            onChange={(event) => setAppId(event.target.value)}
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
            onChange={(event) => setAppSecret(event.target.value)}
            placeholder={copy.secretPlaceholder}
            autoComplete="new-password"
          />
        </div>
        <div>
          <label className={labelClassName}>{copy.timestamp}</label>
          <div className="flex gap-2">
            <input
              className={inputClassName}
              value={timestamp}
              onChange={(event) => setTimestamp(event.target.value)}
              placeholder={copy.timestampPlaceholder}
            />
            <button
              type="button"
              onClick={refreshTimestamp}
              className="shrink-0 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900"
            >
              {copy.useCurrentTime}
            </button>
          </div>
        </div>
        <div>
          <label className={labelClassName}>{copy.method}</label>
          <select
            className={inputClassName}
            value={method}
            onChange={(event) => setMethod(event.target.value)}
          >
            <option>GET</option>
            <option>POST</option>
            <option>PUT</option>
            <option>PATCH</option>
            <option>DELETE</option>
          </select>
        </div>
      </div>

      <div className="mt-4">
        <label className={labelClassName}>{copy.requestPath}</label>
        <input
          className={inputClassName}
          value={path}
          onChange={(event) => setPath(event.target.value)}
          placeholder="/v1/broker/tokens"
        />
      </div>

      <div className="mt-4">
        <label className={labelClassName}>{copy.query}</label>
        <input
          className={inputClassName}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="page=1&size=20"
        />
      </div>

      <div className="mt-4">
        <label className={labelClassName}>{copy.body}</label>
        <textarea
          className={`${inputClassName} min-h-32 font-mono`}
          value={body}
          onChange={(event) => setBody(event.target.value)}
          placeholder={'{"userId":"broker-user-10001","token":"token-value"}'}
          spellCheck={false}
        />
      </div>

      {error && (
        <div className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
          {error}
        </div>
      )}

      <button
        type="button"
        onClick={calculate}
        className="mt-5 rounded-lg bg-orange-600 px-4 py-2 text-sm font-semibold text-white hover:bg-orange-700"
      >
        {copy.calculate}
      </button>

      {signature && (
        <div className="mt-6 space-y-4">
          <div>
            <div className={labelClassName}>{copy.payload}</div>
            <pre className="overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
              {stringToSign}
            </pre>
          </div>
          <div>
            <div className={labelClassName}>x-signature</div>
            <pre className="overflow-x-auto whitespace-pre-wrap break-all rounded-lg bg-gray-900 p-3 text-sm text-gray-100">
              {signature}
            </pre>
          </div>
          <button
            type="button"
            onClick={copyHeaders}
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium dark:border-gray-700 dark:bg-gray-900"
          >
            {copied ? copy.copied : copy.copyHeaders}
          </button>
        </div>
      )}
    </div>
  );
};
