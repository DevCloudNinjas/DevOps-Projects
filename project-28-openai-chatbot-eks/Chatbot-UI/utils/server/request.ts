import { ChatBody, Message } from '@/types/chat';
import { OpenAIModelID } from '@/types/openai';

const MAX_API_KEY_LENGTH = 256;
const MAX_MESSAGES = 50;
const MAX_MESSAGE_LENGTH = 12000;
const MAX_TOTAL_MESSAGE_LENGTH = 60000;
const MAX_PROMPT_LENGTH = 12000;
const MAX_TOKEN_LIMIT = 32000;
const MAX_MODEL_NAME_LENGTH = 64;

export class RequestValidationError extends Error {
  status: number;

  constructor(message: string, status = 400) {
    super(message);
    this.name = 'RequestValidationError';
    this.status = status;
  }
}

export const isServerOpenAIKeyAllowed = () =>
  process.env.ALLOW_SERVER_OPENAI_API_KEY === 'true';

export const resolveOpenAIAPIKey = (providedKey?: string) => {
  const trimmedKey = providedKey?.trim();

  if (trimmedKey) {
    if (trimmedKey.length > MAX_API_KEY_LENGTH) {
      throw new RequestValidationError('OpenAI API key is too long');
    }

    return trimmedKey;
  }

  if (isServerOpenAIKeyAllowed() && process.env.OPENAI_API_KEY) {
    return process.env.OPENAI_API_KEY;
  }

  throw new RequestValidationError('OpenAI API key is required', 401);
};

export const parseJSONBody = async <T>(req: Request): Promise<T> => {
  if (req.method !== 'POST') {
    throw new RequestValidationError('Method not allowed', 405);
  }

  try {
    return (await req.json()) as T;
  } catch {
    throw new RequestValidationError('Invalid JSON body');
  }
};

export const validateChatBody = (body: Partial<ChatBody>) => {
  if (!body || typeof body !== 'object') {
    throw new RequestValidationError('Request body is required');
  }

  const model = body.model;
  if (
    !model ||
    typeof model.id !== 'string' ||
    model.id.length > MAX_MODEL_NAME_LENGTH ||
    !Object.values(OpenAIModelID).includes(model.id as OpenAIModelID) ||
    typeof model.tokenLimit !== 'number' ||
    model.tokenLimit <= 0 ||
    model.tokenLimit > MAX_TOKEN_LIMIT
  ) {
    throw new RequestValidationError('Invalid model');
  }

  if (!Array.isArray(body.messages) || body.messages.length === 0) {
    throw new RequestValidationError('At least one message is required');
  }

  if (body.messages.length > MAX_MESSAGES) {
    throw new RequestValidationError('Too many messages');
  }

  let totalLength = 0;
  for (const message of body.messages) {
    validateMessage(message);
    totalLength += message.content.length;
  }

  if (totalLength > MAX_TOTAL_MESSAGE_LENGTH) {
    throw new RequestValidationError('Messages are too large');
  }

  if (
    body.prompt !== undefined &&
    (typeof body.prompt !== 'string' || body.prompt.length > MAX_PROMPT_LENGTH)
  ) {
    throw new RequestValidationError('Invalid system prompt');
  }
};

const validateMessage = (message: Message) => {
  if (
    !message ||
    (message.role !== 'assistant' && message.role !== 'user') ||
    typeof message.content !== 'string' ||
    message.content.trim().length === 0 ||
    message.content.length > MAX_MESSAGE_LENGTH
  ) {
    throw new RequestValidationError('Invalid message');
  }
};

export const validationErrorResponse = (error: unknown) => {
  if (error instanceof RequestValidationError) {
    return new Response(error.message, { status: error.status });
  }

  return null;
};
