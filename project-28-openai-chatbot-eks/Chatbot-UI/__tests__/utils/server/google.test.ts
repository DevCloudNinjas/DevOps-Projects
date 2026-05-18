import {
  cleanSourceText,
  isPublicHTTPURL,
  readLimitedText,
} from '@/utils/server/google';
import { describe, expect, it } from 'vitest';

describe('Google SSRF helper behavior', () => {
  it('allows public HTTP and HTTPS URLs without credentials', () => {
    expect(isPublicHTTPURL('https://example.com/article')).toBe(true);
    expect(isPublicHTTPURL('http://news.example.org/story')).toBe(true);
  });

  it('rejects unsupported schemes, credentials, and local hostnames', () => {
    expect(isPublicHTTPURL('file:///etc/passwd')).toBe(false);
    expect(isPublicHTTPURL('https://user:pass@example.com')).toBe(false);
    expect(isPublicHTTPURL('http://localhost:3000')).toBe(false);
    expect(isPublicHTTPURL('https://admin.internal/status')).toBe(false);
  });

  it('rejects private IPv4 and IPv6 destinations', () => {
    expect(isPublicHTTPURL('http://10.0.0.1')).toBe(false);
    expect(isPublicHTTPURL('http://127.0.0.1')).toBe(false);
    expect(isPublicHTTPURL('http://169.254.169.254/latest/meta-data')).toBe(
      false,
    );
    expect(isPublicHTTPURL('http://[::1]/')).toBe(false);
    expect(isPublicHTTPURL('http://[fc00::1]/')).toBe(false);
    expect(isPublicHTTPURL('http://[fe80::1]/')).toBe(false);
  });
});

describe('Google source text helpers', () => {
  it('cleans noisy source text', () => {
    expect(cleanSourceText('\n\nHello\t\t   world\n\n\n\nagain\n')).toBe(
      'Hello  world\nagain',
    );
  });

  it('reads small html or plain text responses', async () => {
    const response = new Response('<html>Hello</html>', {
      headers: { 'content-type': 'text/html' },
    });

    await expect(readLimitedText(response)).resolves.toBe('<html>Hello</html>');
  });

  it('rejects unsupported content types and oversized content-length', async () => {
    await expect(
      readLimitedText(
        new Response('{"ok":true}', {
          headers: { 'content-type': 'application/json' },
        }),
      ),
    ).resolves.toBeNull();

    await expect(
      readLimitedText(
        new Response('too large', {
          headers: {
            'content-type': 'text/plain',
            'content-length': '500001',
          },
        }),
      ),
    ).resolves.toBeNull();
  });
});
