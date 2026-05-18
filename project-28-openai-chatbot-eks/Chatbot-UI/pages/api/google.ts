import { Message } from '@/types/chat';
import { GoogleBody, GoogleSource } from '@/types/google';
import { OPENAI_API_HOST } from '@/utils/app/const';
import {
  cleanSourceText,
  isPublicHTTPURL,
  readLimitedText,
} from '@/utils/server/google';
import {
  RequestValidationError,
  resolveOpenAIAPIKey,
  validateChatBody,
} from '@/utils/server/request';
import { Readability } from '@mozilla/readability';
import endent from 'endent';
import jsdom, { JSDOM } from 'jsdom';
import { NextApiRequest, NextApiResponse } from 'next';

const handler = async (req: NextApiRequest, res: NextApiResponse<any>) => {
  try {
    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method not allowed' });
    }

    const { messages, key, model, googleAPIKey, googleCSEId } =
      req.body as GoogleBody;

    validateChatBody({ model, messages, key, prompt: req.body?.prompt });
    const apiKey = resolveOpenAIAPIKey(key);

    const searchAPIKey = googleAPIKey?.trim() || process.env.GOOGLE_API_KEY;
    const searchCSEId = googleCSEId?.trim() || process.env.GOOGLE_CSE_ID;
    if (!searchAPIKey || !searchCSEId) {
      throw new RequestValidationError('Google search credentials are required');
    }

    const userMessage = messages[messages.length - 1];
    const query = userMessage.content.trim().slice(0, 500);

    const googleRes = await fetch(
      `https://customsearch.googleapis.com/customsearch/v1?${new URLSearchParams(
        {
          key: searchAPIKey,
          cx: searchCSEId,
          q: query,
          num: '5',
        },
      )}`,
    );

    if (!googleRes.ok) {
      throw new Error(`Google API returned status ${googleRes.status}`);
    }

    const googleData = await googleRes.json();
    if (!Array.isArray(googleData.items)) {
      return res.status(200).json({ answer: 'No Google search results found.' });
    }

    const sources: GoogleSource[] = googleData.items.map((item: any) => ({
      title: item.title,
      link: item.link,
      displayLink: item.displayLink,
      snippet: item.snippet,
      image: item.pagemap?.cse_image?.[0]?.src,
      text: '',
    }));

    const sourcesWithText: any = await Promise.all(
      sources.map(async (source) => {
        try {
          if (!isPublicHTTPURL(source.link)) {
            return null;
          }

          const timeoutPromise = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request timed out')), 5000),
          );

          const res = (await Promise.race([
            fetch(source.link, { redirect: 'manual' }),
            timeoutPromise,
          ])) as Response;

          if (!res.ok) {
            return null;
          }

          const html = await readLimitedText(res);
          if (!html) {
            return null;
          }

          const virtualConsole = new jsdom.VirtualConsole();
          virtualConsole.on('error', (error) => {
            if (!error.message.includes('Could not parse CSS stylesheet')) {
              console.error(error);
            }
          });

          const dom = new JSDOM(html, { virtualConsole });
          const doc = dom.window.document;
          const parsed = new Readability(doc).parse();

          if (parsed) {
            let sourceText = cleanSourceText(parsed.textContent);

            return {
              ...source,
              // TODO: switch to tokens
              text: sourceText.slice(0, 2000),
            } as GoogleSource;
          }
          // }

          return null;
        } catch (error) {
          console.error(error);
          return null;
        }
      }),
    );

    const filteredSources: GoogleSource[] = sourcesWithText.filter(Boolean);

    const answerPrompt = endent`
    Provide me with the information I requested. Use the sources to provide an accurate response. Respond in markdown format. Cite the sources you used as a markdown link as you use them at the end of each sentence by number of the source (ex: [[1]](link.com)). Provide an accurate response and then stop. Today's date is ${new Date().toLocaleDateString()}.

    Example Input:
    What's the weather in San Francisco today?

    Example Sources:
    [Weather in San Francisco](https://www.google.com/search?q=weather+san+francisco)

    Example Response:
    It's 70 degrees and sunny in San Francisco today. [[1]](https://www.google.com/search?q=weather+san+francisco)

    Input:
    ${userMessage.content.trim()}

    Sources:
    ${filteredSources.map((source) => {
      return endent`
      ${source.title} (${source.link}):
      ${source.text}
      `;
    })}

    Response:
    `;

    const answerMessage: Message = { role: 'user', content: answerPrompt };

    const answerRes = await fetch(`${OPENAI_API_HOST}/v1/chat/completions`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
        ...(process.env.OPENAI_ORGANIZATION && {
          'OpenAI-Organization': process.env.OPENAI_ORGANIZATION,
        }),
      },
      method: 'POST',
      body: JSON.stringify({
        model: model.id,
        messages: [
          {
            role: 'system',
            content: `Use the sources to provide an accurate response. Respond in markdown format. Cite the sources you used as [1](link), etc, as you use them.`,
          },
          answerMessage,
        ],
        max_tokens: 1000,
        temperature: 1,
        stream: false,
      }),
    });

    if (!answerRes.ok) {
      throw new Error(`OpenAI API returned status ${answerRes.status}`);
    }

    const { choices: choices2 } = await answerRes.json();
    const answer = choices2?.[0]?.message?.content;
    if (!answer) {
      throw new Error('OpenAI API returned an empty answer');
    }

    res.status(200).json({ answer });
  } catch (error) {
    if (error instanceof RequestValidationError) {
      return res.status(error.status).json({ error: error.message });
    }

    console.error(error);
    return res.status(500).json({ error: 'Error' });
  }
};

export default handler;
