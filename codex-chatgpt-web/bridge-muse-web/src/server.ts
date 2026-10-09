/**
 * Serveur minimal compatible API Anthropic pour Claude Code.
 *
 *   ANTHROPIC_BASE_URL=http://127.0.0.1:8741 claude "dis bonjour"
 *
 * Traduit POST /v1/messages (SSE) -> MuseWebAdapter.send(),
 * et re-stream la réponse d'A0 comme des content_block_delta.
 *
 * v1 : A0 répond avec SES propres outils (le harness le voit comme
 * un modèle sans tools). v2 : tool-calls retour vers Claude Code.
 */
import { serve } from "bun";
import { MuseWebAdapter } from "./surfaces/muse-web/adapter.ts";

const PORT = 8741;
const adapter = new MuseWebAdapter(
  process.env.BRIDGE_PROFILE_DIR ?? "./.bridge-profile",
  new URL("./surfaces/muse-web/selectors.json", import.meta.url).pathname,
);

await adapter.connect();
console.log(`[bridge] muse_web connecté — écoute sur http://127.0.0.1:${PORT}`);

type AnthropicMessage = { role: string; content: string | unknown[] };

function toPrompt(body: any): string {
  const parts: string[] = [];
  if (body.system) {
    parts.push(
      typeof body.system === "string"
        ? body.system
        : body.system.map((b: any) => b.text ?? "").join("\n"),
    );
  }
  for (const m of body.messages as AnthropicMessage[]) {
    const text =
      typeof m.content === "string"
        ? m.content
        : m.content
            .map((b: any) => (b.type === "text" ? b.text : `[${b.type}]`))
            .join("\n");
    parts.push(m.role === "user" ? text : `[assistant] ${text}`);
  }
  return parts.join("\n\n");
}

serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);
    if (req.method === "POST" && url.pathname === "/v1/messages") {
      const body = await req.json();
      const prompt = toPrompt(body);
      const stream = body.stream === true;

      const sseHeaders = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      };

      const encoder = new TextEncoder();
      const readable = new ReadableStream({
        async start(controller) {
          const send = (event: string, data: object) =>
            controller.enqueue(
              encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`),
            );
          send("message_start", {
            message: { id: "msg_bridge", type: "message", role: "assistant", content: [], model: body.model, stop_reason: null },
          });
          send("content_block_start", { index: 0, content_block: { type: "text", text: "" } });
          try {
            const evidence = await adapter.send(prompt, (delta) =>
              send("content_block_delta", { index: 0, delta: { type: "text_delta", text: delta } }),
            );
            console.log(`[bridge] tour terminé — preuve : ${evidence.threadUrl}`);
          } catch (err: any) {
            send("content_block_delta", { index: 0, delta: { type: "text_delta", text: `\n\n[bridge erreur] ${err.message}` } });
          }
          send("content_block_stop", { index: 0 });
          send("message_stop", {});
          controller.close();
        },
      });
      return new Response(stream ? readable : readable, { headers: sseHeaders });
    }
    if (url.pathname === "/health") return Response.json({ ok: true, surface: "muse_web" });
    return new Response("bridge-muse-web : POST /v1/messages", { status: 404 });
  },
});
