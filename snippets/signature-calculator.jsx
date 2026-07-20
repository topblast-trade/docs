export const SignatureCalculator = () => {
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

  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [timestamp, setTimestamp] = useState(() => String(Date.now()));
  const [method, setMethod] = useState("POST");
  const [path, setPath] = useState("/api/v1/broker/user/login");
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

    if (!apiKey.trim() || !apiSecret || !timestamp.trim() || !path.trim()) {
      setError("请填写 AK、SK、时间戳和请求路径。");
      return;
    }

    if (!path.startsWith("/")) {
      setError("请求路径必须以 / 开头，且不能包含域名。");
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
        encoder.encode(apiSecret),
        { name: "HMAC", hash: "SHA-256" },
        false,
        ["sign"],
      );
      const digest = await crypto.subtle.sign("HMAC", key, encoder.encode(payload));

      setStringToSign(payload);
      setSignature(toBase64(digest));
    } catch (calculationError) {
      setError(`签名计算失败：${calculationError.message}`);
    }
  };

  const copyHeaders = async () => {
    if (!signature) return;
    await navigator.clipboard.writeText(
      `x-api-key: ${apiKey.trim()}\nx-timestamp: ${timestamp.trim()}\nx-signature: ${signature}`,
    );
    setCopied(true);
  };

  return (
    <div className="my-6 rounded-xl border border-gray-200 bg-gray-50 p-5 dark:border-gray-800 dark:bg-gray-950">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className={labelClassName}>AK（API Key）</label>
          <input
            className={inputClassName}
            value={apiKey}
            onChange={(event) => setApiKey(event.target.value)}
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
            onChange={(event) => setApiSecret(event.target.value)}
            placeholder="仅在当前浏览器中参与计算"
            autoComplete="new-password"
          />
        </div>
        <div>
          <label className={labelClassName}>时间戳</label>
          <div className="flex gap-2">
            <input
              className={inputClassName}
              value={timestamp}
              onChange={(event) => setTimestamp(event.target.value)}
              placeholder="秒或毫秒时间戳"
            />
            <button
              type="button"
              onClick={refreshTimestamp}
              className="shrink-0 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900"
            >
              使用当前时间
            </button>
          </div>
        </div>
        <div>
          <label className={labelClassName}>HTTP 方法</label>
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
        <label className={labelClassName}>请求路径</label>
        <input
          className={inputClassName}
          value={path}
          onChange={(event) => setPath(event.target.value)}
          placeholder="/api/v1/broker/user/login"
        />
      </div>

      <div className="mt-4">
        <label className={labelClassName}>Query 参数（原始字符串，可省略开头的 ?）</label>
        <input
          className={inputClassName}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="userId=10001&page=1&pageSize=20"
        />
      </div>

      <div className="mt-4">
        <label className={labelClassName}>请求 Body（原始 JSON，无请求体时留空）</label>
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
        计算签名
      </button>

      {signature && (
        <div className="mt-6 space-y-4">
          <div>
            <div className={labelClassName}>待签名字符串</div>
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
            {copied ? "已复制" : "复制请求头"}
          </button>
        </div>
      )}
    </div>
  );
};
