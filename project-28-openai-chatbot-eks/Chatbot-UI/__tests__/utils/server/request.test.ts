import { OpenAIModels, OpenAIModelID } from '@/types/openai';
import {
  RequestValidationError,
  parseJSONBody,
  resolveOpenAIAPIKey,
  validateChatBody,
  validationErrorResponse,
} from '@/utils/server/request';
import { afterEach, describe, expect, it, vi } from 'vitest';

const validBody = {
  model: OpenAIModels[OpenAIModelID.GPT_3_5],
  messages: [{ role: 'user' as const, content: 'Hello' }],
  key: 'sk-user-key',
  prompt: 'You are helpful.',
};

describe('request validation helpers', () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it('parses POST JSON bodies', async () => {
    const request = new Request('https://example.test/api/chat', {
      method: 'POST',
      body: JSON.stringify(validBody),
    });

    await expect(parseJSONBody(request)).resolves.toEqual(validBody);
  });

  it('rejects non-POST requests before reading the body', async () => {
    const request = new Request('https://example.test/api/chat', {
      method: 'GET',
    });

    await expect(parseJSONBody(request)).rejects.toMatchObject({
      message: 'Method not allowed',
      status: 405,
    });
  });

  it('uses a provided OpenAI key after trimming whitespace', () => {
    expect(resolveOpenAIAPIKey('  sk-user-key  ')).toBe('sk-user-key');
  });

  it('only falls back to the server OpenAI key when explicitly allowed', () => {
    vi.stubEnv('OPENAI_API_KEY', 'sk-server-key');

    expect(() => resolveOpenAIAPIKey('')).toThrow(
      new RequestValidationError('OpenAI API key is required', 401),
    );

    vi.stubEnv('ALLOW_SERVER_OPENAI_API_KEY', 'true');

    expect(resolveOpenAIAPIKey(undefined)).toBe('sk-server-key');
  });

  it('rejects malformed chat payloads', () => {
    expect(() =>
      validateChatBody({
        ...validBody,
        messages: [{ role: 'user', content: '   ' }],
      }),
    ).toThrow(new RequestValidationError('Invalid message'));
  });

  it('turns validation errors into HTTP responses', async () => {
    const response = validationErrorResponse(
      new RequestValidationError('OpenAI API key is required', 401),
    );

    expect(response?.status).toBe(401);
    await expect(response?.text()).resolves.toBe('OpenAI API key is required');
  });
});
