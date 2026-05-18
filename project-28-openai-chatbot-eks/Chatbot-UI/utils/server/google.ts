export const cleanSourceText = (text: string) => {
  return text
    .trim()
    .replace(/(\n){4,}/g, '\n\n\n')
    .replace(/\n\n/g, ' ')
    .replace(/ {3,}/g, '  ')
    .replace(/\t/g, '')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n+(\s*\n)*/g, '\n');
};

const BLOCKED_HOSTS = new Set(['localhost', '0.0.0.0']);
const MAX_SOURCE_BYTES = 500000;

export const isPublicHTTPURL = (value: string) => {
  try {
    const url = new URL(value);
    const hostname = url.hostname.toLowerCase();

    if (url.protocol !== 'http:' && url.protocol !== 'https:') {
      return false;
    }

    if (url.username || url.password) {
      return false;
    }

    if (
      BLOCKED_HOSTS.has(hostname) ||
      hostname.endsWith('.localhost') ||
      hostname.endsWith('.local') ||
      hostname.endsWith('.internal')
    ) {
      return false;
    }

    return !isPrivateIPAddress(hostname);
  } catch {
    return false;
  }
};

export const readLimitedText = async (response: Response) => {
  const contentLength = response.headers.get('content-length');
  if (contentLength && Number(contentLength) > MAX_SOURCE_BYTES) {
    return null;
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/html') && !contentType.includes('text/plain')) {
    return null;
  }

  const reader = response.body?.getReader();
  if (!reader) {
    return null;
  }

  const chunks: Uint8Array[] = [];
  let received = 0;

  while (received <= MAX_SOURCE_BYTES) {
    const { done, value } = await reader.read();
    if (done) {
      return new TextDecoder().decode(concatChunks(chunks, received));
    }

    received += value.length;
    chunks.push(value);
  }

  await reader.cancel();
  return null;
};

const concatChunks = (chunks: Uint8Array[], totalLength: number) => {
  const merged = new Uint8Array(totalLength);
  let offset = 0;

  for (const chunk of chunks) {
    merged.set(chunk, offset);
    offset += chunk.length;
  }

  return merged;
};

const isPrivateIPAddress = (hostname: string): boolean => {
  if (hostname.startsWith('[') && hostname.endsWith(']')) {
    return isPrivateIPAddress(hostname.slice(1, -1));
  }

  if (isPrivateIPv6Address(hostname)) {
    return true;
  }

  const parts = hostname.split('.').map(Number);
  if (parts.length !== 4 || parts.some((part) => Number.isNaN(part))) {
    return false;
  }

  const [first, second] = parts;

  return (
    first === 10 ||
    first === 127 ||
    (first === 172 && second >= 16 && second <= 31) ||
    (first === 192 && second === 168) ||
    (first === 169 && second === 254)
  );
};

const isPrivateIPv6Address = (hostname: string): boolean => {
  const normalized = hostname.toLowerCase();

  return (
    normalized === '::1' ||
    normalized.startsWith('fc') ||
    normalized.startsWith('fd') ||
    normalized.startsWith('fe8') ||
    normalized.startsWith('fe9') ||
    normalized.startsWith('fea') ||
    normalized.startsWith('feb') ||
    normalized.startsWith('::ffff:10.') ||
    normalized.startsWith('::ffff:127.') ||
    normalized.startsWith('::ffff:169.254.') ||
    normalized.startsWith('::ffff:192.168.')
  );
};
